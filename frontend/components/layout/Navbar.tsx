import { Bell, Search, Settings } from "lucide-react";

export default function Navbar() {
  return (
    <header className="glass sticky top-0 z-40 flex h-[4.5rem] shrink-0 items-center justify-between border-b border-border px-8">
      <div>
        <h1 className="text-base font-semibold">Research workspace</h1>
        <p className="text-xs text-muted-foreground">
          Search, compare sources and generate reports
        </p>
      </div>

      <div className="flex items-center gap-1">
        {[Search, Bell, Settings].map((Icon, i) => (
          <button
            key={i}
            className="rounded-xl p-2.5 text-muted-foreground transition-colors hover:bg-surface-hover hover:text-foreground"
          >
            <Icon size={18} />
          </button>
        ))}
      </div>
    </header>
  );
}
