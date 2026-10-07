"use client";

import React, { useState, useEffect } from "react";
import { ShieldCheck, Calculator, RefreshCw } from "lucide-react";

interface AttendanceRecord {
  code: string;
  title: string;
  classes_conducted: number;
  classes_attended: number;
  percentage: number;
  risk_status: string;
}

interface AttendanceSummary {
  records: AttendanceRecord[];
}

interface SimulationResult {
  current_percentage: number;
  projected_percentage: number;
  classes_needed_for_90: number;
}

export default function AttendanceRadar() {
  const [summary, setSummary] = useState<AttendanceSummary | null>(null);
  const [loading, setLoading] = useState(true);

  // What-If Simulator State
  const [selectedCourse, setSelectedCourse] = useState<string>("");
  const [missCount, setMissCount] = useState<number>(0);
  const [attendCount, setAttendCount] = useState<number>(0);
  const [simResult, setSimResult] = useState<SimulationResult | null>(null);

  const fetchSummary = () => {
    setLoading(true);
    fetch("http://localhost:8000/api/attendance/summary")
      .then(res => res.json())
      .then(data => {
        setSummary(data);
        if (data.records && data.records.length > 0) {
          setSelectedCourse(data.records[0].code);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const handleSimulate = (course: string, miss: number, attend: number) => {
    if (!course) return;
    fetch("http://localhost:8000/api/attendance/what-if", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ course_code: course, miss_count: miss, attend_count: attend })
    })
      .then(res => res.json())
      .then(data => setSimResult(data))
      .catch(err => console.error(err));
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between pb-4 border-b border-zinc-800/80 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              Attendance Radar
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                Target: &gt;= 90%
              </span>
            </h2>
            <p className="text-xs text-zinc-400">Strict Personal Requirement (Min. 90% in every subject)</p>
          </div>
        </div>
        <button onClick={fetchSummary} className="p-1.5 rounded-lg bg-zinc-800 text-zinc-400 hover:text-zinc-200">
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Current Attendance Table */}
        <div className="space-y-2 overflow-y-auto max-h-[300px]">
          {summary?.records?.map((record) => {
            const isSafe = record.percentage >= 90;
            return (
              <div
                key={record.code}
                onClick={() => {
                  setSelectedCourse(record.code);
                  handleSimulate(record.code, missCount, attendCount);
                }}
                className={`p-3 rounded-lg border flex items-center justify-between cursor-pointer transition ${
                  selectedCourse === record.code ? 'bg-zinc-800/80 border-indigo-500/50' : 'bg-zinc-950/40 border-zinc-800/80 hover:border-zinc-700'
                }`}
              >
                <div>
                  <h4 className="text-xs font-semibold text-zinc-200">{record.title}</h4>
                  <div className="text-[10px] font-mono text-zinc-500 mt-0.5">
                    {record.code} • {record.classes_attended}/{record.classes_conducted} classes
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs font-mono font-bold ${isSafe ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {record.percentage}%
                  </span>
                  <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded border ${
                    isSafe ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                  }`}>
                    {record.risk_status}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Right: What-If Simulator */}
        <div className="p-4 bg-zinc-950/60 border border-zinc-800 rounded-lg flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-semibold text-zinc-200 mb-3 flex items-center gap-1.5">
              <Calculator className="w-3.5 h-3.5 text-indigo-400" />
              What-If Projection Engine ({selectedCourse || "Select a subject"})
            </h3>

            <div className="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label className="text-[10px] font-mono text-zinc-400 block mb-1">If I miss next (N) classes:</label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={missCount}
                  onChange={(e) => {
                    const val = parseInt(e.target.value) || 0;
                    setMissCount(val);
                    handleSimulate(selectedCourse, val, attendCount);
                  }}
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-lg p-1.5 text-xs text-zinc-200 font-mono"
                />
              </div>

              <div>
                <label className="text-[10px] font-mono text-zinc-400 block mb-1">If I attend next (N) classes:</label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={attendCount}
                  onChange={(e) => {
                    const val = parseInt(e.target.value) || 0;
                    setAttendCount(val);
                    handleSimulate(selectedCourse, missCount, val);
                  }}
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-lg p-1.5 text-xs text-zinc-200 font-mono"
                />
              </div>
            </div>

            {simResult && (
              <div className="space-y-2 border-t border-zinc-800/80 pt-3">
                <div className="flex justify-between text-xs font-mono">
                  <span className="text-zinc-400">Current Attendance:</span>
                  <span className="text-zinc-200 font-bold">{simResult.current_percentage}%</span>
                </div>
                <div className="flex justify-between text-xs font-mono">
                  <span className="text-zinc-400">Projected Attendance:</span>
                  <span className={`font-bold ${simResult.projected_percentage >= 90 ? 'text-emerald-400' : 'text-red-400'}`}>
                    {simResult.projected_percentage}%
                  </span>
                </div>
                <div className="text-[11px] text-zinc-400 pt-1">
                  Classes needed to secure &gt;=90%: <strong className="text-indigo-400">{simResult.classes_needed_for_90} classes</strong>
                </div>
              </div>
            )}
          </div>

          <div className="text-[10px] font-mono text-zinc-500 pt-2 border-t border-zinc-800/40 mt-3">
            Simulations are projections based on the formula (attended + N) / (conducted + N).
          </div>
        </div>
      </div>
    </div>
  );
}
