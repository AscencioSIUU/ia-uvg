import React, { useState, useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import Navbar from './Navbar';
import './App.css';

const ALGOS = ["BFS", "DFS", "Greedy", "A*"];
const ANIMATION_SPEED = 5; // Pasos por frame — menor = más lento y visible

const RANK_LABELS = ['1°', '2°', '3°', '4°'];

const Quadrant = forwardRef(({ algo, maze, rank, onComplete }, ref) => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [metrics, setMetrics] = useState(null);
  const [isComplete, setIsComplete] = useState(false);

  const stepQueue = useRef([]);
  const animationRef = useRef(null);
  // Dimensiones de celda calculadas al dibujar el maze (para reusar en animación)
  const cellDims = useRef({ cellW: 1, cellH: 1 });

  useImperativeHandle(ref, () => ({
    pushStep: (pos, isFinal) => {
      stepQueue.current.push({ pos, isFinal });
    },
    setMetrics: (data) => {
      const checkDone = setInterval(() => {
        if (stepQueue.current.length === 0) {
          setMetrics(data);
          setIsComplete(true);
          clearInterval(checkDone);
          onComplete?.();
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
        const { cellW, cellH } = cellDims.current;
        for (let i = 0; i < ANIMATION_SPEED; i++) {
          const step = stepQueue.current.shift();
          if (!step) break;

          if (step.isFinal) {
            ctx.fillStyle = '#ffeb3b';
            ctx.shadowBlur = 4;
            ctx.shadowColor = '#ffeb3b';
          } else {
            ctx.shadowBlur = 0;
            ctx.fillStyle = 'rgba(255,255,255,0.45)';
          }
          ctx.fillRect(step.pos[1] * cellW, step.pos[0] * cellH, cellW, cellH);

          if (!step.isFinal) {
            ctx.fillStyle = '#fff';
            ctx.fillRect(step.pos[1] * cellW, step.pos[0] * cellH, cellW, cellH);
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

    // Calcular celdas para que el maze llene todo el canvas
    const rows = maze.length;
    const cols = maze[0].length;
    const cellW = canvas.width / cols;
    const cellH = canvas.height / rows;
    cellDims.current = { cellW, cellH };

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const val = maze[r][c];
        if (val === 1) ctx.fillStyle = '#000';
        else if (val === 2) ctx.fillStyle = '#4caf50';
        else if (val === 3) ctx.fillStyle = '#f44336';
        else ctx.fillStyle = '#111';
        ctx.fillRect(c * cellW, r * cellH, cellW, cellH);
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
    <div className={`quadrant ${isComplete ? 'is-complete' : ''}`}>
      <div className="quad-header">
        <span className="algo-name">{algo}</span>
        {rank !== null && rank !== undefined && (
          <span className="finish-rank">{RANK_LABELS[rank - 1]}</span>
        )}
      </div>
      <div className="quad-content-row">
        <div className="canvas-container" ref={containerRef}>
          <canvas ref={canvasRef} />
        </div>
        <div className="metrics-sidebar">
          <div className="metric-group">
            <label>Nodos</label>
            <span>{metrics?.nodes_explored ?? '—'}</span>
          </div>
          <div className="metric-group">
            <label>Camino</label>
            <span>{metrics?.path_length ?? '—'}</span>
          </div>
          <div className="metric-group">
            <label>Tiempo</label>
            <span>{metrics?.execution_time != null ? metrics.execution_time.toFixed(3) + 's' : '—'}</span>
          </div>
          <div className="metric-group">
            <label>B Factor</label>
            <span>{metrics?.branching_factor != null ? metrics.branching_factor.toFixed(2) : '—'}</span>
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
  const [finishOrder, setFinishOrder] = useState({});
  const finishCounter = useRef(0);

  const quadRefs = {
    BFS: useRef(null),
    DFS: useRef(null),
    Greedy: useRef(null),
    "A*": useRef(null)
  };

  const handleAlgoComplete = (algo) => {
    finishCounter.current += 1;
    const rank = finishCounter.current;
    setFinishOrder(prev => ({ ...prev, [algo]: rank }));
  };

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/solve');
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'batch') {
        const ref = quadRefs[msg.algo]?.current;
        if (ref) msg.steps.forEach(s => ref.pushStep(s.pos, s.is_final));
      } else if (msg.type === 'step') {
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
    finishCounter.current = 0;
    setFinishOrder({});
    setIsSolving(true);
    ALGOS.forEach(algo => quadRefs[algo].current?.reset());
    socket.send(JSON.stringify({ maze, heuristic }));
  };

  const handleRestart = () => {
    finishCounter.current = 0;
    setFinishOrder({});
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
            rank={finishOrder[algo] ?? null}
            onComplete={() => handleAlgoComplete(algo)}
          />
        ))}
      </main>
    </div>
  );
}

export default App;
