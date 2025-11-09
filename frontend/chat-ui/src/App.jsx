import React, { useState, useEffect } from "react";
import Chat from "./Chat";
import "./styles.css";

export default function App(){
  const [sessionId] = useState(() => "sess_" + Math.random().toString(36).slice(2,9));
  const [customerId, setCustomerId] = useState("C001");

  return (
    <div className="app">
      <header><h2>Tata Capital - Loan Assistant (Demo)</h2></header>
      <div className="controls">
        <label>Customer ID: 
          <select value={customerId} onChange={e=>setCustomerId(e.target.value)}>
            <option value="C001">C001</option>
            <option value="C002">C002</option>
            <option value="C003">C003</option>
            <option value="C004">C004</option>
            <option value="C005">C005</option>
            <option value="C006">C006</option>
            <option value="C007">C007</option>
            <option value="C008">C008</option>
            <option value="C009">C009</option>
            <option value="C010">C010</option>
          </select>
        </label>
      </div>
      <Chat sessionId={sessionId} customerId={customerId}/>
    </div>
  );
}
