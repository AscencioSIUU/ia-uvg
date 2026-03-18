import React from 'react';

const Navbar = ({ maze, heuristic, setHeuristic, handleFileUpload, handleRestart, handleStart, isSolving }) => {
  return (
    <header className="navbar">
      <div className="nav-left">
        <h1 className="logo">MAZE ENGINE</h1>
        
        <div className="nav-controls">
          <div className="input-group">
            <input 
              type="file" 
              onChange={handleFileUpload} 
              accept=".txt" 
              id="file-upload" 
            />
            <label htmlFor="file-upload" className="custom-file-upload">
              {maze ? "MAPA CARGADO" : "CARGAR MAPA (.TXT)"}
            </label>
          </div>

          <div className="input-group">
            <select 
              className="heuristic-select"
              value={heuristic} 
              onChange={e => setHeuristic(e.target.value)}
            >
              <option value="Manhattan">MANHATTAN</option>
              <option value="Euclidean">EUCLIDEAN</option>
            </select>
          </div>
        </div>
      </div>

      <div className="nav-right">
        <button className="btn-restart" onClick={handleRestart}>
          REINICIAR
        </button>
        <button 
          className="btn-start" 
          disabled={!maze || isSolving} 
          onClick={handleStart}
        >
          {isSolving ? "SIMULANDO..." : "INICIAR"}
        </button>
      </div>
    </header>
  );
};

export default Navbar;
