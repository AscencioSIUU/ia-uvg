import React, { useState, useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import Navbar from './Navbar';
import './App.css';

const ALGOS = ["BFS", "DFS", "Greedy", "A*"];
const MAZE_SIZE = 128;
const ANIMATION_SPEED = 2; // Cantidad de pasos por frame (ajusta para más lento/rápido)

const Quadrant = forwardRef(({ algo, maze }, ref) => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [metrics, setMetrics] = useState(null);
  const [isComplete, setIsComplete] = useState(false);
  
  // Cola interna para la animación
  const stepQueue = useRef([]);
  const animationRef = useRef(null);

  useImperativeHandle(ref, () => ({
    pushStep: (pos, isFinal) => {
      stepQueue.current.push({ pos, isFinal });
    },
    setMetrics: (data) => {
      // Esperar a que la cola se vacíe antes de marcar como completo
      const checkDone = setInterval(() => {
        if (stepQueue.current.length === 0) {
          setMetrics(data);
          setIsComplete(true);
          clearInterval(checkDone);
        }
      }, 100);
    },
    reset: () => {
      stepQueue.current = [];
      setMetrics(null);
      setIsComplete(false);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      initCanvas();
      startAnimationLoop();
    }
  }));

  const startAnimationLoop = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    const animate = () => {
      if (stepQueue.current.length > 0) {
        // Procesar N pasos por frame para fluidez
        for (let i = 0; i < ANIMATION_SPEED; i++) {
          const step = stepQueue.current.shift();
          if (!step) break;

          const cellSize = Math.min(canvas.width, canvas.height) / MAZE_SIZE;
          const offsetX = (canvas.width - (MAZE_SIZE * cellSize)) / 2;
          const offsetY = (canvas.height - (MAZE_SIZE * cellSize)) / 2;

          if (step.isFinal) {
            ctx.fillStyle = '#ffeb3b';
            ctx.shadowBlur = 5;
            ctx.shadowColor = '#ffeb3b';
          } else {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
            ctx.shadowBlur = 0;
          }
          
          ctx.fillRect(offsetX + step.pos[1] * cellSize, offsetY + step.pos[0] * cellSize, cellSize, cellSize);
          
          // Resaltar el "cabezal" de la decisión actual en blanco brillante
          if (!step.isFinal) {
            ctx.fillStyle = '#fff';
            ctx.fillRect(offsetX + step.pos[1] * cellSize, offsetY + step.pos[0] * cellSize, cellSize, cellSize);
          }
        }
      }
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
  };

  const initCanvas = () => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;
    
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    const ctx = canvas.getContext('2d');
    
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (!maze) return;

    const cellSize = Math.min(canvas.width, canvas.height) / MAZE_SIZE;
    const offsetX = (canvas.width - (MAZE_SIZE * cellSize)) / 2;
    const offsetY = (canvas.height - (MAZE_SIZE * cellSize)) / 2;

    for (let r = 0; r < maze.length; r++) {
      for (let c = 0; c < maze[0].length; c++) {
        const val = maze[r][c];
        if (val === 1) ctx.fillStyle = '#000';
        else if (val === 2) ctx.fillStyle = '#4caf50';
        else if (val === 3) ctx.fillStyle = '#f44336';
        else ctx.fillStyle = '#111';
        ctx.fillRect(offsetX + c * cellSize, offsetY + r * cellSize, cellSize, cellSize);
      }
    }
  };

  useEffect(() => {
    initCanvas();
    startAnimationLoop();
    window.addEventListener('resize', initCanvas);
    return () => {
      window.removeEventListener('resize', initCanvas);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [maze]);

  return (
    <div className={`quadrant ${isComplete ? 'is-complete' : ''}`} ref={containerRef}>
      <div className="quad-header">
        <span>{algo}</span>
      </div>
      <div className="quad-content-row">
        <div className="canvas-container">
          <canvas ref={canvasRef} />
        </div>
        <div className="metrics-sidebar">
          <div className="metric-group">
            <label>Nodos</label>
            <span>{metrics?.nodes_explored || 0}</span>
          </div>
          <div className="metric-group">
            <label>Camino</label>
            <span>{metrics?.path_length || 0}</span>
          </div>
          <div className="metric-group">
            <label>Tiempo</label>
            <span>{metrics?.execution_time?.toFixed(3) || "0.000"}s</span>
          </div>
          <div className="metric-group">
            <label>B Factor</label>
            <span>{metrics?.branching_factor?.toFixed(2) || "0.00"}</span>
          </div>
        </div>
      </div>
    </div>
  );
});

function App() {
  const [maze, setMaze] = useState(null);
  const [heuristic, setHeuristic] = useState('Manhattan');
  const [socket, setSocket] = useState(null);
  const [isSolving, setIsSolving] = useState(false);
  
  const quadRefs = {
    BFS: useRef(null),
    DFS: useRef(null),
    Greedy: useRef(null),
    "A*": useRef(null)
  };

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/solve');
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'step') {
        quadRefs[msg.algo]?.current?.pushStep(msg.pos, msg.is_final);
      } else if (msg.type === 'metrics') {
        quadRefs[msg.algo]?.current?.setMetrics(msg.data);
      } else if (msg.type === 'complete') {
        setIsSolving(false);
      }
    };
    setSocket(ws);
    return () => ws.close();
  }, []);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target.result;
      const grid = text.trim().split('\n').map(line => line.trim().split('').map(Number));
      setMaze(grid);
      handleRestart();
    };
    reader.readAsText(file);
  };

  const handleStart = () => {
    if (!maze || !socket || isSolving) return;
    setIsSolving(true);
    ALGOS.forEach(algo => quadRefs[algo].current?.reset());
    socket.send(JSON.stringify({ maze, heuristic }));
  };

  const handleRestart = () => {
    setIsSolving(false);
    ALGOS.forEach(algo => quadRefs[algo].current?.reset());
  };

  return (
    <div className="app-container">
      <Navbar 
        maze={maze}
        heuristic={heuristic}
        setHeuristic={setHeuristic}
        handleFileUpload={handleFileUpload}
        handleRestart={handleRestart}
        handleStart={handleStart}
        isSolving={isSolving}
      />

      <main className="grid-race">
        {ALGOS.map(algo => (
          <Quadrant 
            key={algo} 
            ref={quadRefs[algo]}
            algo={algo} 
            maze={maze}
          />
        ))}
      </main>
    </div>
  );
}

export default App;
