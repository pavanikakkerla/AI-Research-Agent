"use client";

import { useState } from "react";
import Chat from "@/components/chat/Chat";
import Navbar from "@/components/layout/Navbar";
import Sidebar from "@/components/layout/Sidebar";

const RECENT_CHATS = [
  "AI agents",
  "Machine learning",
  "FastAPI backend",
  "Python tooling",
  "SpaceX launches",
  "Climate change",
];

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeChat, setActiveChat] = useState<string | null>(null);

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <Sidebar
        open={sidebarOpen}
        onToggle={() => setSidebarOpen((v) => !v)}
        chats={RECENT_CHATS}
        activeChat={activeChat}
        onSelect={setActiveChat}
        onNewChat={() => setActiveChat(null)}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <Navbar />
        <Chat />
      </div>
    </div>
  );
}