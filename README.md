# tase-paper-reproduction-skill

Private Codex skill for the current local reproduction of Xu et al. 2026 IEEE
TASE paper "Finite-Time Convergence Neural Network-Based Force-Motion Control
for Unknown Surface With Orientation Compliance".

Chinese mirror: [README.zh-CN.md](README.zh-CN.md)

## Current Baseline

| Item | Status |
|---|---|
| Local code baseline | `/home/andy/Documents/UR5e_ws/RNN_F2` |
| Current runnable line | `paper_first` |
| Fig. 5 style inner-loop trend | Partially reproduced |
| Fig. 6 force error | Missing |
| Paper-faithful reproduction | Not achieved |
| Post-run paper gap tables | Included in this repo |

## Problems Covered

- Audit the current `RNN_F2` reproduction against paper Fig. 5 and Fig. 6
- Explain why current runs do not yet match the paper
- Keep `paper_ideal` and `step_surface` lines separate
- Produce fixed Markdown tables after each simulation run
- Hand off the current reproduction state without losing assumptions or gaps

## What Ships

- `tase-paper-reproduction/`: installable Codex skill package
- `tase-paper-reproduction/references/`: paper truths, repo map, gap audit, force-loop roadmap, report contract
- `tase-paper-reproduction/scripts/summarize_tase_results.py`: `.mat` to Markdown summary helper
- `tase-paper-reproduction/agents/openai.yaml`: Codex metadata

## Install

1. Copy `tase-paper-reproduction/` into `${CODEX_HOME:-$HOME/.codex}/skills/`.
2. Restart Codex or refresh local skills.
3. Invoke the skill as `$tase-paper-reproduction`.

## Scope Boundary

This repo is intentionally narrow and private. It tracks one paper, one local
workspace, and one evolving reproduction effort. It does not try to be a
generic robot-control paper reproduction framework.

## Privacy Boundary

This repository contains workflow guidance and helper logic only. It does not
ship the paper PDF, Zotero storage, STEP files, or local MATLAB result data.
