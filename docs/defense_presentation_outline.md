# 复试答辩 PPT 大纲

建议页数：10 页  
建议时长：5-8 分钟主讲，后续根据老师提问展开算法、系统工程或工程实现细节。

---

## Slide 1：项目标题与个人背景

**标题**  
面向应急资源调度的复杂系统建模、优化与仿真平台  
Intelligent Emergency Resource Scheduling & Simulation Platform

**核心内容**
- 本科专业：数据科学与大数据技术；
- 目标方向：电子信息 0854，关注系统工程、优化决策和智能信息系统；
- 项目定位：民用应急物流调度平台，不涉及军事或涉密场景。

**建议放置的图**
- 项目首页截图；
- 一张简洁的系统闭环图：场景输入 -> 算法调度 -> 仿真指标 -> 报告输出。

**我该怎么讲**
> 老师好，我的项目聚焦公开民用应急资源调度。我希望通过这个项目展示自己把复杂系统问题转化为数据模型、优化算法、仿真实验和全栈工程系统的能力。

---

## Slide 2：为什么选择这个问题

**标题**  
从应急物流出发的复杂系统优化问题

**核心内容**
- 应急场景中资源有限、需求紧急、道路状态不确定；
- 不能只看最短距离，还要看响应时间、任务完成率和高优先级保障；
- 适合体现系统工程中的建模、约束、优化和评估。

**建议放置的图**
- 城市路网、仓库、车辆和需求点示意图；
- Normal / Congestion / Blocked Road 三种场景对比小图。

**我该怎么讲**
> 我选择这个问题是因为它天然包含多个子系统：道路网络、车辆资源、需求任务和调度策略。它不是单一算法题，而是一个需要综合权衡的系统决策问题。

---

## Slide 3：系统架构

**标题**  
前后端分离的仿真实验平台

**核心内容**
- 前端：Next.js、TypeScript、Tailwind CSS、Recharts；
- 后端：FastAPI、SQLAlchemy、Pydantic、Alembic；
- 数据与任务：PostgreSQL/PostGIS、Redis、Celery worker；
- 算法：NetworkX、OR-Tools、自研 dispatch 策略；
- 输出：路线、指标、算法对比和 Markdown 实验报告。

**建议放置的图**
- README 中的 Mermaid 架构图；
- API -> Algorithm -> Metrics -> Database 的数据流图。

**我该怎么讲**
> 系统不是只做页面展示，前端所有图表和路线都来自后端真实 API。后端把场景数据转成图模型，运行算法，再把方案、路线和指标持久化。

---

## Slide 4：问题建模

**标题**  
从城市应急调度到图模型与约束模型

**核心内容**
- 路网：有向带权图 `G=(V,E)`；
- 节点：交叉口、仓库位置、车辆起点、需求点；
- 边：距离、速度、拥堵系数、阻塞状态；
- 资源：车辆容量、仓库、需求量、优先级、服务时间；
- 决策：车辆分配、服务顺序、节点路径。

**建议放置的图**
- 数据模型 ER 简图；
- 图模型示意：node / edge / depot / vehicle / demand。

**我该怎么讲**
> 我把道路抽象成有向图，路径规划在图上完成；把车辆和需求抽象成资源分配问题，调度算法需要同时考虑容量、道路状态和任务优先级。

---

## Slide 5：算法设计

**标题**  
路径规划 + 调度优化 + 统一指标评价

**核心内容**
- Dijkstra：非负权重最短路基线；
- A*：加入地理距离启发式；
- Greedy Dispatch：快速可解释基线；
- Priority Dispatch：优先保障高优先级任务；
- OR-Tools CVRP：容量约束车辆路径问题基线。

**建议放置的图**
- 算法流程图；
- 一张表对比算法输入、优点、局限和适用场景。

**我该怎么讲**
> Dijkstra 和 A* 解决点到点路径规划，Dispatch 算法解决“车辆服务哪些需求、按什么顺序服务”。OR-Tools CVRP 用来提供运筹优化基线，特别适合解释容量约束。

