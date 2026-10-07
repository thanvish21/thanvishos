"use client";

import React, { useState } from "react";
import { Search, Book, Library, Compass, Clock, CheckCircle2, Loader2, MapPin } from "lucide-react";

interface BookData {
  id: string;
  title: string;
  authors: string[];
  edition: string;
  call_number: string;
  copies_available: number;
  total_copies: number;
  pages: number;
  topics: string[];
  difficulty: string;
  est_mastery_hours: number;
  summary: string;
  is_online?: boolean;
}

interface RoadmapPhase {
  phase: string;
  weeks: string;
  hours: string;
  focus: string;
  action_items: string[];
}

interface MasteryRoadmap {
  topic: string;
  est_total_hours: number;
  weekly_commitment: number;
  est_weeks_to_master: number;
  phases: RoadmapPhase[];
  srm_central_library_tip: string;
}

export default function SrmLibrary() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<BookData[]>([]);

  const [roadmapLoading, setRoadmapLoading] = useState(false);
  const [activeRoadmap, setActiveRoadmap] = useState<MasteryRoadmap | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setActiveRoadmap(null);
    try {
      const res = await fetch("http://localhost:8000/api/library/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResults(data.books || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateRoadmap = async (topic: string, book_id?: string) => {
    setRoadmapLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/library/mastery", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, hours_per_week: 10, book_id }),
      });
      const data = await res.json();
      setActiveRoadmap(data);
    } catch (err) {
      console.error(err);
    } finally {
      setRoadmapLoading(false);
    }
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-2 pb-4 border-b border-zinc-800/80 mb-4">
        <div className="p-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
          <Library className="w-4 h-4" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
            SRM Central Library OPAC & Mastery Engine
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/30 text-indigo-400">
              Agent Navigator
            </span>
          </h2>
          <p className="text-xs text-zinc-400">
            Search physical textbooks in SRM Library, calculate mastery time, and generate learning roadmaps.
          </p>
        </div>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-zinc-500" />
          <input
            type="text"
            placeholder="Search topics (e.g. 'Bioinformatics', 'Algorithms', 'Operating Systems')..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-zinc-950/80 border border-zinc-800 rounded-lg pl-9 pr-3 py-2 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-indigo-500/50"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-zinc-800 hover:bg-zinc-700 text-zinc-200 px-4 py-2 rounded-lg text-sm font-medium transition border border-zinc-700 flex items-center gap-2"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
          <span>Search OPAC</span>
        </button>
      </form>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto">
        {/* State 1: Active Roadmap View */}
        {activeRoadmap ? (
          <div className="bg-zinc-950/50 border border-zinc-800/80 rounded-lg p-4 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-zinc-100">{activeRoadmap.topic}</h3>
                <div className="flex items-center gap-3 mt-1.5 text-xs font-mono">
                  <span className="text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                    {activeRoadmap.est_total_hours} Hours Total
                  </span>
                  <span className="text-zinc-400 bg-zinc-900 px-2 py-0.5 rounded border border-zinc-800">
                    {activeRoadmap.est_weeks_to_master} Weeks @ {activeRoadmap.weekly_commitment}h/wk
                  </span>
                </div>
              </div>
              <button
                onClick={() => setActiveRoadmap(null)}
                className="text-xs text-zinc-400 hover:text-zinc-200 underline underline-offset-2"
              >
                Back to results
              </button>
            </div>

            <div className="space-y-3 mt-4">
              {activeRoadmap.phases.map((phase, i) => (
                <div key={i} className="border border-zinc-800 rounded-lg p-3 bg-zinc-900/40">
                  <div className="flex items-center justify-between mb-1.5">
                    <h4 className="text-sm font-semibold text-zinc-200">{phase.phase}</h4>
                    <span className="text-[10px] font-mono text-zinc-500">{phase.weeks} ({phase.hours})</span>
                  </div>
                  <p className="text-xs text-zinc-400 mb-2">{phase.focus}</p>
                  <ul className="space-y-1">
                    {phase.action_items.map((item, j) => (
                      <li key={j} className="text-xs text-zinc-300 flex items-start gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500/70 mt-0.5 shrink-0" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            <div className="mt-4 p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-xs text-indigo-300 flex items-start gap-2">
              <MapPin className="w-4 h-4 shrink-0 mt-0.5" />
              <p>{activeRoadmap.srm_central_library_tip}</p>
            </div>
          </div>
        ) : (
          /* State 2: Search Results */
          <div className="space-y-3">
            {results.map((book) => (
              <div key={book.id} className="border border-zinc-800/80 rounded-lg p-3 bg-zinc-950/40 hover:bg-zinc-900/60 transition group">
                <div className="flex justify-between items-start gap-4">
                  <div className="flex-1">
                    <h3 className="text-sm font-semibold text-zinc-100 group-hover:text-indigo-400 transition">
                      {book.title}
                    </h3>
                    <p className="text-xs text-zinc-400 mt-0.5">
                      {book.authors.join(", ")} • {book.edition}
                    </p>

                    {/* Shelf Location Tag */}
                    <div className="mt-2 inline-flex items-center gap-1.5 bg-zinc-900 border border-zinc-800 px-2 py-1 rounded text-[10px] font-mono text-zinc-300">
                      <MapPin className="w-3 h-3 text-emerald-400" />
                      <span>{book.call_number}</span>
                    </div>

                    <p className="text-[11px] text-zinc-500 mt-2 line-clamp-2 leading-relaxed">
                      {book.summary}
                    </p>

                    <div className="flex items-center gap-2 mt-3 text-[10px] font-mono text-zinc-500">
                      <span className="px-1.5 py-0.5 bg-zinc-800 rounded">{book.difficulty}</span>
                      <span>•</span>
                      <span>{book.pages} pages</span>
                      {book.copies_available !== undefined && !book.is_online && (
                        <>
                          <span>•</span>
                          <span className={book.copies_available > 0 ? "text-emerald-400/80" : "text-red-400/80"}>
                            {book.copies_available}/{book.total_copies} available
                          </span>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Actions Column */}
                  <div className="flex flex-col items-end gap-2 shrink-0">
                    <button
                      onClick={() => generateRoadmap(book.title, book.id)}
                      disabled={roadmapLoading}
                      className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-zinc-800 text-zinc-100 px-3 py-1.5 rounded-lg text-xs font-semibold transition"
                    >
                      {roadmapLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Compass className="w-3.5 h-3.5" />}
                      <span>Generate Roadmap</span>
                    </button>
                    <div className="text-[10px] font-mono text-zinc-500 flex items-center gap-1 mt-1">
                      <Clock className="w-3 h-3" />
                      <span>Est. ~{book.est_mastery_hours}h</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {results.length === 0 && !loading && (
              <div className="text-center py-10 px-4">
                <Book className="w-8 h-8 text-zinc-700 mx-auto mb-3" />
                <p className="text-sm text-zinc-400">Search the SRM OPAC to find textbooks and generate learning roadmaps.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
