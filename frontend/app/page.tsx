"use client";

import Chat from "@/components/chat/Chat";
import Navbar from "@/components/layout/Navbar";

export default function Home() {
  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <div className="flex flex-1 flex-col">
        <Navbar />
        <Chat />
      </div>
    </div>
  );
}