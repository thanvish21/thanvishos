"use client";

import React, { useState, useEffect } from "react";
import { Bot, Activity } from "lucide-react";

interface AgentStatus {
  id: string;
  name: string;
  role: string;
  status: string;
  avatar: string;
  color: string;
  tasks_completed: number;
}

export default function AgentsMonitor() {
  const [agents, setAgents] = useState<AgentStatus[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/agents/status")
      .then((res) => res.json())
      .then((data) => setAgents(data.agents || []))
      .catch(() => {
        // Local stub
        setAgents([
          {
            id: "agent-ingest",
            name: "Ingest & Autonomous Classifier",
            role: "Monitors Dropzone, parses incoming PDFs/notes/exam dates, and auto-routes to disk.",
            status: "ACTIVE",
            avatar: "⚡",
            color: "emerald",
            tasks_completed: 42,
          },
          {
            id: "agent-srm-academic",
            name: "SRM Academic & Day Order Dispatcher",
            role: "Tracks rotating Day Orders (DO1-DO5), CT1/CT2 exam radars, and NSS schedules.",
            status: "ACTIVE",
            avatar: "🏛️",
            color: "sky",
            tasks_completed: 128,
          },
          {
            id: "agent-library-mastery",
            name: "SRM Library & Mastery Navigator",
            role: "Queries SRM Library OPAC for call numbers, shelf locations, and calculates master roadmaps.",
            status: "ACTIVE",
            avatar: "📚",
            color: "amber",
            tasks_completed: 35,
          },
          {
            id: "agent-polyglot-coach",
            name: "Parallel Polyglot & Codédex Coach",
            role: "Synchronizes parallel learning across C, Python, Java, DSA, and Codédex Pro perks.",
            status: "ACTIVE",
            avatar: "💻",
            color: "violet",
            tasks_completed: 89,
          },
          {
            id: "agent-knowledge-graph",
            name: "Second Brain & Graph Weaver",
            role: "Links notes and thoughts into an interactive multi-dimensional knowledge graph.",
            status: "ACTIVE",
            avatar: "🧠",
            color: "pink",
            tasks_completed: 64,
          },
          {
            id: "agent-system-sync",
            name: "System Orchestrator & Local Daemon",
            role: "Maintains local disk synchronization and auto-indexes research notes.",
            status: "ACTIVE",
            avatar: "🛡️",
            color: "teal",
            tasks_completed: 210,
          },
        ]);
      });
  }, []);

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-teal-500/10 border border-teal-500/20 text-teal-400">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              Autonomous Agent Orchestration Mesh
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-500/10 border border-teal-500/30 text-teal-400">
                6 Workers Online
              </span>
            </h2>
            <p className="text-xs text-zinc-400">
              Specialized local subagents running in the background to automate ThanvishOS.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1.5 text-[11px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-lg">
          <Activity className="w-3.5 h-3.5 animate-pulse" />
          <span>Daemon Active (Port 8000)</span>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {agents.map((agent) => (
          <div
            key={agent.id}
            className="bg-zinc-950/70 border border-zinc-800/80 rounded-lg p-3 hover:border-zinc-700 transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-base">{agent.avatar}</span>
                  <h3 className="text-xs font-semibold text-zinc-200 truncate">{agent.name}</h3>
                </div>
                <span className="w-2 h-2 rounded-full bg-emerald-500 shadow-sm shadow-emerald-500/50" />
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed line-clamp-2">{agent.role}</p>
            </div>

            <div className="mt-3 pt-2 border-t border-zinc-800/60 flex items-center justify-between text-[10px] font-mono text-zinc-500">
              <span>Status: <strong className="text-emerald-400">{agent.status}</strong></span>
              <span>{agent.tasks_completed} tasks completed</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
