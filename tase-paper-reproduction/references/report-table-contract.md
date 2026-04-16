# Human-Friendly Run Report Contract

After every simulation run, generate one Markdown report file. The file should be easy to scan in a text editor and should not rely on wide tables.

## Required sections

### 1. `Quick Verdict`

Use 3-4 bullets:

- `Current verdict`: one sentence such as `not paper-faithful yet`, `partial match`, or `close on Fig. 6 except ...`
- `Best-matching part`: what currently looks most like the paper
- `Biggest blocker`: the one issue that most clearly prevents a paper-faithful claim
- `Next step`: exactly one next action

### 2. `Run Snapshot`

Use short bullets, not a wide table:

- `Run type`
- `Result file`
- `Branch / commit`
- `Dirty state`
- `Duration / steps`
- `Key end metrics`

### 3. `Current vs Paper`

Use one flat bullet per item in this shape:

- `Fig. 6(c) force error`: `[Match|Partial|Missing|Mismatch]` short plain-language comparison
- `q7 @ 22 s`: ...
- `Joint velocity pattern`: ...
- `Position error`: ...
- `Orientation error`: ...
- `Scene assumptions`: ...

Each bullet should lead with the verdict tag so the user can skim quickly.

### 4. `Blocking Gaps`

Use 2-5 bullets. Each bullet should include:

- the gap name
- the concrete evidence
- why it blocks a paper-faithful claim

### 5. `Next Single Action`

Use exactly one bullet:

- the next action
- why it is the highest-leverage move now

## Optional appendix

Small two-column tables are allowed only for compact metric snapshots. Do not use large four-column audit tables unless the user explicitly asks for them.

## Wording rules

- Use `Missing` when a subsystem does not exist.
- Use `Mismatch` when the subsystem exists but behaves differently.
- Use `Partial` when the trend matches but the scene or signals still differ materially.
- Use `Match` only when the item is genuinely close enough to support a paper-side claim.
- Prefer plain language over audit jargon.
- The chat reply after a run should be 2-4 short lines plus the report path, unless the user explicitly asks to read the full report inline.
