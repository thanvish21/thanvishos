"use client";

import React, { useState, useEffect } from "react";
import { Calendar, Clock, AlertTriangle, Zap } from "lucide-react";

interface ScheduleData {
  date: string;
  day_order: string;
  title: string;
  energy: string;
  energy_badge: string;
  timetable: string;
  end_time: string;
  session_mode: string;
  nss_info: string;
  power_day: boolean;
  tomorrow: {
    date: string;
    day_order: string;
    energy: string;
    timetable: string;
  };
  exam_alert: {
    urgency: string;
    subject: string;
    time: string;
    message: string;
  } | null;
}

export default function Header() {
  const [schedule, setSchedule] = useState<ScheduleData | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/schedule/today")
      .then((res) => res.json())
      .then((data) => {
        setSchedule(data);
      })
      .catch((err) => {
        console.error("Failed to fetch schedule:", err);
        // Fallback local stub
        setSchedule({
          date: "2026-10-08",
          day_order: "DO3",
          title: "Day Order 3",
          energy: "LIGHT ✨ (Power Day)",
          energy_badge: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
          timetable: "Calculus (P4) + Chemistry (P5) — Done by 12:25 PM!",
          end_time: "12:25 PM",
          session_mode: "90 min Deep Engineering & Research Window",
          nss_info: "No NSS today",
          power_day: true,
          tomorrow: {
            date: "2026-10-09",
            day_order: "DO4",
            energy: "HEAVY",
            timetable: "Chemistry (P1–P2) + Calculus (P6–P7) + Chemistry (P8) + PPS (P9) + Calculus (P10)"
          },
          exam_alert: {
            urgency: "TOMORROW",
            subject: "Mathematics",
            time: "12:30 PM - 02:10 PM",
            message: "⚠️ EXAM ALERT: Mathematics CT1 is TOMORROW at 12:30 PM. Keep interview prep light and revise tonight."
          }
        });
      });
  }, []);

  return (
    <header className="border-b border-zinc-800/80 bg-zinc-950/90 backdrop-blur-md sticky top-0 z-40">
      {/* Top Banner: Exam Alert if active */}
      {schedule?.exam_alert && (
        <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 text-xs font-mono text-amber-300 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400 animate-pulse" />
            <span className="font-semibold tracking-wide">{schedule.exam_alert.message}</span>
          </div>
          <span className="hidden sm:inline bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-500/30 text-[10px]">
            CT1 RADAR
          </span>
        </div>
      )}

      {/* Main Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Identity & Core Status */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-mono font-bold text-lg shadow-sm shadow-cyan-500/10">
            T
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-semibold tracking-tight text-zinc-100">ThanvishOS</h1>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-zinc-900 border border-zinc-700 text-zinc-400">
                v2.4
              </span>
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" title="System Online" />
            </div>
            <p className="text-xs text-zinc-400 font-mono">
              SRM CS + Computational Biology • <span className="text-zinc-300">RA2611027010109</span>
            </p>
          </div>
        </div>

        {/* Day Order & Energy Telemetry Card */}
        {schedule && (
          <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs font-mono">
            {/* DO Badge */}
            <div className="flex items-center gap-1.5 bg-zinc-900 border border-zinc-800 px-3 py-1.5 rounded-lg">
              <Calendar className="w-3.5 h-3.5 text-zinc-400" />
              <span className="text-zinc-400">SRM DAY:</span>
              <span className="font-bold text-cyan-400 bg-cyan-500/10 px-1.5 py-0.5 rounded border border-cyan-500/20">
                {schedule.day_order}
              </span>
            </div>

            {/* Energy Level */}
            <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium ${schedule.energy_badge}`}>
              <Zap className="w-3.5 h-3.5" />
              <span>{schedule.energy}</span>
            </div>

            {/* Timetable / Done Time */}
            <div className="flex items-center gap-1.5 bg-zinc-900/80 border border-zinc-800 px-3 py-1.5 rounded-lg text-zinc-300">
              <Clock className="w-3.5 h-3.5 text-zinc-400" />
              <span>Classes end: <strong className="text-zinc-100">{schedule.end_time}</strong></span>
            </div>

            {/* Tomorrow Preview Pill */}
            <div className="hidden lg:flex items-center gap-1.5 bg-zinc-900/50 border border-zinc-800/80 px-2.5 py-1.5 rounded-lg text-[11px] text-zinc-400">
              <span>Tomorrow: <strong className="text-zinc-300">{schedule.tomorrow.day_order}</strong> ({schedule.tomorrow.energy})</span>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
