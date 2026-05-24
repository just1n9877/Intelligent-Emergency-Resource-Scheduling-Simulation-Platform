# Resume and Interview Materials

项目依据：当前 README、docs、代码结构和已实现功能。以下表述只覆盖已完成内容，不把 Roadmap 功能写成已实现能力。

---

## 1. 中文简历项目经历

项目名：面向应急资源调度的复杂系统建模、优化与仿真平台

- 建模路网、车辆、仓库与需求约束
- 实现 Dijkstra/A*/OR-Tools 调度
- 构建仿真实验与多指标对比
- 完成 FastAPI/Next.js 全栈平台

---

## 2. English Resume Bullets

Project: Intelligent Emergency Resource Scheduling & Simulation Platform

- Modeled civil emergency logistics as a weighted road graph with depots, vehicles, demands, congestion, and blocked edges.
- Implemented Dijkstra, A*, Greedy/Priority dispatch, and an OR-Tools CVRP baseline for route planning and constrained scheduling.
- Built simulation evaluation with distance, response time, completion rate, priority completion, utilization, and runtime metrics.
- Delivered a FastAPI + Next.js dashboard with real API data flow, algorithm comparison charts, and deterministic report generation.

---

## 3. 复试中文自我介绍中的项目段落

### 30 秒版本

我做的项目是“面向应急资源调度的复杂系统建模、优化与仿真平台”。它面向公开民用应急物流场景，把城市路网、仓库、车辆和需求点建模成一个带约束的调度系统。项目实现了 Dijkstra、A*、贪心调度、优先级调度和 OR-Tools CVRP，并通过 FastAPI 和 Next.js 做成可运行平台，可以展示路线、指标对比和实验报告。

### 1 分钟版本

我的核心项目是“面向应急资源调度的复杂系统建模、优化与仿真平台”。我把城市道路抽象为有向带权图，节点表示路口或需求位置，边包含距离、速度、拥堵系数和阻塞状态；同时建模仓库、车辆容量、需求量、优先级和服务时间。算法层实现了 Dijkstra、A*、Greedy Dispatch、Priority Dispatch 和 OR-Tools CVRP，用统一指标比较总距离、响应时间、完成率、高优先级完成率、车辆利用率和运行时间。工程上使用 FastAPI、SQLAlchemy、PostgreSQL/PostGIS、Redis/Celery、Next.js 和 Recharts，形成从场景管理、仿真运行、结果展示到报告生成的闭环。

### 2 分钟版本

我想重点介绍一个面向系统工程方向的项目，叫“面向应急资源调度的复杂系统建模、优化与仿真平台”。项目限定在公开民用应急物流场景，不涉及军事或涉密内容。它的目标不是做一个普通后台，而是把一个复杂调度问题完整地转化为系统模型、优化算法、仿真实验和工程平台。

在建模上，我把城市路网抽象为有向带权图，节点表示路口、仓库或需求点，边记录距离、速度、拥堵系数和是否阻塞。车辆有容量和起点，需求点有需求量、优先级、服务时间和时间窗评估信息。系统需要决定哪些车辆服务哪些需求点、按什么顺序服务、走哪些路网节点，并记录未服务和延迟任务。

在算法上，我实现了 Dijkstra 和 A* 路径规划，也实现了 Greedy Dispatch、Priority Dispatch，并用 OR-Tools CVRP 作为容量约束车辆路径问题的优化基线。所有算法通过统一指标评价，包括总距离、平均响应时间、完成率、高优先级完成率、车辆利用率、未服务任务和运行时间。系统还内置六类标准场景，比如拥堵、需求激增、资源不足和道路阻塞，用来比较算法在不同约束下的表现。

在工程上，我使用 FastAPI、SQLAlchemy、PostgreSQL/PostGIS、Redis/Celery 和 pytest 做后端，用 Next.js、TypeScript、Tailwind 和 Recharts 做前端 Dashboard。前端展示的路线和图表来自真实 API 和仿真结果，不是静态假数据。这个项目让我更系统地理解了复杂系统建模、路径规划、运筹优化和全栈工程之间的联系。

---

## 4. English Interview Project Introduction

### 30-second Version

I built an Intelligent Emergency Resource Scheduling and Simulation Platform for civil emergency logistics. It models road networks, depots, vehicles, demands, congestion, and blocked roads, then compares dispatch algorithms such as Dijkstra, A*, Greedy, Priority-based dispatch, and OR-Tools CVRP. The platform records routes and metrics, visualizes results in a Next.js dashboard, and generates deterministic experiment reports.

### 1-minute Version

My project is a full-stack simulation platform for civil emergency resource scheduling. I model the city as a weighted directed graph, where edges include distance, speed, congestion factor, and blocked status. Vehicles have capacity, and demands have quantity, priority, service time, and time-window evaluation fields.

On the algorithm side, I implemented Dijkstra and A* for route planning, Greedy and Priority-based dispatch for heuristic assignment, and OR-Tools CVRP as a constrained optimization baseline. All algorithms are evaluated with the same metrics, including total distance, response time, completion rate, priority completion, vehicle utilization, unserved demands, and runtime. The system is built with FastAPI, SQLAlchemy, PostgreSQL/PostGIS, Redis/Celery, Next.js, TypeScript, and Recharts, so it demonstrates both system engineering thinking and real full-stack delivery.

---

## 5. 项目难点总结

### 1. 建模难点

难点：应急调度不是单一最短路问题，而是路网、车辆、仓库、需求、优先级、拥堵和阻塞共同作用的复杂系统。

