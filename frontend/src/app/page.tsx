"use client";
import { useState } from "react";

export default function VectorPulseDashboard() {
  const [prompt, setPrompt] = useState("");
  const [threatActor, setThreatActor] = useState("");
  const [response, setResponse] = useState("");
  const [loadingChat, setLoadingChat] = useState(false);
  const [loadingIngest, setLoadingIngest] = useState(false);

  // Function to ask the AI a question
  const handleChat = async () => {
    if (!prompt) return;
    setLoadingChat(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setResponse(data.answer);
    } catch (error) {
      setResponse("❌ Connection to VectorPulse Core failed. Make sure the FastAPI backend is running.");
    }
    setLoadingChat(false);
  };

  // Function to trigger background AlienVault ingestion
  const handleIngest = async () => {
    if (!threatActor) return;
    setLoadingIngest(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/ingest/otx", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ threat_actor: threatActor }),
      });
      const data = await res.json();
      alert(`✅ ${data.message} (Task ID: ${data.task_id})`);
    } catch (error) {
      alert("❌ Failed to start ingestion. Make sure the FastAPI backend is running.");
    }
    setLoadingIngest(false);
    setThreatActor("");
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-300 font-mono p-8 selection:bg-green-900">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="border-b border-slate-800 pb-4">
          <h1 className="text-4xl font-bold tracking-tight text-green-500">VectorPulse</h1>
          <p className="text-slate-500 mt-2">Enterprise Cyber Threat Intelligence Platform</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Left Sidebar: Data Ingestion Controls */}
          <div className="md:col-span-1 bg-slate-900 border border-slate-800 p-6 rounded-lg h-fit space-y-6 shadow-xl">
            <h2 className="text-xl font-semibold text-white">Data Integration</h2>
            <div className="space-y-4">
              <label className="text-sm text-slate-400">Pull AlienVault OTX Pulses</label>
              <input
                type="text"
                placeholder="e.g., APT29, Scattered Spider..."
                className="w-full bg-slate-950 border border-slate-700 rounded-md p-3 text-sm focus:outline-none focus:border-green-500 transition-colors"
                value={threatActor}
                onChange={(e) => setThreatActor(e.target.value)}
              />
              <button 
                onClick={handleIngest}
                disabled={loadingIngest}
                className="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 text-green-400 px-4 py-2 rounded-md text-sm font-semibold transition-all shadow-sm disabled:opacity-50"
              >
                {loadingIngest ? "Ingesting Data..." : "Run Intel Extraction"}
              </button>
            </div>
            <div className="text-xs text-slate-600 mt-6 border-t border-slate-800 pt-4">
              Background workers (Celery) will process feeds without blocking the UI.
            </div>
          </div>

          {/* Right Area: RAG Chat Interface */}
          <div className="md:col-span-2 flex flex-col space-y-4">
            <div className="flex-1 bg-slate-900 border border-slate-800 p-6 rounded-lg min-h-[400px] shadow-xl overflow-y-auto">
              <h2 className="text-xl font-semibold text-white mb-6">Threat Intelligence Copilot</h2>
              
              {response ? (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-md whitespace-pre-wrap leading-relaxed text-slate-300">
                  {response}
                </div>
              ) : (
                <div className="flex items-center justify-center h-48 text-slate-600 italic">
                  Database initialized. Awaiting queries...
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="flex gap-4">
              <input
                type="text"
                className="flex-1 bg-slate-900 border border-slate-700 rounded-lg p-4 focus:outline-none focus:border-green-500 shadow-xl transition-colors text-white"
                placeholder="Query database (e.g., 'What IPs are associated with the latest APT29 pulse?')"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleChat()}
              />
              <button 
                onClick={handleChat}
                disabled={loadingChat}
                className="bg-green-600 hover:bg-green-500 text-white px-8 py-4 rounded-lg font-bold transition-colors shadow-lg disabled:opacity-50"
              >
                {loadingChat ? "Analyzing..." : "Query VectorDB"}
              </button>
            </div>
          </div>
          
        </div>
      </div>
    </main>
  );
}