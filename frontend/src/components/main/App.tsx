import React from 'react';
import './App.css';
import SimpleHealthbar from '../healthbars/SimpleHealthbar/SimpleHealthbar'
import '../../stylesheets-main/switch.css'

function App() {
  return (
    <div className="main-container">
      <div className="healthbar-container">
        <h1 className="title">
          HP
        </h1>
        <SimpleHealthbar></SimpleHealthbar>
      </div>
      <label className="switch">
        <input type="checkbox"></input>
        <span className="slider round"></span>
      </label>
    </div>
  );
}

export default App;
