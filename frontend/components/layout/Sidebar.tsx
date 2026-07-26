import { MessageSquare, PanelLeftClose, PanelLeftOpen, Plus } from "lucide-react";

interface SidebarProps {
  open: boolean;
  onToggle: () => void;
  chats: string[];
  activeChat: string | null;
  onSelect: (chat: string) => void;
  onNewChat: () => void;
}

export default function Sidebar({
  open,
  onToggle,
  chats,
  activeChat,
  onSelect,
  onNewChat,
}: SidebarProps) {
  return (
    <aside
      className={`flex h-full shrink-0 flex-col border-r border-border bg-sidebar transition-[width] duration-300 ${
        open ? "w-[17rem]" : "w-[4.5rem]"
      }`}
    >
      <div className="flex h-[4.5rem] items-center gap-3 border-b border-border px-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-brand text-base font-bold text-primary-foreground shadow-glow">
          N
        </div>
        {open && (
          <div className="min-w-0 flex-1">
            <div className="truncate text-sm font-semibold">Neo Research</div>
            <div className="truncate text-xs text-muted-foreground">
              AI Research Assistant
            </div>
          </div>
        )}
        <button
          onClick={onToggle}
          aria-label={open ? "Collapse sidebar" : "Expand sidebar"}
          className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-surface-hover hover:text-foreground"
        >
          {open ? <PanelLeftClose size={18} /> : <PanelLeftOpen size={18} />}
        </button>
      </div>

      <div className="p-3">
        <button
          onClick={onNewChat}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
        >
          <Plus size={18} />
          {open && "New chat"}
        </button>
      </div>

      <div className="no-scrollbar flex-1 overflow-y-auto px-3 pb-3">
        {open && (
          <h2 className="mb-2 px-2 text-[0.6875rem] font-semibold uppercase tracking-widest text-muted-foreground">
            Recent
          </h2>
        )}
        <div className="space-y-1">
          {chats.map((chat) => (
            <button
              key={chat}
              onClick={() => onSelect(chat)}
              title={chat}
              className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${
                activeChat === chat
                  ? "bg-surface-hover text-foreground"
                  : "text-muted-foreground hover:bg-surface-hover hover:text-foreground"
              } ${open ? "" : "justify-center px-0"}`}
            >
              <MessageSquare size={16} className="shrink-0" />
              {open && <span className="truncate">{chat}</span>}
            </button>
          ))}
        </div>
      </div>

      <div className="border-t border-border p-3">
        <div
          className={`flex items-center gap-3 rounded-xl bg-surface px-3 py-2.5 ${
            open ? "" : "justify-center px-0"
          }`}
        >
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-brand text-xs font-bold text-primary-foreground">
            N
          </div>
          {open && (
            <div className="min-w-0">
              <div className="truncate text-sm font-medium">Neo Research</div>
              <div className="truncate text-xs text-muted-foreground">Free plan</div>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
