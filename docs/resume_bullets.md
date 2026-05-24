# Resume Bullets

## 中文简历项目描述

- 构建面向民用应急资源调度的全栈仿真平台，将城市路网、仓库、车辆、需求点、拥堵和道路阻塞建模为可持久化的复杂系统对象，支持场景管理、仿真运行、路线可视化和报告生成。
- 基于 NetworkX 实现 Dijkstra 与 A* 路径规划，并实现 Greedy Dispatch、Priority Dispatch 与 OR-Tools CVRP 调度基线，支持车辆容量、需求优先级、服务时间、拥堵和阻塞边等约束。
- 设计六类标准实验场景，构建 total distance、average response time、completion rate、priority completion rate、vehicle utilization、runtime 等指标体系，并实现 weighted score 综合评价模型。
- 使用 FastAPI、SQLAlchemy、PostgreSQL/PostGIS、Redis/Celery、Next.js、TypeScript、Recharts 和 Docker Compose 完成前后端闭环工程，实现真实 API、真实算法结果、测试覆盖和可复现实验文档。

## English Resume Bullets

- Built a full-stack civil emergency resource scheduling and simulation platform that models road networks, depots, vehicles, demands, congestion, and blocked roads as persistent complex-system entities.
- Implemented Dijkstra and A* path planning with NetworkX, plus Greedy Dispatch, Priority-based Dispatch, and an OR-Tools CVRP baseline under capacity, priority, service-time, congestion, and blocked-edge constraints.
- Designed six benchmark scenarios and a multi-metric evaluation framework covering total distance, response time, completion rate, priority completion, vehicle utilization, unserved demands, and algorithm runtime.
- Delivered a reproducible engineering stack with FastAPI, SQLAlchemy, PostgreSQL/PostGIS, Redis/Celery, Next.js, TypeScript, Recharts, Docker Compose, pytest, OpenAPI docs, and deterministic experiment report generation.
