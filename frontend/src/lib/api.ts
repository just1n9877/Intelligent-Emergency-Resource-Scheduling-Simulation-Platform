import type { ApiResponse, Comparison, Metric, Network, Report, Route, Scenario, SimulationRun } from "@/types/api";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

async function unwrap<T>(response: Response): Promise<T> {
  const payload = (await response.json()) as ApiResponse<T>;
  if (!response.ok || !payload.success) {
    throw new Error(payload.message || `API request failed with ${response.status}`);
  }
  return payload.data;
}

export async function listScenarios(): Promise<Scenario[]> {
  return unwrap<Scenario[]>(await fetch(`${API_BASE}/scenarios`, { cache: "no-store" }));
}

export async function createScenario(input: Pick<Scenario, "name" | "description" | "scenario_type">): Promise<Scenario> {
  return unwrap<Scenario>(
    await fetch(`${API_BASE}/scenarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input)
    })
  );
}

export async function seedScenario(id: number): Promise<Scenario> {
  return unwrap<Scenario>(await fetch(`${API_BASE}/scenarios/${id}/seed`, { method: "POST" }));
}

export async function getNetwork(scenarioId: number): Promise<Network> {
  return unwrap<Network>(await fetch(`${API_BASE}/scenarios/${scenarioId}/network`, { cache: "no-store" }));
}

export async function runSimulation(scenarioId: number, algorithm: string, objective: string, parameters = {}): Promise<SimulationRun> {
  return unwrap<SimulationRun>(
    await fetch(`${API_BASE}/scenarios/${scenarioId}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ algorithm, objective, parameters })
    })
  );
}

export async function compareAlgorithms(
  scenarioId: number,
  algorithms: string[],
  objective: string,
  parameters = {}
): Promise<SimulationRun> {
  return unwrap<SimulationRun>(
    await fetch(`${API_BASE}/scenarios/${scenarioId}/compare`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ algorithms, objective, parameters })
    })
  );
}

export async function getRoutes(runId: number): Promise<Route[]> {
  return unwrap<Route[]>(await fetch(`${API_BASE}/simulation-runs/${runId}/routes`, { cache: "no-store" }));
}

export async function getMetrics(runId: number): Promise<Metric[]> {
  return unwrap<Metric[]>(await fetch(`${API_BASE}/simulation-runs/${runId}/metrics`, { cache: "no-store" }));
}

export async function getComparison(scenarioId: number): Promise<Comparison> {
  return unwrap<Comparison>(await fetch(`${API_BASE}/scenarios/${scenarioId}/comparison`, { cache: "no-store" }));
}

export async function generateReport(runId: number): Promise<Report> {
  return unwrap<Report>(await fetch(`${API_BASE}/reports/${runId}/generate`, { method: "POST" }));
}
