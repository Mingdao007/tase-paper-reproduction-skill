# Paper Truth

Use this file before judging whether a run matches the paper.

## Paper

- Xu et al., 2026
- "Finite-Time Convergence Neural Network-Based Force-Motion Control for Unknown Surface With Orientation Compliance"
- Local PDF:
  `/home/andy/Zotero/storage/UZRF97KG/Xu 等 - 2026 - Finite-Time Convergence Neural Network-Based Force-Motion Control for Unknown Surface With Orientati.pdf`

## Directly stated simulation truths

| Item | Paper statement |
|---|---|
| Initial joint angle | `q0 = [0; -π/4; 0; -3π/4; 0; π/2; π/4]` |
| Desired free-motion trajectory | `xpd = [0.2 cos(0.2t); 0.2 sin(0.2t); z0]` |
| Orientation specification | `u = [cos(0.1t), sin(0.1t)]` appears in the text, but this is dimensionally inconsistent with the paper's earlier 3D `u` definition |
| Joint angle limits | `±2.5 rad` |
| Joint velocity limits | `±1.5 rad/s` |
| Desired normal force | `fd = 5 N` |

## Fig. 5 truths

| r | Reported convergence time |
|---|---|
| 0.2 | `0.15 s` with noticeable early instability |
| 0.4 | `0.26 s` |
| 0.6 | `0.38 s` |
| 0.8 | `0.55 s` |
| 1.0 | `0.89 s` |

The paper states that larger `r` yields slower but more stable convergence.

## Fig. 6 channel definitions

| Panel | Meaning |
|---|---|
| (a) | Joint velocities |
| (b) | Joint angles |
| (c) | Force error |
| (d) | Intermediate variable `λ` |
| (e) | Position error |
| (f) | Orientation error |

## Paper-side claims to test against

- At the start of the motion, joint velocity reaches the predefined limit.
- At `t = 22 s`, the seventh joint angle reaches its limit.
- Position error, orientation error, and force error all converge.

## Interpretation guardrails

- Do not call a run paper-faithful if it omits force error.
- Do not silently replace the paper's `q0`, limits, or ideal trajectory and then claim Fig. 6 has been matched.
- Treat the published `u = [cos(0.1t), sin(0.1t)]` as an unresolved ambiguity that needs explicit labeling in any audit.
