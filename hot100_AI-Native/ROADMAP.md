# Hot100 Agent 路线图

## 核心原则（来自面试官标准）

本项目按 AI 应用工程岗位的真实评审标准设计，重点不在"调通 LLM"，
而在三个维度：

### 1. Evaluation 严谨性
- 构建 ground truth 数据集（目标 500+ 问题）
- 定义 TP/FP/TN/FN 在每个场景下的含义
- 自动化评测 + 失败模式分类（幻觉 vs 检索 vs prompt）
- 追踪指标随版本演化

### 2. 工程自动化
- 单元测试覆盖核心逻辑
- GitHub Actions CI
- 环境一键复现
- 评测自动化

### 3. 项目管理痕迹
- Milestone + Issue 管理
- ADR（架构决策记录）
- CHANGELOG 维护
- 清晰的目录结构

## 版本规划

### v0.1（5/31 完成）
- ✅ 环境搭建 + API 调通
- ✅ 6 题 hot100 子集 demo

### v0.2（暑期前半 7/15-8/4）
- [ ] Schema 扩展（hot100 + carl）
- [ ] SQLite 持久层
- [ ] Ground truth 数据集 v0.1（50 个问题）
- [ ] 单元测试基础

### v0.3（暑期中段 8/5-8/15）
- [ ] Evaluation 自动化脚本
- [ ] GitHub Actions CI
- [ ] 错误模式库 v0.1（基于 6 月刷题日志提炼）

### v1.0（暑期末 8/16-8/31）
- [ ] 完整 Agent 流程
- [ ] 项目文档化（README / ADR / CHANGELOG）
- [ ] 部署 + Demo 视频