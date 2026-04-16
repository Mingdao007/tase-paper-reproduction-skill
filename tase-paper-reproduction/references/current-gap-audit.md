# Current Gap Audit

Current audited result:

- `paper_first`
- result file: `/home/andy/Documents/UR5e_ws/RNN_F2/results/paper_first/paper_first_results.mat`

## Gap table

| Topic | Current status | Why it differs from paper | Gap type |
|---|---|---|---|
| Fig. 6(c) force error | Missing | No contact model, no force loop, no force state, no `fd = 5 N` closed loop | Unimplemented subsystem |
| `q7 @ 22 s` | Not matched | Current run uses `q0_contact`, STEP geometry, and `±2.6` soft bounds | Experimental design gap |
| Early velocity saturation | Not matched | Saturation is dominated by a late spike near `19–20 s`, not a paper-like start-up pattern | Behavioral mismatch |
| `19–20 s` spike | Still present | Likely limit/projection/geometry interaction under the current assumptions | Structural distortion |
| Position error plot | Incomplete paper contract | Current plot only tracks tangential channels directly | Reporting mismatch |
| Orientation error plot | Proxy only | Uses `normal-only` orientation because paper `u` is ambiguous | Ambiguous paper + proxy |

## Current measured facts

| Item | Current value |
|---|---|
| `q7(22 s)` | about `0.863 rad` |
| First soft-limit hit | joint 4 near `12.95 s` |
| Peak velocity saturation times | concentrated around `18.85 s` to `19.69 s` |
| Force error | unavailable |
| Inner-loop residual end value | near zero in current stable run |

## What to say explicitly

- The current controller is runnable and convergent.
- It is not yet a faithful reproduction of paper Fig. 6.
- Force error absence is not a plotting omission. It is a missing control and contact subsystem.
