# 面向应急资源调度的复杂系统建模、优化与仿真平台

项目英文名：Intelligent Emergency Resource Scheduling & Simulation Platform  
应用场景：公开民用应急物资配送、灾后救援资源调度、校园医疗物资调度、智能物流调度  
技术关键词：Complex System Modeling, Path Planning, Vehicle Routing Problem, Simulation Evaluation, Full-stack Engineering

---

## 第一页：问题背景、定义与技术路线

### 1. 项目背景

城市应急资源调度需要在有限车辆、有限仓库库存、道路拥堵或阻塞、需求优先级不同等条件下，快速决定“哪些车辆去服务哪些需求点、按什么顺序服务、走哪条路径”。这类问题不是单纯的网页系统，也不是单一最短路问题，而是一个包含资源、网络、任务、约束、目标和反馈指标的复杂系统。

本项目选择民用应急物流作为场景，避免军事、涉密或攻击性内容，重点展示系统工程和电子信息方向中常见的建模、优化、仿真与工程实现能力。

### 2. 问题定义

给定一个城市道路网络、若干仓库（depots）、车辆（vehicles）和需求点（demands），系统需要生成调度方案（dispatch plan）：

- 为每辆可用车辆分配需求点服务序列；
- 为车辆生成经过路网节点的实际路径；
- 考虑车辆容量、需求量、服务时间、需求优先级、道路拥堵和道路阻塞；
- 计算总距离、平均响应时间、完成率、高优先级完成率、车辆利用率、延迟任务和未服务任务；
- 对多种算法进行统一指标对比，并生成实验报告。

### 3. 系统工程价值

该项目体现系统工程（System Engineering）的核心思想：先定义系统边界和组成要素，再建立模型和约束，最后通过仿真指标评估决策效果。

- 系统要素：路网节点、道路边、仓库、车辆、需求点、算法配置、调度方案、路线和指标结果；
- 系统约束：车辆容量、道路通行状态、拥堵系数、服务时间、需求优先级、可选时间窗；
- 系统目标：不是只追求最短距离，而是在完成率、响应时间、优先级保障和运行效率之间做权衡；
- 系统评估：用统一指标和 weighted score 比较算法，而不是只展示单次路径结果。

### 4. 技术路线总览

项目采用前后端分离和可复现实验架构：

- 前端：Next.js App Router、TypeScript、Tailwind CSS、shadcn/ui、Recharts；
- 后端：FastAPI、SQLAlchemy 2.x、Pydantic、Alembic；
- 数据层：PostgreSQL + PostGIS，测试环境支持 SQLite；
- 异步与工程化：Docker Compose、Redis、Celery worker、pytest、GitHub Actions；
- 算法层：NetworkX 实现图建模、Dijkstra 和 A*；OR-Tools 实现 CVRP 基线；自研 Greedy 和 Priority dispatch；
- 报告层：无 API key 时使用 deterministic template，有 OpenAI-compatible API key 时可进行英文报告润色。

---

## 第二页：数学建模与算法设计

### 1. 数学建模

道路网络建模为有向带权图：

```text
G = (V, E)
```

其中 `V` 表示路网节点，`E` 表示道路边。每条边包含距离、速度、拥堵系数和是否阻塞。实际通行时间为：

```text
travel_time_min = distance_km / speed_kmph * 60 * congestion_factor
```

如果道路被阻塞（blocked edge），算法构图时将该边视为不可通行。

### 2. 决策变量

核心决策变量包括：

- `x_{k,i}`：车辆 `k` 是否服务需求点 `i`；
- `seq_k`：车辆 `k` 的需求点服务顺序；
- `path_{u,v}`：从节点 `u` 到节点 `v` 的路网路径；
- `arrival_i`：需求点 `i` 的到达时间；
- `unserved_i`：需求点 `i` 是否未被服务。

在工程实现中，这些变量对应 `DispatchPlan`、`Route`、`demand_sequence`、`node_path` 和 `MetricResult` 等数据结构。

### 3. 目标函数

系统支持多种目标：

- `minimize_total_distance`：最小化总行驶距离；
- `minimize_total_response_time`：最小化响应时间；
- `maximize_priority_completion`：最大化高优先级需求完成效果；
- `weighted_multi_objective`：综合考虑完成率、优先级、响应时间、距离和运行时间。

当前 weighted score 的定义为：

```text
score =
0.30 * completion_rate
+ 0.25 * priority_completion_rate
+ 0.20 * normalized_response_time_score
+ 0.15 * normalized_distance_score
+ 0.10 * normalized_runtime_score
```

对距离、响应时间和运行时间这类“越小越好”的指标，采用同场景算法间 min-max 归一化：

```text
normalized_score = 1 - (value - min_value) / (max_value - min_value)
```

如果所有算法数值相同，则该项归一化得分为 `1.0`。

### 4. 约束条件

当前项目真实实现和评估的约束包括：

