"use client";

import React, { useState, useEffect } from "react";
import { Code2, Flame, Terminal, ChevronRight } from "lucide-react";

interface LanguageProgress {
  name: string;
  role: string;
  progress: number;
  color: string;
}

interface PolyglotData {
  codedex_pro_sprint: {
    expires_in_days: number;
    days_completed: number;
    streak: number;
    progress_percent: number;
  };
  languages: LanguageProgress[];
}

export default function PolyglotGrid() {
  const [data, setData] = useState<PolyglotData | null>(null);

  useEffect(() => {
    fetch("/api/polyglot/status")
      .then((res) => res.json())
      .then((resData) => setData(resData))
      .catch(() => {
        // Local stub
        setData({
          codedex_pro_sprint: {
            expires_in_days: 82,
            days_completed: 108,
            streak: 14,
            progress_percent: 62,
          },
          languages: [
            { name: "Python", role: "AI & CompBio", progress: 75, color: "bg-emerald-500" },
            { name: "C / C++", role: "Systems & DSA", progress: 45, color: "bg-blue-500" },
            { name: "Java", role: "Enterprise Backend", progress: 30, color: "bg-orange-500" },
            { name: "DSA", role: "Interview Core", progress: 55, color: "bg-purple-500" },
            { name: "Rust", role: "Modern Systems", progress: 15, color: "bg-rose-500" },
          ],
        });
      });
  }, []);

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <Code2 className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              Parallel Polyglot Mastery Matrix
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                Active Sprint
              </span>
            </h2>
            <p className="text-xs text-zinc-400">
              Parallel skill building across C, Python, Java & DSA with Codédex Pro 3-Month accelerator.
            </p>
          </div>
        </div>

        {/* Codédex Pro Badge */}
        {data && (
          <div className="flex items-center gap-2 bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-amber-500/20 px-3 py-1.5 rounded-lg text-xs font-mono text-amber-300">
            <Flame className="w-4 h-4 text-orange-400 fill-orange-400" />
            <span>
              <strong>{data.codedex_pro_sprint.expires_in_days} Days</strong> left on Pro Perk
            </span>
          </div>
        )}
      </div>

      {/* Language Tracks Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {data?.languages.map((lang) => (
          <div
            key={lang.name}
            className="bg-zinc-950/70 border border-zinc-800/80 rounded-lg p-3 hover:border-zinc-700 transition"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-semibold text-zinc-200">{lang.name}</span>
              <span className="text-[10px] font-mono text-zinc-400">{lang.progress}%</span>
            </div>
            <div className="text-[10px] text-zinc-500 font-mono mb-2 truncate">{lang.role}</div>
            {/* Progress Bar */}
            <div className="w-full h-1.5 bg-zinc-800 rounded-full overflow-hidden">
              <div
                className={`h-full ${lang.color} rounded-full transition-all duration-500`}
                style={{ width: `${lang.progress}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Daily Challenge Banner */}
      <div className="mt-4 p-3 rounded-lg bg-zinc-950/80 border border-zinc-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded bg-cyan-500/10 text-cyan-400 font-mono font-bold">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <div className="text-zinc-200 font-semibold flex items-center gap-2">
              Tonight&apos;s Focus: <span className="text-cyan-300">Two Sum & Hash Map Mastery</span>
            </div>
            <p className="text-[11px] text-zinc-400 font-mono">
              Synchronized with evening interview prep & CT1 Mathematics exam warm-up.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <a
            href="/test"
            className="flex items-center gap-1.5 bg-indigo-600/90 hover:bg-indigo-600 text-zinc-100 font-mono text-[11px] font-semibold px-3 py-1.5 rounded-lg transition shrink-0"
          >
            <span>Launch 3-Level Test</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </a>
          <a
            href="/polyglot"
            className="flex items-center gap-1 text-cyan-400 hover:text-cyan-300 font-mono text-[11px] font-medium shrink-0"
          >
            <span>Coding Sandbox</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
}
