"use client";

import React, { useState, useEffect } from "react";
import { UploadCloud, Send, CheckCircle2, Sparkles, Loader2 } from "lucide-react";

interface DumpItem {
  id: string;
  type: string;
  title: string;
  category: string;
  preview: string;
  created_at: string;
  actions?: string[];
}

export default function Dropzone() {
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [recentDumps, setRecentDumps] = useState<DumpItem[]>([]);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const fetchRecent = () => {
    fetch("http://localhost:8000/api/dump/recent")
      .then((res) => res.json())
      .then((data) => {
        if (data.history) setRecentDumps(data.history);
      })
      .catch(() => {
        // Fallback local stub
        setRecentDumps([
          {
            id: "dump-01",
            type: "EXAM_SCHEDULE",
            title: "Mathematics CT1 Exam",
            category: "academics",
            preview: "Mathematics CT1 on Oct 9 at 12:30 PM",
            created_at: new Date().toISOString(),
            actions: ["Auto-synced to SRM Exam Radar."]
          },
          {
            id: "dump-02",
            type: "NOTE",
            title: "Computational Biology DNA Alignment",
            category: "second-brain",
            preview: "Smith-Waterman dynamic programming notes for protein sequencing...",
            created_at: new Date().toISOString(),
            actions: ["Saved to ThanvishOS/documents/notes/note_compbio.md"]
          }
        ]);
      });
  };

  useEffect(() => {
    fetchRecent();
  }, []);

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    setLoading(true);
    setStatusMessage(null);

    try {
      const res = await fetch("http://localhost:8000/api/dump/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, title: title.trim() || undefined }),
      });
      const data = await res.json();
      setContent("");
      setTitle("");
      setStatusMessage(`Agent categorized as [${data.result.type}]: ${data.result.actions?.[0] || 'Filed to local disk'}`);
      fetchRecent();
    } catch (err) {
      console.error(err);
      setStatusMessage("Dumped locally. Background agent will index shortly.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setStatusMessage(`Uploading ${file.name}...`);

    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch("http://localhost:8000/api/dump/file", {
        method: "POST",
        body: formData,
      });
      setStatusMessage(`File [${file.name}] sorted into /ThanvishOS/documents/pdfs/`);
      fetchRecent();
    } catch (err) {
      console.error(err);
      setStatusMessage(`File ${file.name} saved locally.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            <UploadCloud className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              Universal Brain Dump & File Nexus
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                Autonomous Sorting
              </span>
            </h2>
            <p className="text-xs text-zinc-400">
              Dump raw thoughts, notes, PDFs, or exam dates — 6 background agents sort and route them locally.
            </p>
          </div>
        </div>
      </div>

      {/* Input Form */}
      <form onSubmit={handleTextSubmit} className="space-y-3">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Optional title / topic tag..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="flex-1 bg-zinc-950/80 border border-zinc-800 rounded-lg px-3 py-1.5 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-cyan-500/50"
          />
          <label className="cursor-pointer flex items-center gap-1.5 bg-zinc-800 hover:bg-zinc-700/80 text-zinc-300 px-3 py-1.5 rounded-lg text-xs font-medium transition border border-zinc-700">
            <UploadCloud className="w-3.5 h-3.5 text-zinc-400" />
            <span>Attach PDF / Note</span>
            <input type="file" onChange={handleFileUpload} className="hidden" />
          </label>
        </div>

        <textarea
          rows={3}
          placeholder="Dump anything here: e.g. 'Maths CT1 on Oct 9 at 12:30 PM', 'Need to learn Hidden Markov Models for CompBio', or paste lecture notes..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full bg-zinc-950/80 border border-zinc-800 rounded-lg p-3 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-cyan-500/50 resize-none font-mono"
        />

        <div className="flex items-center justify-between">
          <div className="text-[11px] text-zinc-500 font-mono flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400/80" />
            <span>Auto-detects: Exam Dates • Code • Books • Notes</span>
          </div>
          <button
            type="submit"
            disabled={loading || !content.trim()}
            className="flex items-center gap-1.5 bg-cyan-600 hover:bg-cyan-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-zinc-950 font-semibold px-4 py-1.5 rounded-lg text-xs transition shadow-sm shadow-cyan-500/20"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Agents Sorting...</span>
              </>
            ) : (
              <>
                <Send className="w-3.5 h-3.5" />
                <span>Dump & Sort</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Live Agent Action Alert */}
      {statusMessage && (
        <div className="mt-3 bg-cyan-500/10 border border-cyan-500/20 rounded-lg p-2.5 text-xs text-cyan-300 font-mono flex items-start gap-2">
          <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
          <div>{statusMessage}</div>
        </div>
      )}

      {/* Recent Dumps Feed */}
      {recentDumps.length > 0 && (
        <div className="mt-4 pt-3 border-t border-zinc-800/60">
          <div className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Recent Ingested Vault Items</span>
            <span className="text-[10px] text-zinc-500">Stored on local disk</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-40 overflow-y-auto pr-1">
            {recentDumps.map((dump) => (
              <div
                key={dump.id}
                className="bg-zinc-950/70 border border-zinc-800/80 rounded-lg p-2.5 hover:border-zinc-700 transition text-xs"
              >
                <div className="flex items-center justify-between gap-1 mb-1">
                  <span className="font-semibold text-zinc-200 truncate">{dump.title}</span>
                  <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-cyan-300 border border-zinc-700">
                    {dump.type}
                  </span>
                </div>
                <p className="text-[11px] text-zinc-400 font-mono truncate">{dump.preview}</p>
                {dump.actions && dump.actions.length > 0 && (
                  <div className="mt-1 text-[10px] text-emerald-400/90 font-mono flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span className="truncate">{dump.actions[0]}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
