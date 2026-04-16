#!/usr/bin/env python3
"""Summarize current TASE MATLAB result files into fixed Markdown tables."""

from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.io import loadmat


PAPER_Q0 = np.array([0.0, -math.pi / 4, 0.0, -3 * math.pi / 4, 0.0, math.pi / 2, math.pi / 4])
PAPER_JOINT_LIMIT = 2.5
PAPER_VEL_LIMIT = 1.5


def fmt_float(value: float, digits: int = 4) -> str:
    if math.isnan(value):
        return "n/a"
    return f"{value:.{digits}f}"


def fmt_vec(values: Iterable[float], digits: int = 4) -> str:
    arr = np.asarray(list(values), dtype=float)
    return "[" + ", ".join(f"{x:.{digits}f}" for x in arr) + "]"


def git_value(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "n/a"
    return result.stdout.strip()


def verdict(match: bool, partial: bool = False, missing: bool = False) -> str:
    if missing:
        return "missing"
    if match:
        return "match"
    if partial:
        return "partial"
    return "mismatch"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mat", required=True, help="Path to MATLAB .mat result file")
    parser.add_argument("--run-type", required=True, help="Run label such as paper_first")
    parser.add_argument("--repo", required=True, help="Path to git repo that produced the run")
    args = parser.parse_args()

    mat_path = Path(args.mat).expanduser().resolve()
    repo_path = Path(args.repo).expanduser().resolve()
    data = loadmat(mat_path)

    t = np.asarray(data["t_save"]).reshape(-1)
    e = np.asarray(data["e_save"])
    q = np.asarray(data["q_save"])
    dq = np.asarray(data["dq_save"])
    E = np.asarray(data["E_save"]).reshape(-1)
    lam = np.asarray(data["lambda_1_save"]) if "lambda_1_save" in data else None
    cfg = data.get("cfg")

    has_force = "force_error_save" in data or "f_err_save" in data or "force_save" in data
    has_position_channels = e.shape[1] >= 3
    has_orientation_channels = e.shape[1] >= 6

    q0_current = q[0]
    idx_22 = int(np.argmin(np.abs(t - 22.0)))
    q7_22 = float(q[idx_22, 6]) if q.shape[1] >= 7 else float("nan")
    q_abs_max = np.max(np.abs(q), axis=0)
    dq_abs_max = np.max(np.abs(dq), axis=0)
    near_vel_limit = bool(np.any(np.isclose(dq_abs_max, PAPER_VEL_LIMIT, atol=5e-3)))
    first_limit_idx = np.where(np.any(np.isclose(np.abs(q), PAPER_JOINT_LIMIT, atol=5e-3), axis=1))[0]
    first_limit_text = "none"
    if first_limit_idx.size:
        first_i = int(first_limit_idx[0])
        joints = np.where(np.isclose(np.abs(q[first_i]), PAPER_JOINT_LIMIT, atol=5e-3))[0] + 1
        first_limit_text = f"t={t[first_i]:.3f}s joints={','.join(map(str, joints.tolist()))}"

    branch = git_value(repo_path, "branch", "--show-current")
    dirty = "dirty" if git_value(repo_path, "status", "--short") else "clean"
    commit = git_value(repo_path, "rev-parse", "--short", "HEAD")

    pos_final = e[-1, :3] if has_position_channels else np.array([])
    ori_final = e[-1, 3:6] if has_orientation_channels else np.array([])
    pos_max = np.max(np.abs(e[:, :3]), axis=0) if has_position_channels else np.array([])
    ori_max = np.max(np.abs(e[:, 3:6]), axis=0) if has_orientation_channels else np.array([])
    force_series = None
    if has_force:
        for key in ("force_error_save", "f_err_save", "force_save"):
            if key in data:
                force_series = np.asarray(data[key]).reshape(-1)
                break
    force_converged = False
    force_partial = False
    if force_series is not None:
        tail = force_series[max(0, len(force_series) - 5000):]
        tail_mean_abs = float(np.mean(np.abs(tail)))
        final_force_abs = float(abs(force_series[-1]))
        force_converged = tail_mean_abs < 1.0 and final_force_abs < 1.0
        force_partial = tail_mean_abs < 2.0 and final_force_abs < 2.0

    q0_matches = np.allclose(q0_current, PAPER_Q0, atol=1e-3)
    q7_match = abs(abs(q7_22) - PAPER_JOINT_LIMIT) <= 5e-2

    print("| Field | Value |")
    print("|---|---|")
    print(f"| Run type | `{args.run_type}` |")
    print(f"| Result file | `{mat_path}` |")
    print(f"| Branch | `{branch}` (`{commit}`) |")
    print(f"| Dirty state | `{dirty}` |")
    print(f"| Duration / steps | `{fmt_float(float(t[-1]), 3)} s / {len(t)}` |")
    print(f"| Key final metrics | `E_end={fmt_float(float(E[-1]), 6)}`, `q7@22s={fmt_float(q7_22, 4)}` |")
    print()

    print("| Paper item | Paper truth | Current result | Verdict |")
    print("|---|---|---|---|")
    print(
        f"| Fig. 6(c) force error | `fd = 5 N` and convergent force error curve | "
        f"{'force variable present' if has_force else 'no force-error state in .mat'} | "
        f"{verdict(force_converged, partial=force_partial, missing=not has_force)} |"
    )
    print(
        f"| `q7 @ 22 s` | seventh joint reaches `±2.5 rad` | "
        f"`q7(22s)={fmt_float(q7_22, 4)}` | {verdict(q7_match)} |"
    )
    print(
        f"| Joint velocity pattern | start-up velocity limit hit | "
        f"`max|dq|={fmt_vec(dq_abs_max, 3)}` | {verdict(False, partial=near_vel_limit)} |"
    )
    print(
        f"| Position error | convergent | `final={fmt_vec(pos_final, 6)}`, `max={fmt_vec(pos_max, 4)}` | "
        f"{verdict(np.linalg.norm(pos_final) < 5e-3, partial=True)} |"
    )
    print(
        f"| Orientation error | convergent | `final={fmt_vec(ori_final, 6)}`, `max={fmt_vec(ori_max, 4)}` | "
        f"{verdict(np.linalg.norm(ori_final) < 5e-3, partial=True)} |"
    )
    print(
        f"| Scene assumptions | paper simulation scene | "
        f"`q0_match={q0_matches}`, `first_limit={first_limit_text}` | "
        f"{verdict(q0_matches and q7_match)} |"
    )
    print()

    print("| Gap | Evidence | Why it blocks paper-faithful claim |")
    print("|---|---|---|")
    if not has_force:
        print("| Force loop absent | No force-error variable saved in the result file | Fig. 6(c) cannot be claimed or compared |")
    elif not force_converged:
        final_force_abs = float(abs(force_series[-1]))
        print(f"| Force error not converged | `final |e_f|={fmt_float(final_force_abs, 4)}` | Fig. 6(c) exists but still does not satisfy the paper claim of convergence |")
    if not q0_matches:
        print("| Initial state differs | Current run does not start from the paper `q0` | Joint-limit timing and velocity shape are not directly comparable |")
    if not q7_match:
        print(f"| `q7@22s` mismatch | Current `q7(22s)={fmt_float(q7_22, 4)}` | The paper's most explicit Fig. 6 timing landmark is not matched |")
    if float(np.max(E)) > 1.0:
        print(f"| Residual spike | `E_max={fmt_float(float(np.max(E)), 4)}` | The current inner-loop shape still differs materially from the paper plots |")
    print()

    print("| Priority | Action | Expected effect |")
    print("|---|---|---|")
    if not has_force:
        print("| 1 | Add the minimum force/contact chain and log force error | Enables a real Fig. 6(c) comparison and changes motion distribution under contact |")
    elif not force_converged:
        print("| 1 | Stabilize the force/contact loop before chasing later shape details | Keeps contact active and turns Fig. 6(c) from present-but-wrong into convergent |")
    elif not q0_matches:
        print("| 1 | Split `paper_ideal` from `step_surface` and restore paper `q0` in the paper line | Makes `q7@22s` and early velocity saturation comparable to the paper |")
    else:
        print("| 1 | Diagnose the `19–20 s` spike with Jacobian condition and clamp activity traces | Targets the remaining shape mismatch without mixing scene changes |")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
