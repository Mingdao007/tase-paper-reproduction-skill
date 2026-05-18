# RNN_F2 Repo Map

Local working repo root:

- `/home/andy/Documents/UR5e_ws/RNN_F2`

Original baseline source of truth:

- `/home/andy/Documents/UR5e_ws/RNN_F2_baseline`

## Key files

| Path | Role | Notes |
|---|---|---|
| `../RNN_F2_baseline/main.m` | Original as-received baseline | Primary source of truth for the supplied code |
| `main.m` | Mirror copy of baseline main | Matches `RNN_F2_baseline/main.m` |
| `../RNN_F2_baseline/forward.m` | Original baseline forward kinematics | Source of truth for legacy baseline behavior |
| `../RNN_F2_baseline/getJacobian.m` | Original baseline Jacobian | Source of truth for legacy baseline behavior |
| `config_audit.m` | Current parameter registry | Mixes `from_rnn_f2`, `from_paper`, and `assumed` |
| `run_baseline.m` | Batch baseline entry | Later wrapper for export and comparison, not the original baseline itself |
| `run_paper_first.m` | Current paper-inspired line | Uses DH Panda, STP surface, `q0_contact`, `normal-only` orientation |
| `plot_paper_first.m` | Current figure export | Exports 7 PNGs, not full paper contract |
| `surface_bspline.m` | Local STP-derived B-spline surface | Geometry proxy, not paper truth |
| `forward_panda.m` | Current Panda forward kinematics | Replaces broken legacy kinematics |
| `getJacobian_panda.m` | Current Panda Jacobian | Consistent with `forward_panda.m` |
| `find_q0_contact.m` | IK helper for contact start | Produces `q0_contact`, not paper `q0` |
| `verify_paper_first.m` | Verification helper | Local audit utility |

## Result landmarks

| Path | Meaning |
|---|---|
| `results/paper_first/paper_first_results.mat` | Current paper-first result bundle |
| `results/paper_first/fig1_position_error.png` | Position error figure |
| `results/paper_first/fig2_orientation_error.png` | Orientation error figure |
| `results/paper_first/fig3_joint_angles.png` | Joint angle figure |
| `results/paper_first/fig4_joint_velocities.png` | Joint velocity figure |
| `results/paper_first/fig5_constraint_error.png` | Inner-loop constraint residual |
| `results/paper_first/fig6_lagrange_multipliers.png` | Intermediate variable `λ` |
| `results/paper_first/fig7_surface_normal.png` | Local extra diagnostic |

## Important boundary

When the user says `baseline`, `original code`, or `code-first`, default to `RNN_F2_baseline/` as the reference source, not `run_baseline.m`.

`run_paper_first.m` is an exploratory bridge. It does not yet implement:

- contact force model
- normal force control loop
- force error logging
- paper-faithful `paper_ideal` trajectory/limit scene separated from STEP scene