- 车辆容量约束（vehicle capacity）：车辆服务需求量不能超过容量；
- 需求优先级（demand priority）：Priority Dispatch 会优先处理高优先级任务，指标中计算 priority completion；
- 服务时间（service time）：车辆到达需求点后需要消耗服务时间；
- 道路拥堵（road congestion）：拥堵系数会放大通行时间；
- 道路阻塞（blocked edge）：阻塞边不参与路径搜索；
- 时间窗评估（time-window evaluation）：当前以 delayed demands 指标评估是否超过需求截止时间，完整硬约束 VRPTW 属于未来扩展。

### 5. 算法设计

**Dijkstra**：用于非负权重图上的最短路搜索。项目中可按距离或通行时间作为权重，适合作为透明、稳定的路径规划基线。

**A\***：在 Dijkstra 的代价基础上加入地理距离启发式（heuristic），在空间图上有机会减少搜索范围。最终路径仍由真实边权决定。

**Greedy Dispatch**：按需求顺序处理任务，每次选择容量可行且当前路径代价较低的车辆。优点是速度快、逻辑清晰；缺点是局部最优，可能忽视高优先级任务。

**Priority Dispatch**：先按优先级和时间窗排序需求，再做可行车辆分配。适合解释应急场景中“高优先级任务优先保障”的决策逻辑。

**OR-Tools CVRP**：将车辆调度建模为 Capacitated Vehicle Routing Problem。系统构造需求点距离矩阵、车辆容量和需求量，由 OR-Tools 求解容量约束下的车辆路径问题。若资源短缺导致不可行，当前实现会回退到 priority fallback，并在算法名称中体现。

---

## 第三页：实验设计、结果解读与项目总结

### 1. 实验设计

系统内置六类标准场景：

| 场景 | 车辆 | 需求 | 道路状态 | 预期挑战 |
| --- | ---: | ---: | --- | --- |
| Normal Scenario | 3 | 6 | 正常 | 作为基准组，观察距离、响应时间和利用率 |
| Congestion Scenario | 3 | 6 | 中心道路拥堵 | 检验算法是否受拥堵通行时间影响 |
| Demand Surge Scenario | 4 | 9 | 正常 | 检验需求突然增加时的完成率和扩展性 |
| Resource Shortage Scenario | 2 | 6 | 正常 | 检验车辆容量不足下的未服务任务 |
| Blocked Road Scenario | 3 | 6 | 关键道路阻塞 | 检验路网连通性和绕行能力 |
| High Priority Rescue Scenario | 3 | 7 | 局部轻度拥堵 | 检验高优先级任务集中时的保障能力 |

每个场景都可以通过同一 API 和前端页面运行仿真，保证算法比较是在相同输入条件下完成。

### 2. 实验指标

项目记录并展示以下指标：

- `total_distance`：所有车辆总行驶距离；
- `average_response_time`：已服务需求点平均到达时间；
- `max_response_time`：最晚响应时间；
- `completion_rate`：任务完成率；
- `priority_completion_rate`：按优先级加权的完成率；
- `vehicle_utilization`：已服务需求量占总车辆容量比例；
- `delayed_demands`：超过时间窗的任务数；
- `unserved_demands`：未被服务的任务数；
- `algorithm_runtime_ms`：算法运行时间。

### 3. 算法对比结果

当前平台不会写死实验数值，而是通过 `/api/scenarios/{id}/compare` 运行同一场景下的算法，并在 `/results` 页面展示真实返回的指标、图表和 weighted score。

从实验解释角度，可以重点说明：

- Greedy Dispatch 通常运行最快，适合作为快速基线；
- Priority Dispatch 在高优先级任务集中的场景中更容易提高 urgent task completion；
- Dijkstra-based 和 A*-based Dispatch 展示了路径规划算法在调度中的作用；
- OR-Tools CVRP 更适合解释容量约束和全局车辆路径优化，但在资源短缺场景下可能出现不可行并触发 fallback；
- blocked edge 和 congestion 会改变路径成本，因此同一需求点在不同场景下可能得到不同路线。

### 4. 项目亮点

- 完整闭环：建模、算法、仿真、指标、报告和前端展示形成闭环；
- 真实数据流：前端图表来自 FastAPI 和数据库中的实际仿真结果，不是静态假数据；
- 多算法比较：同一场景下可比较启发式算法和 OR-Tools 基线；
- 可复现：seed 场景、测试、Docker Compose、OpenAPI 文档和 deterministic report 支持复现实验；
- 适合复试讲解：能从系统工程、运筹优化、数据结构、AI 辅助决策和全栈实现多个角度展开。

### 5. 不足与未来改进

当前项目仍是可演示 MVP，不应夸大为工业级系统。主要不足包括：

- 动态需求和实时道路状态尚未做在线滚动优化；
- VRPTW 目前主要是时间窗评估，完整硬约束求解仍需扩展；
- 道路网络为 seed 生成网格，不是接入真实城市地图；
- 前端有基础可视化和图表，但还可以加入更强的交互分析；
- 报告支持 Markdown，PDF 导出是后续计划。

后续可以继续加入 rolling-horizon re-optimization、完整 VRPTW、真实地图数据接入、实验批处理和更系统的消融实验。
