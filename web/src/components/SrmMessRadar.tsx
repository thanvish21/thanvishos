"use client";

import React, { useState, useEffect } from "react";
import { Utensils, AlertCircle } from "lucide-react";

interface MessTimings {
  breakfast: string;
  lunch: string;
  snacks: string;
  dinner: string;
}

interface MessResponse {
  status: string;
  message: string;
  timings: MessTimings;
  constraint_note?: string | null;
}

export default function SrmMessRadar() {
  const [mess, setMess] = useState<MessResponse | null>(null);

  useEffect(() => {
    fetch("/api/mess/today")
      .then(res => res.json())
      .then(data => setMess(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm flex flex-col h-full">
      <div className="flex items-center justify-between pb-4 border-b border-zinc-800/80 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400">
            <Utensils className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              SRM Mess &amp; Food Radar
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">
                {mess?.status || "AWAITING SYNC"}
              </span>
            </h2>
            <p className="text-xs text-zinc-400">Meal Timings &amp; Exam Overlap Constraints</p>
          </div>
        </div>
      </div>

      <div className="space-y-3 flex-1">
        <div className="grid grid-cols-2 gap-2 text-xs font-mono">
          <div className="p-2.5 bg-zinc-950/40 border border-zinc-800/80 rounded-lg">
            <span className="text-zinc-500 block text-[10px]">BREAKFAST</span>
            <span className="text-zinc-200 font-semibold">{mess?.timings?.breakfast || "07:30–09:00"}</span>
          </div>
          <div className="p-2.5 bg-zinc-950/40 border border-zinc-800/80 rounded-lg">
            <span className="text-zinc-500 block text-[10px]">LUNCH</span>
            <span className="text-zinc-200 font-semibold">{mess?.timings?.lunch || "12:30–14:00"}</span>
          </div>
          <div className="p-2.5 bg-zinc-950/40 border border-zinc-800/80 rounded-lg">
            <span className="text-zinc-500 block text-[10px]">SNACKS</span>
            <span className="text-zinc-200 font-semibold">{mess?.timings?.snacks || "16:30–17:30"}</span>
          </div>
          <div className="p-2.5 bg-zinc-950/40 border border-zinc-800/80 rounded-lg">
            <span className="text-zinc-500 block text-[10px]">DINNER</span>
            <span className="text-zinc-200 font-semibold">{mess?.timings?.dinner || "19:30–21:00"}</span>
          </div>
        </div>

        {mess?.constraint_note && (
          <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300 flex items-start gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <p>{mess.constraint_note}</p>
          </div>
        )}

        <div className="p-3 bg-zinc-950/60 border border-zinc-800/80 rounded-lg text-center">
          <p className="text-xs text-zinc-400 font-mono">
            {mess?.message || "Mess menu unavailable — upload hostel menu PDF/text in Brain Dump."}
          </p>
        </div>
      </div>
    </div>
  );
}
