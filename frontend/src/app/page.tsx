import Link from "next/link";
import { ArrowRight, Cpu, GitBranch, Network, ShieldCheck, type LucideIcon } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  const featureCards: Array<{ title: string; body: string; Icon: LucideIcon }> = [
    { title: "Complex System Model", body: "Nodes, edges, depots, vehicles, demands, road states.", Icon: Network },
    { title: "Optimization Core", body: "Dijkstra, A*, greedy, priority dispatch, OR-Tools CVRP.", Icon: GitBranch },
    { title: "Engineering Stack", body: "Next.js, FastAPI, SQLAlchemy, PostGIS, Redis, Celery.", Icon: Cpu },
    { title: "Interview Narrative", body: "Metrics, algorithm comparison, limitations, future work.", Icon: ShieldCheck }
  ];

  return (
    <main>
      <section className="relative min-h-[calc(100vh-65px)] overflow-hidden border-b border-border">
        <svg className="absolute inset-0 h-full w-full" viewBox="0 0 1200 680" preserveAspectRatio="none" aria-hidden="true">
          <defs>
            <linearGradient id="road" x1="0" x2="1" y1="0" y2="1">
              <stop offset="0%" stopColor="#0f766e" stopOpacity="0.46" />
              <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.28" />
            </linearGradient>
          </defs>
          <path d="M60 520 C260 400 300 180 540 250 S830 510 1140 160" fill="none" stroke="url(#road)" strokeWidth="18" />
          <path d="M120 180 C330 230 470 420 700 360 S920 210 1120 420" fill="none" stroke="#1f2937" strokeOpacity="0.16" strokeWidth="10" />
          {[140, 330, 520, 730, 910, 1060].map((x, index) => (
            <circle key={x} cx={x} cy={index % 2 === 0 ? 420 : 265} r={index === 3 ? 16 : 10} fill={index === 3 ? "#dc2626" : "#0f766e"} opacity="0.9" />
          ))}
        </svg>
        <div className="relative mx-auto grid max-w-7xl gap-8 px-5 py-16 lg:grid-cols-[1.05fr_0.95fr] lg:py-24">
          <div className="max-w-3xl">
            <Badge className="border-accent/30 bg-teal-50 text-accent">System Engineering / Operations Research / Simulation</Badge>
            <h1 className="mt-6 text-4xl font-black leading-tight text-foreground md:text-6xl">
              Intelligent Emergency Resource Scheduling & Simulation Platform
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-muted">
              A full-stack research-grade platform for civil emergency logistics: road-network modeling, constrained vehicle dispatch,
              routing algorithms, simulation metrics, and reproducible experiment reports.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button asChild>
                <Link href="/simulation">
                  Run Demo <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="secondary">
                <Link href="/network">Inspect Network</Link>
              </Button>
            </div>
          </div>
          <div className="grid content-end gap-3 sm:grid-cols-2 lg:pb-8">
            {featureCards.map(({ title, body, Icon }) => (
              <div key={title} className="rounded-[8px] border border-border bg-panel/90 p-5 shadow-command">
                <Icon className="h-6 w-6 text-accent" />
                <h2 className="mt-4 text-base font-bold">{title}</h2>
                <p className="mt-2 text-sm leading-6 text-muted">{body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
