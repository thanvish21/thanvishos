import React from "react";
import Header from "@/components/Header";
import TodayCommandCenter from "@/components/TodayCommandCenter";
import AttendanceRadar from "@/components/AttendanceRadar";
import SemesterExamRadar from "@/components/SemesterExamRadar";
import SrmMessRadar from "@/components/SrmMessRadar";
import Dropzone from "@/components/Dropzone";
import PolyglotGrid from "@/components/PolyglotGrid";
import SrmLibrary from "@/components/SrmLibrary";
import AppleMusicDock from "@/components/AppleMusicDock";
import AgentsMonitor from "@/components/AgentsMonitor";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 flex flex-col selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Universal Header (Live DO, Timetable, Exam Radar) */}
      <Header />

      {/* Main Dashboard Grid */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 pb-24 space-y-6">

        {/* Section 1: Today Command Center (Master Spec v4.0 Centerpiece) */}
        <TodayCommandCenter />

        {/* Section 2: Attendance Radar (90% Personal Target & What-If Engine) */}
        <AttendanceRadar />

        {/* Section 3: Semester Exam Radar & SRM Mess Radar */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <SemesterExamRadar />
          <SrmMessRadar />
        </div>

        {/* Section 4: Universal Dropzone & Apple Music Dock */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="flex flex-col h-full">
            <Dropzone />
          </div>
          <div className="flex flex-col h-full">
            <AppleMusicDock />
          </div>
        </div>

        {/* Section 5: Parallel Polyglot & Codédex Pro Matrix */}
        <PolyglotGrid />

        {/* Section 6: SRM Library OPAC Search & 10-Agent Telemetry Mesh */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="h-full min-h-[450px]">
            <SrmLibrary />
          </div>
          <div className="h-full min-h-[450px]">
            <AgentsMonitor />
          </div>
        </div>

      </main>
    </div>
  );
}
