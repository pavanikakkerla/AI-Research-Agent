import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export default function Message({ role, content }: ChatMessage) {
  if (role === "user") {
    return (
      <div className="flex w-full justify-end">
        <div className="max-w-[42rem] rounded-2xl rounded-br-md bg-primary px-5 py-3.5 text-primary-foreground shadow-soft">
          <p className="whitespace-pre-wrap leading-7">{content}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex w-full gap-4">
      <div className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-brand text-xs font-bold text-primary-foreground shadow-glow">
        N
      </div>
      <div className="min-w-0 flex-1">
        <div className="mb-2 text-sm font-semibold text-muted-foreground">
          Neo Research
        </div>
        <article className="markdown">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        </article>
      </div>
    </div>
  );
}
