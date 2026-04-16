# Branch And Handoff

## Current local repo status

- Repo: `/home/andy/Documents/UR5e_ws/RNN_F2`
- Current working branch during the latest audit: `fix/paper-first-kkt-inner-loop`
- Current worktree is dirty and contains paper-first files that are not yet part of the original baseline

## Branch rules

- Keep `baseline_rnn_f2` logic untouched when working on `paper_first`
- Use a fresh branch when making a new conceptual jump, such as:
  - adding force loop
  - splitting `paper_ideal` from `step_surface`
  - replacing orientation representation
- Do not silently reuse `paper_first` as if it were the paper ground truth

## Handoff rules

When handing off to another agent or engineer, include:

| Item | Required content |
|---|---|
| Goal | Which scene is being targeted: `baseline_rnn_f2`, `paper_first`, `paper_ideal`, or `step_surface` |
| Branch | Exact current branch |
| Dirty state | Whether the worktree contains uncommitted files |
| Paper truth | Any paper-side values being claimed |
| Missing subsystem | Force loop/contact/orientation ambiguity status |
| Last result | Exact `.mat` or figure paths |

## Non-negotiable wording

- Say `paper-inspired` when the current line still uses assumed scene geometry
- Say `paper-faithful` only when the run includes paper-consistent scene, limits, and force-error chain
