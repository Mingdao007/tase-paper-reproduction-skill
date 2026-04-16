---
name: tase-paper-reproduction
description: Use when auditing, iterating, or handing off the Xu et al. 2026 IEEE TASE simulation reproduction in `/home/andy/Documents/UR5e_ws/RNN_F2`, especially for `RNN_F2`, `paper-first`, `Fig. 5`, `Fig. 6`, `force error`, `q7@22s`, `paper gap audit`, and post-run result reporting against the paper.
---

# TASE Paper Reproduction

Use this skill for the current local reproduction of:

- Xu et al., "Finite-Time Convergence Neural Network-Based Force-Motion Control for Unknown Surface With Orientation Compliance"
- local code baseline: `/home/andy/Documents/UR5e_ws/RNN_F2`
- current working line: `baseline_rnn_f2`, `paper_first`, or future `paper_ideal` / `step_surface`

This skill is narrow on purpose. It is not a generic robot-control paper skill.

## Workflow

1. Read `references/paper-truth.md` before making claims about whether a run matches the paper.
2. Read `references/current-gap-audit.md` to understand what is still missing or structurally different.
3. Read `references/repo-map-rnn-f2.md` before editing or reviewing code paths in `RNN_F2`.
4. Classify the current run as one of:
   - `baseline_rnn_f2`
   - `paper_first`
   - `paper_ideal`
   - `step_surface`
5. If the user asks for current status after a run, use `scripts/summarize_tase_results.py` on the `.mat` result first.
6. By default, generate a human-friendly Markdown report file next to the `.mat` result using the contract in `references/report-table-contract.md`.
7. In chat, give only a short verdict, the biggest remaining mismatch, and the report path unless the user explicitly asks for the full content inline.
8. If the result is missing `force error`, say it is an unimplemented subsystem, not a tuning issue.
9. If a run mixes paper-style claims with STEP geometry or `q0_contact`, call out that it is not paper-faithful.

## Decision Rules

- Treat the paper PDF and `references/paper-truth.md` as the source of truth for `q0`, limits, Fig. 5 timings, and the declared Fig. 6 channels.
- Treat `run_paper_first.m` as an exploratory bridge, not as proof that the paper was reproduced.
- Keep `paper_ideal` and `step_surface` separate. Do not collapse them into one line of results.
- Keep `normal-only` orientation reporting unless a better paper-faithful orientation specification is discovered.
- Do not claim Fig. 6 is matched while `force error` is absent.
- Do not treat `q7@22s` mismatch as a simple gain issue when the current run changed initial state, limits, and geometry.

## Result Contract

After every simulation run:

1. Generate one Markdown report file next to the `.mat` result.
2. Use the section structure and wording rules from `references/report-table-contract.md`.
3. In chat, summarize the report in 2-4 short lines instead of dumping wide tables.

## Force-Loop Priority

If the user asks what to do next for closer Fig. 6 matching:

1. Read `references/force-loop-roadmap.md`
2. Prioritize the smallest viable `force/contact` chain:
   - contact normal
   - normal force model
   - `fd = 5 N`
   - force error logging
   - tangential vs normal task split
3. Only after that, push on `q7@22s`, early velocity saturation shape, and the `19–20 s` spike

## References

- `references/paper-truth.md`
- `references/current-gap-audit.md`
- `references/repo-map-rnn-f2.md`
- `references/force-loop-roadmap.md`
- `references/report-table-contract.md`
- `references/branch-and-handoff.md`

## Script

Use this helper after runs:

```bash
python3 tase-paper-reproduction/scripts/summarize_tase_results.py \
  --mat /home/andy/Documents/UR5e_ws/RNN_F2/results/paper_first/paper_first_results.mat \
  --run-type paper_first \
  --repo /home/andy/Documents/UR5e_ws/RNN_F2
```
