import React from "react";
import Header from "@/components/Header";
import Dropzone from "@/components/Dropzone";
import SrmLibrary from "@/components/SrmLibrary";
import PolyglotGrid from "@/components/PolyglotGrid";
import AppleMusicDock from "@/components/AppleMusicDock";
import AgentsMonitor from "@/components/AgentsMonitor";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 flex flex-col">
      {/* Universal Header (Live DO, Timetable, Exam Radar) */}
      <Header />

      {/* Main Dashboard Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 pb-24 space-y-6">

        {/* Top Section: Split Universal Dropzone & Apple Music Dock */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="flex flex-col h-full">
            <Dropzone />
          </div>
          <div className="flex flex-col h-full">
            <AppleMusicDock />
          </div>
        </div>

        {/* Middle Section: Parallel Polyglot Tracker & Codédex Pro */}
        <PolyglotGrid />

        {/* Lower Section: Split SRM Library / Mastery & Agents Monitor */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="h-[450px]">
            <SrmLibrary />
          </div>
          <div className="h-auto">
            <AgentsMonitor />
          </div>
        </div>

      </main>
    </div>
  );
}
