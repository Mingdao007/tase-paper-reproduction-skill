# Report Table Contract

After every simulation run, return these four Markdown tables in this order.

## 1. Run Summary

| Field | Value |
|---|---|
| Run type | |
| Result file | |
| Branch | |
| Dirty state | |
| Duration / steps | |
| Key final metrics | |

## 2. Current vs Paper

| Paper item | Paper truth | Current result | Verdict |
|---|---|---|---|
| Fig. 6(c) force error | `fd = 5 N` and convergent force error curve | | `match / partial / missing / mismatch` |
| `q7 @ 22 s` | seventh joint reaches limit | | |
| Joint velocity pattern | start-up velocity limit hit | | |
| Position error | convergent | | |
| Orientation error | convergent | | |
| Scene assumptions | paper simulation scene | | |

## 3. Blocking Gaps

| Gap | Evidence | Why it blocks paper-faithful claim |
|---|---|---|
| | | |

## 4. Next Single Action

| Priority | Action | Expected effect |
|---|---|---|
| 1 | | |

## Wording rules

- Use `missing` when a subsystem does not exist.
- Use `mismatch` when the subsystem exists but behaves differently.
- Use `partial` when the trend matches but the scene or signals still differ materially.
- Do not replace these tables with prose.
