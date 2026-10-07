"use client";

import React, { useState } from "react";
import Header from "@/components/Header";
import { Terminal, Play, Flame, ArrowLeft, Sparkles } from "lucide-react";
import Link from "next/link";

export default function PolyglotPage() {
  const [selectedLang, setSelectedLang] = useState("Python");
  const [code, setCode] = useState(`def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test execution
print("Output:", two_sum([2, 7, 11, 15], 9))
`);
  const [output, setOutput] = useState<string | null>(null);

  const handleRun = () => {
    setOutput("Executing in Linux Sandbox...\n>>> Output: [0, 1]\n>>> All 3 test cases passed! (Time: 12ms, Space: O(n))");
  };

  return (
    <div className="min-h-screen bg-zinc-950 flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* Navigation & Header */}
        <div className="flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 text-xs font-mono text-zinc-400 hover:text-zinc-200 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to ThanvishOS Command Center</span>
          </Link>

          <div className="flex items-center gap-2 bg-amber-500/10 border border-amber-500/20 px-3 py-1 rounded-lg text-xs font-mono text-amber-300">
            <Flame className="w-4 h-4 text-orange-400" />
            <span>Codédex Pro Sprint • 82 Days Left</span>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Problem & SRM Course Sync */}
          <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Easy Warm-Up
              </span>
              <span className="text-xs font-mono text-zinc-500">CT1 Maths Warm-Up</span>
            </div>

            <div>
              <h2 className="text-base font-semibold text-zinc-100">Two Sum (Hashing & Arrays)</h2>
              <p className="text-xs text-zinc-400 mt-2 leading-relaxed">
                Given an array of integers <code className="text-zinc-300 font-mono">nums</code> and an integer <code className="text-zinc-300 font-mono">target</code>, return indices of the two numbers such that they add up to target.
              </p>
            </div>

            <div className="space-y-2 pt-2 border-t border-zinc-800/80">
              <h3 className="text-xs font-mono text-zinc-300 uppercase tracking-wider">Language Tracks</h3>
              <div className="flex flex-wrap gap-2">
                {["Python", "C / C++", "Java", "DSA", "Rust"].map((lang) => (
                  <button
                    key={lang}
                    onClick={() => setSelectedLang(lang)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-mono transition border ${
                      selectedLang === lang
                        ? "bg-cyan-500/20 text-cyan-300 border-cyan-500/40"
                        : "bg-zinc-950 border-zinc-800 text-zinc-400 hover:text-zinc-200"
                    }`}
                  >
                    {lang}
                  </button>
                ))}
              </div>
            </div>

            <div className="p-3 bg-zinc-950/80 border border-zinc-800 rounded-lg text-xs text-zinc-400 space-y-1.5 font-mono">
              <div className="font-semibold text-zinc-300 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                <span>SRM Lab Integration</span>
              </div>
              <p className="text-[11px]">
                Essential for PPS / C Programming and Semester 3 Data Structures course.
              </p>
            </div>
          </div>

          {/* Right: Coding Sandbox */}
          <div className="lg:col-span-2 bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 flex flex-col space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
              <div className="flex items-center gap-2 text-xs font-mono text-zinc-300">
                <Terminal className="w-4 h-4 text-cyan-400" />
                <span>Interactive Sandbox ({selectedLang})</span>
              </div>
              <button
                onClick={handleRun}
                className="flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-zinc-950 px-4 py-1.5 rounded-lg text-xs font-bold transition shadow-sm shadow-emerald-500/20"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Run Code</span>
              </button>
            </div>

            <textarea
              rows={12}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg p-3 text-xs text-cyan-300 font-mono focus:outline-none focus:border-cyan-500/50 resize-none"
            />

            {output && (
              <div className="bg-zinc-950 border border-zinc-800 rounded-lg p-3 text-xs font-mono text-emerald-400 whitespace-pre-wrap">
                {output}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
