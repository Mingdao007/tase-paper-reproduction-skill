# tase-paper-reproduction-skill

English README: [README.md](README.md)

这是一个私有 Codex skill 仓库，专门服务当前这篇 TASE 论文在本机上的复现：

- 论文：Xu 等，2026，Finite-Time Convergence Neural Network-Based Force-Motion Control for Unknown Surface With Orientation Compliance
- 本地代码基线：`/home/andy/Documents/UR5e_ws/RNN_F2`

## 覆盖问题

- 审计当前 `RNN_F2` 复现和 paper Fig.5 / Fig.6 的差异
- 解释为什么当前结果还不满足 paper
- 固定区分 `paper_ideal` 与 `step_surface`
- 每次仿真后输出固定 Markdown 表格
- 交接当前复现状态、假设和 gap

## 当前状态

- `paper_first` 可运行
- Fig.5 风格的内环误差趋势已部分对上
- Fig.6(c) `force error` 仍未实现
- 当前还不能宣称 paper-faithful reproduction

## 主要内容

- `tase-paper-reproduction/`: 可安装 skill 包
- `tase-paper-reproduction/references/`: 论文真值、repo 地图、gap 审计、force-loop 路线、报告契约
- `tase-paper-reproduction/scripts/summarize_tase_results.py`: `.mat -> Markdown 表格` 工具
- `tase-paper-reproduction/agents/openai.yaml`: Codex 元数据

## 安装

1. 把 `tase-paper-reproduction/` 复制到 `${CODEX_HOME:-$HOME/.codex}/skills/`。
2. 重启 Codex，或者刷新本地 skills。
3. 通过 `$tase-paper-reproduction` 调用这个 skill。

## 边界

这个仓库是窄范围私有 skill，不是通用的机器人控制论文复现框架，也不包含本地 PDF、STEP 或 MATLAB 结果文件。
