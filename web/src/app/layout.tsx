import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ThanvishOS — Neural Academic Hub",
  description: "Personal AI Academic Dashboard, SRM Day Order Radar, Second Brain & Parallel Mastery Hub",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-zinc-950 text-zinc-100 min-h-screen selection:bg-cyan-500/30 selection:text-cyan-200">
        {children}
      </body>
    </html>
  );
}
