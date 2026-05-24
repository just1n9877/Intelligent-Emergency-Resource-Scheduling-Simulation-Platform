"use client";

import type { Demand, Network, Route } from "@/types/api";

type Props = {
  network: Network;
  routes?: Route[];
};

function priorityColor(priority: number) {
  if (priority >= 5) return "#dc2626";
  if (priority >= 4) return "#f59e0b";
  if (priority >= 3) return "#0f766e";
  return "#64748b";
}

export function NetworkMap({ network, routes = [] }: Props) {
  if (!network.nodes.length) {
    return <div className="flex h-[520px] items-center justify-center text-sm text-muted">No network data</div>;
  }

  const minLat = Math.min(...network.nodes.map((node) => node.latitude));
  const maxLat = Math.max(...network.nodes.map((node) => node.latitude));
  const minLon = Math.min(...network.nodes.map((node) => node.longitude));
  const maxLon = Math.max(...network.nodes.map((node) => node.longitude));
  const demandByNode = new Map<number, Demand>(network.demands.map((demand) => [demand.node_id, demand]));
  const depotNodes = new Set(network.depots.map((depot) => depot.node_id));
  const vehicleNodes = new Set(network.vehicles.map((vehicle) => vehicle.current_node_id));
  const nodeById = new Map(network.nodes.map((node) => [node.id, node]));

  const project = (nodeId: number) => {
    const node = nodeById.get(nodeId);
    if (!node) return { x: 0, y: 0 };
    const x = 52 + ((node.longitude - minLon) / Math.max(maxLon - minLon, 0.0001)) * 696;
    const y = 48 + (1 - (node.latitude - minLat) / Math.max(maxLat - minLat, 0.0001)) * 424;
    return { x, y };
  };

  return (
    <svg viewBox="0 0 800 520" className="h-[520px] w-full rounded-[8px] border border-border bg-stone-50">
      <rect x="0" y="0" width="800" height="520" fill="#fafaf8" />
      {network.edges.map((edge) => {
        const a = project(edge.source_node_id);
        const b = project(edge.target_node_id);
        const congested = edge.congestion_factor > 1.4;
        return (
          <line
            key={edge.id}
            x1={a.x}
            y1={a.y}
            x2={b.x}
            y2={b.y}
            stroke={edge.is_blocked ? "#dc2626" : congested ? "#f59e0b" : "#94a3b8"}
            strokeWidth={edge.is_blocked ? 4 : congested ? 3 : 2}
            strokeDasharray={edge.is_blocked ? "8 7" : undefined}
            opacity={edge.is_blocked ? 0.88 : 0.62}
          >
            <title>
              Edge {edge.source_node_id} to {edge.target_node_id} / {edge.distance_km} km / congestion {edge.congestion_factor}
            </title>
          </line>
        );
      })}
      {routes.flatMap((route, routeIndex) =>
        route.node_path.slice(0, -1).map((nodeId, index) => {
          const a = project(nodeId);
          const b = project(route.node_path[index + 1]);
          return (
            <line
              key={`${route.id}-${index}`}
              className="route-line"
              x1={a.x}
              y1={a.y}
              x2={b.x}
              y2={b.y}
              stroke={["#0f766e", "#2563eb", "#d97706", "#7c3aed"][routeIndex % 4]}
              strokeWidth={5}
              strokeLinecap="round"
              opacity={0.86}
            />
          );
        })
      )}
      {network.nodes.map((node) => {
        const point = project(node.id);
        const demand = demandByNode.get(node.id);
        const isDepot = depotNodes.has(node.id);
        const hasVehicle = vehicleNodes.has(node.id);
        const radius = isDepot ? 11 : demand ? 9 : 5;
        const fill = isDepot ? "#111827" : demand ? priorityColor(demand.priority) : "#475569";
        return (
          <g key={node.id}>
            <circle cx={point.x} cy={point.y} r={radius} fill={fill} stroke="#fff" strokeWidth="2">
              <title>
                {node.name}
                {demand ? ` / demand ${demand.quantity} / priority ${demand.priority}` : ""}
                {isDepot ? " / depot" : ""}
                {hasVehicle ? " / vehicle start" : ""}
              </title>
            </circle>
            {hasVehicle && <rect x={point.x + 7} y={point.y - 15} width="12" height="12" fill="#2563eb" rx="2" />}
          </g>
        );
      })}
    </svg>
  );
}

