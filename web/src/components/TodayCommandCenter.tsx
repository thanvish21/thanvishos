"use client";

import React, { useState, useEffect } from "react";
import { AlertCircle, Calendar, ShieldAlert, Target, Moon, MapPin, XCircle } from "lucide-react";

interface ClassSession {
  period: string;
  subject: string;
  type: string;
}

interface ExamRadarItem {
  subject: string;
  urgency: string;
  category: string;
}

interface AttendanceRiskItem {
  course: string;
  percentage: number;
}

interface TodayPlan {
  academic_priority: string;
  technical_learning: string;
  building_goal: string;
  why_these_priorities: string;
  what_not_to_do: string;
  free_time_windows: {
    summary: string;
    evening_wind_down: string;
  };
}

interface CommandCenterData {
  date: string;
  weekday: string;
  day_order: string;
  working_status: string;
  classes: ClassSession[];
  exam_radar: ExamRadarItem[];
  attendance_risks: AttendanceRiskItem[];
  today_plan: TodayPlan;
}

export default function TodayCommandCenter() {
  const [data, setData] = useState<CommandCenterData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/planner/today")
      .then(res => res.json())
      .then(resData => {
        setData(resData);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="h-64 bg-zinc-900/50 rounded-xl animate-pulse"></div>;
  if (!data) return null;

  return (
    <div className="bg-zinc-950/80 border border-zinc-800 rounded-xl shadow-2xl overflow-hidden backdrop-blur-md">
      {/* Top Bar: Date & DO Status */}
      <div className="flex flex-wrap items-center justify-between p-5 border-b border-zinc-800/80 bg-zinc-900/50">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-indigo-500/10 border border-indigo-500/30 rounded-xl flex items-center justify-center">
            <span className="font-mono font-bold text-xl text-indigo-400">{data.day_order.replace('DO', '')}</span>
          </div>
          <div>
            <h2 className="text-xl font-bold text-zinc-100 uppercase tracking-wide">
              {data.date} • {data.weekday}
            </h2>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs font-mono text-zinc-400">SRM DAY ORDER: {data.day_order}</span>
              {data.working_status === "WORKING" ? (
                <span className="text-[10px] bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded border border-emerald-500/20">CLASSES</span>
              ) : (
                <span className="text-[10px] bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded border border-purple-500/20">HOLIDAY</span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-0 divide-y lg:divide-y-0 lg:divide-x divide-zinc-800/80">

        {/* Left Column: Schedule & Exams */}
        <div className="p-5 space-y-6">
          <div>
            <h3 className="text-xs font-mono text-zinc-500 mb-3 flex items-center gap-2">
              <Calendar className="w-3.5 h-3.5" /> TODAY&apos;S SCHEDULE
            </h3>
            <ul className="space-y-2">
              {data.classes.map((cls, i) => (
                <li key={i} className="flex justify-between items-center text-sm border-b border-zinc-800/50 pb-1">
                  <span className="font-mono text-zinc-400 text-xs">{cls.period}</span>
                  <span className={`font-semibold ${cls.type === 'FREE' ? 'text-zinc-500' : 'text-zinc-200'}`}>{cls.subject}</span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-xs font-mono text-zinc-500 mb-3 flex items-center gap-2">
              <ShieldAlert className="w-3.5 h-3.5" /> EXAM RADAR
            </h3>
            {data.exam_radar.length > 0 ? (
              <div className="space-y-2">
                {data.exam_radar.map((exam, i) => (
                  <div key={i} className={`p-3 rounded-lg border ${exam.urgency === 'TOMORROW' ? 'bg-amber-500/10 border-amber-500/30' : 'bg-indigo-500/10 border-indigo-500/20'}`}>
                    <div className="flex justify-between items-start">
                      <span className={`text-sm font-bold ${exam.urgency === 'TOMORROW' ? 'text-amber-400' : 'text-indigo-400'}`}>{exam.subject}</span>
                      <span className="text-[10px] font-mono bg-zinc-950 px-1.5 py-0.5 rounded border border-zinc-800 text-zinc-300">{exam.urgency}</span>
                    </div>
                    <p className="text-[11px] text-zinc-400 mt-1">Category: {exam.category}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-zinc-500 bg-zinc-900/40 p-3 rounded-lg border border-zinc-800">No imminent exams detected.</div>
            )}
          </div>
        </div>

        {/* Middle Column: Academic & Technical Priorities */}
        <div className="p-5 space-y-6">
          <div>
            <h3 className="text-xs font-mono text-zinc-500 mb-3 flex items-center gap-2">
              <Target className="w-3.5 h-3.5" /> WHAT MATTERS TODAY
            </h3>

            <div className="space-y-4">
              <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg">
                <span className="text-[10px] text-zinc-500 uppercase tracking-wider block mb-1">Academic Priority</span>
                <p className="text-sm text-zinc-100 font-semibold">{data.today_plan.academic_priority}</p>
              </div>

              <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg">
                <span className="text-[10px] text-zinc-500 uppercase tracking-wider block mb-1">Technical Learning</span>
                <p className="text-sm text-zinc-100 font-semibold">{data.today_plan.technical_learning}</p>
              </div>

              <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg">
                <span className="text-[10px] text-zinc-500 uppercase tracking-wider block mb-1">Project Milestone</span>
                <p className="text-sm text-zinc-100 font-semibold">{data.today_plan.building_goal}</p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-indigo-500/5 border border-indigo-500/20 rounded-xl">
            <h4 className="text-xs font-bold text-indigo-400 mb-1 flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5" /> Why these priorities?
            </h4>
            <p className="text-[11px] leading-relaxed text-indigo-200/70">{data.today_plan.why_these_priorities}</p>
          </div>
        </div>

        {/* Right Column: Constraints & Free Time */}
        <div className="p-5 space-y-6">
          <div className="p-4 bg-red-500/5 border border-red-500/20 rounded-xl">
            <h3 className="text-xs font-bold text-red-400 mb-2 flex items-center gap-1.5">
              <XCircle className="w-3.5 h-3.5" /> WHAT NOT TO DO TODAY
            </h3>
            <p className="text-sm text-zinc-200 font-medium leading-relaxed">{data.today_plan.what_not_to_do}</p>
          </div>

          <div>
            <h3 className="text-xs font-mono text-zinc-500 mb-3 flex items-center gap-2">
              <AlertCircle className="w-3.5 h-3.5" /> ATTENDANCE RISK
            </h3>
            {data.attendance_risks.length > 0 ? (
              <div className="space-y-2">
                {data.attendance_risks.map((risk, i) => (
                  <div key={i} className="flex justify-between items-center text-sm p-2 bg-zinc-900 border border-zinc-800 rounded-lg">
                    <span className="text-zinc-200">{risk.course}</span>
                    <span className="font-mono font-bold text-red-400">{risk.percentage}%</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-[11px] font-mono text-zinc-500">No critical attendance drops detected (All safe &gt;=90%).</div>
            )}
          </div>

          <div>
            <h3 className="text-xs font-mono text-zinc-500 mb-3 flex items-center gap-2">
              <Moon className="w-3.5 h-3.5" /> FREE TIME / RELAXATION
            </h3>
            <div className="p-3 bg-zinc-900/40 border border-zinc-800 rounded-lg">
              <p className="text-sm text-zinc-300 mb-2">{data.today_plan.free_time_windows.summary}</p>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-1 rounded">
                Recommended Wind-down: {data.today_plan.free_time_windows.evening_wind_down}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
