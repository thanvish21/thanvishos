"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/Header";
import { Brain, AlertTriangle, ArrowLeft, Target, RefreshCw } from "lucide-react";
import Link from "next/link";

interface Question {
  id: string;
  level_name: string;
  format: string;
  question: string;
}

interface TestData {
  topic: string;
  questions: Question[];
}

interface TestResult {
  overall_score: number;
  scores: Record<string, string>;
  strongest_area: string;
  weakest_area: string;
  weaknesses_identified: Array<{ topic: string; issue: string; retest_in_days: number }>;
  next_action: string;
}

export default function AdaptiveTestPage() {
  const [test, setTest] = useState<TestData | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<TestResult | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setTest({
      topic: "Calculus & Mathematics CT1",
      questions: [
        {
          id: "calc-l1-01",
          level_name: "Level 1 — Concept + Foundation",
          format: "CONCEPT_EXPLANATION",
          question: "Explain conceptually: What does it mean for a function f(x) to be continuous at x = a, and what are the three mathematical conditions required?",
        },
        {
          id: "calc-l1-02",
          level_name: "Level 1 — Concept + Foundation",
          format: "MCQ_WITH_WHY",
          question: "A square matrix A has det(A) = 0. Which of the following is true, and WHY?\n\nA. The matrix is invertible\nB. The system Ax = 0 has only the trivial solution\nC. The rows/columns of A are linearly dependent\nD. The rank of A equals n",
        },
        {
          id: "calc-l2-02",
          level_name: "Level 2 — Engineering & Problem Solving",
          format: "DEBUGGING",
          question: "A student claims: 'To find the absolute maximum of f(x) on [a, b], we just solve f'(x) = 0 and pick the largest x value.' What is flawed with this reasoning, and what must be checked?",
        },
        {
          id: "calc-l3-01",
          level_name: "Level 3 — Critical Thinking & Transfer",
          format: "REAL_WORLD_SCENARIO",
          question: "In Machine Learning, we optimize a loss function L(w) using gradient descent: w = w - alpha * grad(L). If the function has an ill-conditioned Hessian (high curvature in one direction, flat in another), what happens to standard gradient descent, and how does momentum address this?",
        }
      ]
    });
  }, []);

  const handleSubmit = async () => {
    setSubmitting(true);
    setTimeout(() => {
      setResult({
        overall_score: 82,
        scores: {
          "Conceptual Understanding": "95%",
          "Practical & Coding Ability": "80%",
          "Debugging": "65%",
          "Critical Thinking & Transfer": "88%"
        },
        strongest_area: "Conceptual Depth",
        weakest_area: "Debugging & Edge Cases",
        weaknesses_identified: [
          { topic: "Calculus: Critical Points & Optimization", issue: "Missed checking boundary conditions [a,b] for absolute extrema", retest_in_days: 2 }
        ],
        next_action: "Mathematics CT1 revision on formulas & derivatives before tomorrow's exam."
      });
      setSubmitting(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-zinc-950 flex flex-col">
      <Header />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* Navigation & Header */}
        <div className="flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 text-xs font-mono text-zinc-400 hover:text-zinc-200 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </Link>
          <div className="flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 rounded-lg text-xs font-mono text-indigo-300">
            <Brain className="w-4 h-4 text-indigo-400" />
            <span>Daily Mastery Evaluation</span>
          </div>
        </div>

        {!result ? (
          <div className="space-y-6">
            <div className="border-b border-zinc-800 pb-4">
              <h1 className="text-xl font-bold text-zinc-100">{test?.topic}</h1>
              <p className="text-sm text-zinc-400 mt-1">Multi-Format Adaptive Testing Engine • 3 Levels</p>
            </div>

            {test?.questions.map((q) => (
              <div key={q.id} className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80">
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-zinc-800 text-cyan-300 border border-zinc-700">
                    {q.format}
                  </span>
                  <span className="text-xs font-semibold text-zinc-400">{q.level_name}</span>
                </div>
                <div className="text-sm text-zinc-200 font-medium whitespace-pre-wrap leading-relaxed">
                  {q.question}
                </div>
                <textarea
                  rows={4}
                  placeholder="Enter your reasoning and answer..."
                  value={answers[q.id] || ""}
                  onChange={(e) => setAnswers({ ...answers, [q.id]: e.target.value })}
                  className="w-full bg-zinc-950/80 border border-zinc-800 rounded-lg p-3 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-cyan-500/50 resize-y"
                />
              </div>
            ))}

            <div className="flex justify-end pt-4">
              <button
                onClick={handleSubmit}
                disabled={submitting}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-zinc-800 text-zinc-100 px-6 py-2.5 rounded-lg text-sm font-semibold transition"
              >
                {submitting ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Target className="w-4 h-4" />}
                <span>Evaluate Mastery</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-6">
              <div className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8 border-b border-zinc-800 pb-6">
                <div>
                  <h2 className="text-2xl font-bold text-zinc-100">Evaluation Complete</h2>
                  <p className="text-sm text-zinc-400 mt-1">Multi-Dimensional Score Breakdown</p>
                </div>
                <div className="w-24 h-24 rounded-full border-4 border-emerald-500/30 flex items-center justify-center bg-emerald-500/10 shadow-lg shadow-emerald-500/20">
                  <span className="text-3xl font-bold text-emerald-400">{result.overall_score}%</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="space-y-3">
                  {Object.entries(result.scores).map(([dim, score]) => (
                    <div key={dim} className="flex items-center justify-between text-sm">
                      <span className="text-zinc-400">{dim}</span>
                      <span className="font-mono text-zinc-200">{score}</span>
                    </div>
                  ))}
                </div>
                <div className="space-y-4">
                  <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                    <div className="text-[11px] font-mono text-emerald-500 uppercase tracking-wider mb-1">Strongest Area</div>
                    <div className="text-sm text-zinc-200 font-semibold">{result.strongest_area}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                    <div className="text-[11px] font-mono text-red-500 uppercase tracking-wider mb-1">Weakest Area</div>
                    <div className="text-sm text-zinc-200 font-semibold">{result.weakest_area}</div>
                  </div>
                </div>
              </div>

              {result.weaknesses_identified.length > 0 && (
                <div className="mt-6 pt-6 border-t border-zinc-800">
                  <h3 className="text-sm font-semibold text-zinc-200 mb-3 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    <span>Concepts to Retest</span>
                  </h3>
                  <div className="space-y-2">
                    {result.weaknesses_identified.map((w, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 bg-zinc-950 rounded-lg border border-zinc-800/80 text-sm text-zinc-400">
                        <span className="bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded border border-amber-500/20 text-[10px] font-mono shrink-0 mt-0.5">
                          RETEST IN {w.retest_in_days}D
                        </span>
                        <span>{w.topic}: <span className="text-zinc-300">{w.issue}</span></span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-6 p-4 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-sm text-indigo-200">
                <strong className="text-indigo-400 block mb-1">Next Action:</strong>
                {result.next_action}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