---

## Slide 6：系统实现

**标题**  
真实 API、真实算法结果和真实可视化

**核心内容**
- REST API：scenario、network、run、routes、metrics、compare、report；
- 数据库表：Scenario、Node、Edge、Depot、Vehicle、Demand、DispatchPlan、Route、SimulationRun、MetricResult、AlgorithmConfig；
- 前端页面：场景管理、路网可视化、仿真控制、结果仪表盘、报告生成；
- 测试：pytest 覆盖算法、seed、API 和 report。

**建议放置的图**
- Swagger 页面截图；
- Results Dashboard 截图；
- 数据表或 API 列表示意。

**我该怎么讲**
> 我重点保证了从数据库到算法再到前端展示的真实数据流。例如运行一次仿真后，系统会保存 SimulationRun、DispatchPlan、Route 和 MetricResult，前端再读取这些结果展示。

---

## Slide 7：实验设计

**标题**  
六类标准场景构成实验基准

**核心内容**
- Normal Scenario：基准组；
- Congestion Scenario：道路拥堵；
- Demand Surge Scenario：需求激增；
- Resource Shortage Scenario：车辆和容量不足；
- Blocked Road Scenario：关键道路不可通行；
- High Priority Rescue Scenario：高优先级需求集中。

**建议放置的图**
- 六类场景表；
- `/scenarios` 页面截图。

**我该怎么讲**
> 我没有只做一个简单 demo，而是设计了不同压力条件下的实验场景。这样可以观察算法在正常、拥堵、阻塞、资源不足和高优先级任务下的差异。

---

## Slide 8：实验结果

**标题**  
多指标算法对比与综合评分

**核心内容**
- 指标：total distance、average response time、completion rate、priority completion rate、vehicle utilization、runtime 等；
- 图表：距离、响应时间、完成率、优先级完成率、运行时间；
- 综合评分：completion 0.30、priority 0.25、response 0.20、distance 0.15、runtime 0.10；
- 报告：deterministic Markdown report，可选 LLM 润色。

**建议放置的图**
- `/results` 页面柱状图和 weighted score 表；
- `/report` 页面截图。

**我该怎么讲**
> 我不会只说某个算法最好，而是先看原始指标，再看综合评分。比如应急场景下完成率和高优先级完成率权重更高，距离和运行时间是辅助指标。

---

## Slide 9：不足与改进

**标题**  
当前边界与下一步研究方向

**核心内容**
- 当前需求和道路状态主要是静态场景；
- 时间窗目前用于延迟评估，完整 VRPTW 还未实现；
- 路网是 seed 网格，不是真实城市地图；
- 前端测试和实验批处理还可以继续完善。

**建议放置的图**
- Roadmap 时间线；
- Static snapshot -> rolling horizon 的改进示意。

**我该怎么讲**
> 我会如实说明当前项目是可运行 MVP，不把未来工作说成已实现。下一步最有研究价值的是动态需求下的滚动重优化和完整 VRPTW。

---

## Slide 10：与电子信息/系统工程方向的关系

**标题**  
从信息系统到系统优化决策

**核心内容**
- 电子信息：数据采集建模、API 系统、可视化、AI 辅助报告；
- 系统工程：系统边界、模型、约束、目标函数、仿真评估；
- 运筹优化：VRP/CVRP、容量约束、多目标评价；
- 数据结构与算法：图结构、最短路、启发式搜索、调度策略；
- 研究生阶段延展：复杂系统建模、智能决策、仿真实验和优化算法。

**建议放置的图**
- 四象限图：System Engineering / OR / AI Decision Support / Full-stack Engineering。

**我该怎么讲**
> 这个项目和电子信息方向的关系在于，它不是单独做算法，而是把算法变成可交互、可复现、可评估的信息系统；和系统工程的关系在于，它强调建模、优化、仿真和评价闭环。
