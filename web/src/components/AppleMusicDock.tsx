"use client";

import React, { useState } from "react";
import { Music, ExternalLink, Headphones, Disc3 } from "lucide-react";

interface PlaylistPreset {
  id: string;
  name: string;
  genre: string;
  embedUrl: string;
  appUrl: string;
}

const PRESET_PLAYLISTS: PlaylistPreset[] = [
  {
    id: "endel-study",
    name: "Endel Study Soundscape",
    genre: "Adaptive Sound / Deep Work",
    embedUrl: "https://embed.music.apple.com/us/playlist/study-beats/pl.u-38oWZlNuPYo74B",
    appUrl: "https://music.apple.com/us/playlist/study-beats/pl.u-38oWZlNuPYo74B"
  },
  {
    id: "deep-focus",
    name: "Deep Focus Ambient Waves",
    genre: "Atmospheric / No Vocals",
    embedUrl: "https://embed.music.apple.com/us/playlist/pure-focus/pl.u-pMyl1m4u43lA",
    appUrl: "https://music.apple.com/us/playlist/pure-focus/pl.u-pMyl1m4u43lA"
  },
  {
    id: "lofi-coding",
    name: "Lo-Fi Instrumental Beats",
    genre: "Chillhop / Problem Solving",
    embedUrl: "https://embed.music.apple.com/us/playlist/beat-instrumentals/pl.u-AkAm84bTD2Z0",
    appUrl: "https://music.apple.com/us/playlist/beat-instrumentals/pl.u-AkAm84bTD2Z0"
  },
  {
    id: "synthwave",
    name: "Cyberpunk & Synth Flow",
    genre: "High-Speed Engineering",
    embedUrl: "https://embed.music.apple.com/us/playlist/synthwave-focus/pl.u-xlyNE8duJk3y",
    appUrl: "https://music.apple.com/us/playlist/synthwave-focus/pl.u-xlyNE8duJk3y"
  }
];

export default function AppleMusicDock() {
  const [activePlaylist, setActivePlaylist] = useState<PlaylistPreset>(PRESET_PLAYLISTS[0]);
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400">
            <Music className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              Apple Music Study & Focus Dock
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/10 border border-rose-500/30 text-rose-400">
                MusicKit Embedded
              </span>
            </h2>
            <p className="text-xs text-zinc-400">
              Instant soundscapes for SRM DO3 Power Days, late-night coding, and exam revision.
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs text-zinc-400 hover:text-zinc-200 font-mono"
        >
          {isExpanded ? "Collapse Player" : "Expand Player"}
        </button>
      </div>

      {/* Playlist Selector Buttons */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
        {PRESET_PLAYLISTS.map((pl) => (
          <button
            key={pl.id}
            onClick={() => {
              setActivePlaylist(pl);
              setIsExpanded(true);
            }}
            className={`p-2.5 rounded-lg border text-left transition flex flex-col justify-between ${
              activePlaylist.id === pl.id
                ? "bg-rose-500/10 border-rose-500/40 text-zinc-100 shadow-sm shadow-rose-500/10"
                : "bg-zinc-950/60 border-zinc-800/80 text-zinc-400 hover:border-zinc-700 hover:text-zinc-200"
            }`}
          >
            <div className="flex items-center justify-between gap-1 mb-1">
              <span className="text-xs font-semibold truncate">{pl.name}</span>
              {activePlaylist.id === pl.id && <Disc3 className="w-3.5 h-3.5 text-rose-400 animate-spin shrink-0" />}
            </div>
            <span className="text-[10px] font-mono text-zinc-500 truncate">{pl.genre}</span>
          </button>
        ))}
      </div>

      {/* Embedded Apple Music Player */}
      {isExpanded && (
        <div className="rounded-xl overflow-hidden border border-zinc-800/80 bg-zinc-950 shadow-inner">
          <iframe
            id="apple-music-player"
            allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write"
            frameBorder="0"
            height="175"
            style={{ width: "100%", maxWidth: "100%", overflow: "hidden", borderRadius: "10px" }}
            sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation"
            src={activePlaylist.embedUrl}
          />
        </div>
      )}

      {/* Footer Info */}
      <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-zinc-500">
        <div className="flex items-center gap-1.5">
          <Headphones className="w-3.5 h-3.5 text-rose-400/80" />
          <span>Active: {activePlaylist.name}</span>
        </div>
        <a
          href={activePlaylist.appUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1 text-zinc-400 hover:text-rose-400 transition"
        >
          <span>Open in Apple Music</span>
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
}
