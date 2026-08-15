"use client";

import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import Message, { type ChatMessage } from "./Message";

const API_URL =
  process.env.NEXT_PUBLIC_RESEARCH_API_URL ??
  "http://127.0.0.1:8000";

const SUGGESTIONS = [
  "Latest AI research breakthroughs",
  "State of quantum computing in 2026",
  "How do diffusion models work?",
  "Climate policy: compare recent sources",
];

const STATS = [
  { value: "50+", label: "Trusted sources" },
  { value: "AI", label: "Smart summaries" },
  { value: "PDF", label: "Export reports" },
];

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: text,
      },
    ]);

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/research`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: text,
          max_results: 5,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Research failed."
        );
      }

      // --------------------------------------------------
      // Build Assistant Response
      // --------------------------------------------------

      const summary =
        data.summary || "";

      const conclusion =
        data.conclusion || "";

      let assistantContent = summary;

      // --------------------------------------------------
      // Add Conclusion
      // --------------------------------------------------

      if (conclusion.trim()) {
        assistantContent +=
          `\n\n### Conclusion\n\n${conclusion}`;
      }

      // --------------------------------------------------
      // Add Assistant Message
      // --------------------------------------------------

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: assistantContent,
        },
      ]);

    } catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error instanceof Error &&
            error.message !== "Failed to fetch"
              ? error.message
              : `Unable to reach the research backend at \`${API_URL}\`. Start it and try again.`,
        },
      ]);

    } finally {

      setLoading(false);

    }
  };

  const isEmpty =
    messages.length === 0;

  return (
    <main className="flex min-h-0 flex-1 flex-col">

      <div className="flex-1 overflow-y-auto">

        <div className="mx-auto w-full max-w-[56rem] px-8 py-12 2xl:max-w-[64rem]">

          {isEmpty && !loading && (

            <section className="pb-4">

              <h2 className="text-5xl font-bold tracking-tight">

                Welcome to research Agent{" "}

                <span className="text-gradient-brand"></span>

              </h2>

              <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">

                Search the web, analyze trusted sources,
                summarize long articles and generate
                research reports in seconds.

              </p>

              <div className="mt-8 flex flex-wrap gap-2.5">

                {SUGGESTIONS.map((item) => (

                  <button
                    key={item}
                    onClick={() => sendMessage(item)}
                    className="rounded-full border border-border bg-surface px-4 py-2 text-sm text-muted-foreground transition-colors hover:border-primary/50 hover:text-foreground"
                  >
                    {item}
                  </button>

                ))}

              </div>

              <div className="mt-12 grid grid-cols-3 gap-4">

                {STATS.map((stat) => (

                  <div
                    key={stat.label}
                    className="rounded-2xl border border-border bg-surface p-6 text-center shadow-soft"
                  >

                    <div className="text-3xl font-bold text-gradient-brand">

                      {stat.value}

                    </div>

                    <p className="mt-1 text-sm text-muted-foreground">

                      {stat.label}

                    </p>

                  </div>

                ))}

              </div>

            </section>

          )}

          <div className="space-y-8">

            {messages.map((message, index) => (

              <Message
                key={index}
                role={message.role}
                content={message.content}
              />

            ))}

            {loading && (

              <Message
                role="assistant"
                content={
                  "**Researching…**\n\n" +
                  "Searching multiple websites and preparing your report."
                }
              />

            )}

            <div ref={bottomRef} />

          </div>

        </div>

      </div>

      <div className="shrink-0 bg-background/80 pb-8 pt-4 backdrop-blur-xl">

        <div className="mx-auto w-full max-w-[56rem] px-8 2xl:max-w-[64rem]">

          <ChatInput
            onSend={sendMessage}
            disabled={loading}
          />

        </div>

      </div>

    </main>
  );
}