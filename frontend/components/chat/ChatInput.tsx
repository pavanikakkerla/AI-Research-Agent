"use client";
import { SendHorizonal } from "lucide-react";
import { useEffect, useRef, useState } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "0px";
    el.style.height = Math.min(el.scrollHeight, 180) + "px";
  }, [message]);

  const send = () => {
    const value = message.trim();
    if (!value || disabled) return;
    onSend(value);
    setMessage("");
  };

  return (
    <div className="flex flex-col">
      <div className="flex items-end gap-3 rounded-2xl border border-border bg-surface px-4 py-3 transition-colors focus-within:border-primary/60 focus-within:shadow-glow">
        <textarea
          ref={textareaRef}
          rows={1}
          value={message}
          placeholder="Ask anything..."
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send();
            }
          }}
          className="max-h-44 min-h-[2.75rem] flex-1 resize-none bg-transparent py-2 text-[0.9375rem] leading-7 text-foreground outline-none placeholder:text-muted-foreground"
        />
        <button
          onClick={send}
          disabled={!message.trim() || disabled}
          aria-label="Send message"
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:bg-muted disabled:text-muted-foreground"
        >
          <SendHorizonal size={18} />
        </button>
      </div>

      <div className="mt-2.5 flex items-center justify-between px-1 text-xs text-muted-foreground">
        <span>AI can make mistakes. Verify important information.</span>
        <span className="hidden lg:block">
          <kbd className="rounded bg-surface-hover px-1.5 py-0.5">Enter</kbd> send ·{" "}
          <kbd className="rounded bg-surface-hover px-1.5 py-0.5">Shift + Enter</kbd>{" "}
          new line
        </span>
      </div>
    </div>
  );
}
