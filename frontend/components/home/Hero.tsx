"use client";

import { ArrowRight, Search, Sparkles } from "lucide-react";
import Container from "../layout/Container";

const suggestions = [
  "Latest AI Research",
  "Quantum Computing",
  "Machine Learning",
  "Climate Change",
];

export default function Hero() {
  return (
    <section className="relative overflow-hidden">

      {/* Background Glow */}

      <div className="absolute left-1/2 top-32 h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-blue-600/10 blur-[150px]" />

      <Container>

        <div className="relative flex flex-col items-center pt-28 pb-20">

          {/* Badge */}

          <div className="mb-8 flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-5 py-2 text-sm text-blue-300">

            <Sparkles size={15} />

            Built for Developers • Researchers • Students

          </div>

          {/* Heading */}

          <h1 className="max-w-5xl text-center text-5xl font-black leading-tight tracking-tight md:text-7xl">

            AI Research

            <br />

            <span className="bg-gradient-to-r from-blue-400 via-cyan-300 to-sky-400 bg-clip-text text-transparent">

              Done Right.

            </span>

          </h1>

          {/* Subtitle */}

          <p className="mt-8 max-w-2xl text-center text-xl leading-9 text-zinc-400">

            Search. Analyze. Compare. Generate reliable research
            reports in seconds.

          </p>

          {/* Search */}

          <div className="mt-14 w-full max-w-3xl">

            <div className="group flex items-center rounded-2xl border border-zinc-800 bg-zinc-900 transition-all duration-300 hover:border-blue-500/40 hover:shadow-[0_0_40px_rgba(59,130,246,.15)]">

              <Search
                size={22}
                className="ml-6 text-zinc-500"
              />

              <input
                placeholder="Ask anything..."
                className="h-16 flex-1 bg-transparent px-4 text-lg outline-none placeholder:text-zinc-500"
              />

              <button className="m-2 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 transition hover:bg-blue-500">

                <ArrowRight size={20} />

              </button>

            </div>

          </div>

          {/* Suggestions */}

          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">

            {suggestions.map((item) => (

              <button
                key={item}
                className="rounded-full border border-zinc-800 bg-zinc-900 px-5 py-2 text-sm text-zinc-400 transition hover:border-blue-500/40 hover:text-white"
              >
                {item}
              </button>

            ))}

          </div>

          {/* Stats */}

          <div className="mt-20 grid w-full max-w-5xl grid-cols-3 gap-6">

            <div className="rounded-3xl border border-zinc-800 bg-zinc-900/60 p-8 text-center backdrop-blur">

              <h2 className="text-4xl font-bold text-blue-400">

                50+

              </h2>

              <p className="mt-2 text-zinc-400">

                Trusted Sources

              </p>

            </div>

            <div className="rounded-3xl border border-zinc-800 bg-zinc-900/60 p-8 text-center backdrop-blur">

              <h2 className="text-4xl font-bold text-blue-400">

                AI

              </h2>

              <p className="mt-2 text-zinc-400">

                Smart Summaries

              </p>

            </div>

            <div className="rounded-3xl border border-zinc-800 bg-zinc-900/60 p-8 text-center backdrop-blur">

              <h2 className="text-4xl font-bold text-blue-400">

                PDF

              </h2>

              <p className="mt-2 text-zinc-400">

                Export Reports

              </p>

            </div>

          </div>

        </div>

      </Container>

    </section>
  );
}