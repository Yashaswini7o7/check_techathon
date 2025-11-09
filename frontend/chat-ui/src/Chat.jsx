import React, { useState, useRef } from "react";
import axios from "axios";

export default function Chat({ sessionId, customerId }){
  const [messages, setMessages] = useState([{from:"bot", text:"Hello! Type 'hi' to start."}]);
  const [input, setInput] = useState("");
  const [awaitUpload, setAwaitUpload] = useState(false);
  const fileRef = useRef(null);

  const append = (m) => setMessages(prev => [...prev, m]);

  async function sendText(text){
    append({from:"user", text});
    try{
      const res = await axios.post("http://localhost:8000/chat/send", {
        session_id: sessionId,
        customer_id: customerId,
        text
      });
      const botText = res.data.responses.join("\n");
      append({from:"bot", text: botText});
      const stage = res.data.context && res.data.context.stage;
      if(stage === "await_salary") setAwaitUpload(true);
      else setAwaitUpload(false);
    }catch(err){
      append({from:"bot", text:"Error contacting server."});
      console.error(err);
    }
  }

  async function uploadSalary(){
    const file = fileRef.current.files[0];
    if(!file) return alert("Choose a file");
    const fd = new FormData();
    fd.append("session_id", sessionId);
    fd.append("file", file);
    try{
      const res = await axios.post("http://localhost:8000/upload/salary", fd, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      append({from:"bot", text:"Salary slip uploaded."});
      // notify master agent to re-run
      await sendText("uploaded_salary");
      setAwaitUpload(false);
    }catch(err){
      append({from:"bot", text:"Upload failed."});
    }
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={"msg " + (m.from==="user" ? "user":"bot")}>
            <div className="bubble">{m.text}</div>
          </div>
        ))}
      </div>
      {awaitUpload && (
        <div className="upload-row">
          <input ref={fileRef} type="file" />
          <button onClick={uploadSalary}>Upload Salary Slip</button>
        </div>
      )}
      <div className="input-row">
        <input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>{ if(e.key==="Enter"){ sendText(input); setInput(""); }}} placeholder="Type message and press Enter" />
        <button onClick={()=>{ sendText(input); setInput(""); }}>Send</button>
      </div>
    </div>
  );
}
