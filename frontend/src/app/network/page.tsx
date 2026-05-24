"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusPanel } from "@/components/ui/status";
import { getNetwork, listScenarios } from "@/lib/api";
import { NetworkMap } from "@/features/dashboard/NetworkMap";
import type { Network, Scenario } from "@/types/api";

function NetworkPageContent() {
  const params = useSearchParams();
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [scenarioId, setScenarioId] = useState<number | null>(Number(params.get("scenarioId")) || null);
  const [network, setNetwork] = useState<Network | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listScenarios()
      .then((items) => {
        setScenarios(items);
        if (!scenarioId && items[0]) setScenarioId(items[0].id);
        setError(null);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load scenarios"));
  }, []);

  useEffect(() => {
    if (!scenarioId) return;
    setNetwork(null);
    getNetwork(scenarioId)
      .then((data) => {
        setNetwork(data);
        setError(null);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load network"));
  }, [scenarioId]);

  const selected = useMemo(() => scenarios.find((scenario) => scenario.id === scenarioId), [scenarioId, scenarios]);

  return (
    <main className="mx-auto max-w-7xl px-5 py-8">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm font-bold uppercase text-accent">Network Visualization</p>
          <h1 className="mt-2 text-3xl font-black">{selected?.name ?? "Road Network"}</h1>
        </div>
        <select
          value={scenarioId ?? ""}
          onChange={(event) => setScenarioId(Number(event.target.value))}
          className="h-10 rounded-[6px] border border-border bg-panel px-3"
        >
          {scenarios.map((scenario) => (
            <option key={scenario.id} value={scenario.id}>{scenario.name}</option>
          ))}
        </select>
      </div>
      {error && <StatusPanel className="mt-6" title="Network data unavailable" message={error} variant="error" />}
      <div className="mt-6 grid gap-5 lg:grid-cols-[1fr_310px]">
        <Card>
          <CardContent className="p-3">
            {network ? <NetworkMap network={network} /> : <StatusPanel title="Loading network" message="Fetching nodes, edges, vehicles, depots, and demands from the backend." />}
          </CardContent>
        </Card>
        <div className="space-y-4">
          <Card>
            <CardHeader><CardTitle>Road State</CardTitle></CardHeader>
            <CardContent className="space-y-3 text-sm">
              <p><span className="mr-2 inline-block h-1 w-8 bg-slate-400" /> Normal edge</p>
              <p><span className="mr-2 inline-block h-1 w-8 bg-warning" /> Congested edge</p>
              <p><span className="mr-2 inline-block h-1 w-8 border-t-4 border-dashed border-danger" /> Blocked edge</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Demand Priority</CardTitle></CardHeader>
            <CardContent className="space-y-3 text-sm">
              <p><span className="mr-2 inline-block h-3 w-3 rounded-full bg-danger" /> Priority 5</p>
              <p><span className="mr-2 inline-block h-3 w-3 rounded-full bg-warning" /> Priority 4</p>
              <p><span className="mr-2 inline-block h-3 w-3 rounded-full bg-accent" /> Priority 3</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}

export default function NetworkPage() {
  return (
    <Suspense fallback={<main className="mx-auto max-w-7xl px-5 py-8"><StatusPanel title="Loading network" message="Preparing network visualization controls." /></main>}>
      <NetworkPageContent />
    </Suspense>
  );
}
