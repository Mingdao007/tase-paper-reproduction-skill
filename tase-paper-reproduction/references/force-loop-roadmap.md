# Force-Loop Roadmap

This is the next-priority roadmap for getting closer to paper Fig. 6.

## First milestone: smallest viable force chain

Add these in this order:

1. Contact normal definition for the active scene
2. Normal reaction model
3. Desired normal force `fd = 5 N`
4. Force error logging
5. Tangential motion vs normal force task split

Do not skip directly to gain tuning before these exist.

## Minimum implementation shape

### `paper_ideal`

- Use the paper `q0`
- Use paper joint angle bounds `±2.5 rad`
- Use paper joint velocity bounds `±1.5 rad/s`
- Use ideal task-space circular path
- Use a controlled normal direction and force model

### `step_surface`

- Keep `q0_contact`
- Keep real STP geometry
- Keep local surface normals
- Use this line for realism and geometry testing, not for paper-faithful claims

## Why force error is currently absent

The current `run_paper_first.m` only computes:

- kinematics
- task-space tracking error
- projected inner-loop dynamics
- `λ`

It does not compute:

- penetration or signed distance
- contact stiffness or damping response
- measured normal force
- desired-vs-measured force error

## What to diagnose after force-loop exists

Add these diagnostics before chasing the `19–20 s` spike:

- `cond(J)`
- active velocity clamps
- active joint-angle proximity to bounds
- `qdot_proj_raw` vs `qdot_proj`
- normal direction change rate
- tangential vs normal task error

## Priority rule

If the user asks "why not just tune the spike first", answer:

- because Fig. 6(c) is still absent
- because `q7@22s` and velocity-shape mismatch are scene-design dependent
- because force/contact completion changes the motion distribution itself
