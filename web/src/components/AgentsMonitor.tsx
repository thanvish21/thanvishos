"use client";

import React, { useState, useEffect } from "react";
import { Activity, ShieldAlert, CheckCircle2, Clock } from "lucide-react";

interface AgentTelemetry {
  id: string;
  name: string;
  avatar: string;
  role: string;
  status: string;
  success_count: number;
  failure_count: number;
  last_started: string | null;
}

export default function AgentsMonitor() {
  const [agents, setAgents] = useState<AgentTelemetry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/agents/telemetry")
      .then(res => res.json())
      .then(data => {
        setAgents(data.agents || []);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm h-full flex flex-col">
      <div className="flex items-center justify-between pb-4 border-b border-zinc-800/80 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-teal-500/10 border border-teal-500/20 text-teal-400">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              Autonomous 10-Agent Mesh
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-500/10 border border-teal-500/30 text-teal-400">
                {agents.filter(a => a.status === 'RUNNING' || a.status === 'ONLINE').length} Active
              </span>
            </h2>
            <p className="text-xs text-zinc-400">Live Database Telemetry &amp; Verification Auditor</p>
          </div>
        </div>
      </div>

      <div className="space-y-3 overflow-y-auto flex-1 pr-1 custom-scrollbar">
        {loading ? (
          <div className="animate-pulse space-y-3">
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="h-16 bg-zinc-950/50 rounded-lg"></div>
            ))}
          </div>
        ) : (
          agents.map(agent => {
            const isOnline = agent.status === "ONLINE" || agent.status === "RUNNING";
            const isAuditor = agent.id === "agent-verification-auditor";

            return (
              <div key={agent.id} className="p-3 bg-zinc-950/40 border border-zinc-800/80 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{agent.avatar}</span>
                    <div>
                      <h3 className={`text-xs font-semibold ${isAuditor ? 'text-teal-400' : 'text-zinc-200'}`}>
                        {agent.name}
                      </h3>
                      <p className="text-[10px] text-zinc-500 font-mono mt-0.5">{agent.id}</p>
                    </div>
                  </div>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                    isOnline ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-zinc-800 text-zinc-400 border-zinc-700'
                  }`}>
                    {agent.status}
                  </span>
                </div>

                <p className="text-[11px] text-zinc-400 leading-relaxed mb-2 line-clamp-2">
                  {agent.role}
                </p>

                <div className="flex items-center justify-between text-[10px] font-mono pt-2 border-t border-zinc-800/50">
                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1 text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" /> {agent.success_count} runs
                    </span>
                    {agent.failure_count > 0 && (
                      <span className="flex items-center gap-1 text-red-400">
                        <ShieldAlert className="w-3 h-3" /> {agent.failure_count} errors
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-1 text-zinc-500">
                    <Clock className="w-3 h-3" />
                    {agent.last_started ? new Date(agent.last_started).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : "Never"}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