解决：我把道路抽象为有向带权图，把仓库、车辆、需求点和算法结果拆成独立数据模型，并通过 Scenario 统一管理实验边界。

### 2. 算法难点

难点：路径规划和车辆调度不是同一个层次的问题；最短路只能解决两点之间怎么走，不能直接决定车辆任务分配。

解决：我将 Dijkstra/A* 作为路径规划子模块，再在 Greedy、Priority 和 OR-Tools CVRP 中完成车辆到需求的分配和路线生成。

### 3. 工程难点

难点：算法结果要能被 API、数据库和前端一致理解，否则路线、指标和报告会脱节。

解决：我统一了 DispatchPlan、Route、SimulationRun 和 MetricResult 的数据流，让每次仿真都能持久化、查询、展示和生成报告。

### 4. 实验难点

难点：如果只有一个正常场景，无法说明算法在不同约束下的差异，也容易变成演示型项目。

解决：我设计了六类标准 seed 场景，并用 total distance、response time、completion rate、priority completion、runtime 等指标做统一比较。

### 5. 展示难点

难点：复试老师或面试官需要快速看懂项目价值，不能只看到代码或页面。

解决：我补充了 README、系统设计、算法设计、技术报告、复试问答、英文介绍、演示脚本和报告生成模块，让项目可以从工程和研究两个角度讲清楚。

---

## 6. 复试追问答案

### 1. 为什么这不是一个简单 Web 系统？

因为 Web 只是展示层。项目核心包括复杂系统建模、图算法、车辆调度、容量约束、仿真实验、指标比较和报告生成，前端展示的是后端真实算法结果。

### 2. 这个项目为什么适合系统工程方向？

它强调系统边界、组成要素、约束、目标和评价闭环。路网、车辆、需求和道路状态共同影响调度结果，符合系统工程中建模、优化、仿真和评估的思路。

### 3. 为什么选择民用应急资源调度？

这个场景公开、安全、容易解释，同时包含资源有限、需求紧急、道路状态变化和多目标权衡，很适合作为系统工程和电子信息方向的综合项目。

### 4. 你的图模型怎么定义？

我把路网建模为有向带权图，节点是路口、仓库或需求位置，边包含距离、速度、拥堵系数和阻塞状态。路径算法在这个图上运行。

### 5. Dijkstra 和 A* 在项目里分别做什么？

Dijkstra 是非负权重图上的最短路基线；A* 在代价基础上加入地理距离启发式，用于目标导向的路径搜索。它们都服务于车辆到需求点的路径规划。

### 6. 为什么还需要调度算法？

最短路只解决“从 A 到 B 怎么走”，但调度还要解决“哪辆车服务哪个需求、按什么顺序服务”。所以路径规划只是调度的一部分。

### 7. Greedy Dispatch 的局限是什么？

它只看当前局部最优，速度快但可能牺牲全局效果。例如先服务低优先级任务后，可能导致高优先级任务服务不及时或容量不足。

### 8. Priority Dispatch 的意义是什么？

它把高优先级任务排在前面，更符合应急场景中优先保障紧急需求的原则。代价是可能增加总距离或影响低优先级任务。

### 9. 为什么使用 OR-Tools？

OR-Tools 是成熟的运筹优化工具，适合表达 CVRP 这类容量约束车辆路径问题。相比手写完整求解器，它更可靠，也便于后续扩展时间窗、惩罚项等约束。

### 10. OR-Tools 一定比启发式算法好吗？

不一定。OR-Tools 更适合全局容量约束，但运行时间可能更高；在不可行场景下也可能触发 fallback。项目用它作为对比基线，而不是绝对最优保证。

### 11. 为什么需要仿真？

单次算法输出不容易评价好坏。仿真可以在相同场景下运行多种算法，记录路线和指标，从而比较不同策略在距离、响应时间和完成率上的差异。

### 12. 你用了哪些实验指标？

主要包括 total distance、average response time、max response time、completion rate、priority completion rate、vehicle utilization、delayed demands、unserved demands 和 algorithm runtime。

### 13. 为什么不能只看总距离？

应急场景更关注任务是否完成、是否优先服务紧急需求、响应是否及时。总距离短但高优先级任务没服务，也不是好的调度方案。

### 14. weighted score 怎么理解？

它是一个可解释的综合评分。完成率和高优先级完成率权重最高，其次是响应时间，再考虑距离和算法运行时间，用于辅助比较算法。

### 15. 道路阻塞怎么处理？

道路边有 blocked 状态。构建算法图时，阻塞边不作为可通行边参与路径搜索，因此路径规划会自动绕开这些道路，无法到达时需求可能未服务。

### 16. 拥堵怎么影响结果？

拥堵通过 congestion factor 放大通行时间。按时间成本规划或调度时，拥堵边会变得更“贵”，从而影响路线选择和响应时间。

### 17. 你的个人贡献是什么？

我完成了问题建模、数据库模型、seed 场景、核心调度算法、后端 API、前端 Dashboard、指标比较、报告生成、测试和复试文档整理。

### 18. 项目目前有哪些不足？

目前是可演示 MVP，还没有实时动态重优化、完整硬约束 VRPTW、真实城市地图接入和 PDF 报告导出，前端组件测试也可以继续补充。

### 19. 如果需求动态变化，你会怎么改？

我会做 rolling-horizon re-optimization，周期性读取新增需求和车辆状态，保留已完成任务，对剩余车辆和需求重新规划。

### 20. 如果继续做研究生阶段扩展，你会做什么？

我会重点扩展真实路网数据、完整 VRPTW、多目标优化、动态重调度和批量仿真实验，让项目从可演示平台进一步走向系统工程研究原型。
