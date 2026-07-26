export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 flex h-18 items-center border-b border-border bg-background/90 px-8 backdrop-blur-md">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">
          Research Agent
        </h1>

        <p className="mt-1 text-sm text-muted-foreground">
          AI-powered research assistant for searching, analysing and generating reports.
        </p>
      </div>
    </header>
  );
}