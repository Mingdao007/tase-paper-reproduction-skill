#!/usr/bin/env python3
"""Summarize TASE MATLAB result files into a human-friendly Markdown report."""

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
        return "Missing"
    if match:
        return "Match"
    if partial:
        return "Partial"
    return "Mismatch"


def default_report_path(mat_path: Path) -> Path:
    return mat_path.with_name(f"{mat_path.stem}_report.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mat", required=True, help="Path to MATLAB .mat result file")
    parser.add_argument("--run-type", required=True, help="Run label such as paper_first")
    parser.add_argument("--repo", required=True, help="Path to git repo that produced the run")
    parser.add_argument("--out", help="Optional path for the generated Markdown report")
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
    force_meas = None
    if has_force:
        for key in ("force_error_save", "f_err_save", "force_save"):
            if key in data:
                force_series = np.asarray(data[key]).reshape(-1)
                break
    if "force_meas_save" in data:
        force_meas = np.asarray(data["force_meas_save"]).reshape(-1)
    force_converged = False
    force_partial = False
    force_tail_mean_abs = float("nan")
    force_final_abs = float("nan")
    if force_series is not None:
        tail = force_series[max(0, len(force_series) - 5000):]
        force_tail_mean_abs = float(np.mean(np.abs(tail)))
        force_final_abs = float(abs(force_series[-1]))
        force_converged = force_tail_mean_abs < 1.0 and force_final_abs < 1.0
        force_partial = force_tail_mean_abs < 2.0 and force_final_abs < 2.0

    q0_matches = np.allclose(q0_current, PAPER_Q0, atol=1e-3)
    q7_match = abs(abs(q7_22) - PAPER_JOINT_LIMIT) <= 5e-2
    pos_norm = float(np.linalg.norm(pos_final)) if pos_final.size else float("nan")
    ori_norm = float(np.linalg.norm(ori_final)) if ori_final.size else float("nan")
    E_end = float(E[-1])
    E_max = float(np.max(E))
    contact_fraction = float(np.mean(np.asarray(data["contact_active_save"]).reshape(-1))) if "contact_active_save" in data else float("nan")
    measured_force_end = float(force_meas[-1]) if force_meas is not None else float("nan")

    if not has_force:
        current_verdict = "Not paper-faithful yet."
        biggest_blocker = "Fig. 6(c) still has no force-error subsystem."
        next_action = "Add the minimum force/contact chain and log force error."
    elif not force_converged:
        current_verdict = "Not paper-faithful yet."
        biggest_blocker = "Force/contact exists but does not stay engaged, so Fig. 6(c) still fails."
        next_action = "Stabilize force/contact retention before tuning any later-shape details."
    elif not q7_match:
        current_verdict = "Partially matching, but still not paper-faithful."
        biggest_blocker = "The paper's clearest timing landmark, q7 hitting the limit at 22 s, is still missing."
        next_action = "Make the paper_ideal scene more comparable before chasing secondary plot shape details."
    else:
        current_verdict = "Close on the core paper landmarks."
        biggest_blocker = "Only secondary plot-shape differences remain."
        next_action = "Diagnose the remaining spike and start-up velocity shape."

    force_line = (
        f"{verdict(force_converged, partial=force_partial, missing=not has_force)}: "
        + (
            "result file still has no force-error state."
            if not has_force
            else f"force channel exists, final |e_f|={fmt_float(force_final_abs, 4)} N, "
            f"tail mean |e_f|={fmt_float(force_tail_mean_abs, 4)} N, "
            f"final measured force={fmt_float(measured_force_end, 4)} N."
        )
    )
    q7_line = (
        f"{verdict(q7_match)}: paper expects the seventh joint near ±2.5 rad at 22 s, "
        f"current q7(22 s)={fmt_float(q7_22, 4)} rad."
    )
    vel_line = (
        f"{verdict(False, partial=near_vel_limit)}: paper shows start-up velocity saturation, "
        f"current max |dq|={fmt_vec(dq_abs_max, 3)} rad/s."
    )
    pos_line = (
        f"{verdict(pos_norm < 5e-3, partial=pos_norm < 5e-2)}: "
        f"final position error={fmt_vec(pos_final, 6)} m, max={fmt_vec(pos_max, 4)} m."
    )
    ori_line = (
        f"{verdict(ori_norm < 5e-3, partial=ori_norm < 5e-2)}: "
        f"final orientation error={fmt_vec(ori_final, 6)}, max={fmt_vec(ori_max, 4)}."
    )
    scene_line = (
        f"{verdict(q0_matches and q7_match, partial=q0_matches)}: "
        f"q0_match={q0_matches}, first limit event={first_limit_text}."
    )

    blocking_gaps: list[str] = []
    if not has_force:
        blocking_gaps.append(
            "- Force loop absent: no force-error variable is saved, so Fig. 6(c) cannot be claimed at all."
        )
    elif not force_converged:
        blocking_gaps.append(
            f"- Force/contact not retained: final |e_f|={fmt_float(force_final_abs, 4)} N, "
            f"contact fraction={fmt_float(contact_fraction, 4)}. This blocks a paper-faithful Fig. 6(c)."
        )
    if not q0_matches:
        blocking_gaps.append(
            "- Initial state differs from paper q0: joint-limit timing and early velocity shape are no longer directly comparable."
        )
    if not q7_match:
        blocking_gaps.append(
            f"- q7 landmark still misses: q7(22 s)={fmt_float(q7_22, 4)} rad instead of about ±2.5 rad."
        )
    if E_max > 1.0:
        blocking_gaps.append(
            f"- Residual inner-loop spike remains: E_max={fmt_float(E_max, 4)}, so the plot shape still differs materially."
        )
    if not blocking_gaps:
        blocking_gaps.append("- No major blocking gaps detected from the saved signals.")

    report_lines = [
        f"# TASE Run Report: {args.run_type}",
        "",
        "## Quick Verdict",
        f"- Current verdict: {current_verdict}",
        f"- Best-matching part: orientation convergence is the cleanest match right now with final error norm {fmt_float(ori_norm, 6)}.",
        f"- Biggest blocker: {biggest_blocker}",
        f"- Next step: {next_action}",
        "",
        "## Run Snapshot",
        f"- Run type: `{args.run_type}`",
        f"- Result file: `{mat_path}`",
        f"- Branch / commit: `{branch}` / `{commit}`",
        f"- Dirty state: `{dirty}`",
        f"- Duration / steps: `{fmt_float(float(t[-1]), 3)} s / {len(t)}`",
        f"- Key end metrics: `E_end={fmt_float(E_end, 6)}`, `q7@22s={fmt_float(q7_22, 4)}`, "
        + (f"`final |e_f|={fmt_float(force_final_abs, 4)} N`, " if has_force else "")
        + f"`|e_p(final)|={fmt_float(pos_norm, 6)}`, `|e_o(final)|={fmt_float(ori_norm, 6)}`",
        "",
        "## Current vs Paper",
        f"- Fig. 6(c) force error: {force_line}",
        f"- q7 @ 22 s: {q7_line}",
        f"- Joint velocity pattern: {vel_line}",
        f"- Position error: {pos_line}",
        f"- Orientation error: {ori_line}",
        f"- Scene assumptions: {scene_line}",
        "",
        "## Blocking Gaps",
        *blocking_gaps,
        "",
        "## Next Single Action",
        f"- {next_action} This is the highest-leverage move because it addresses the largest paper-side mismatch first.",
        "",
    ]

    report_text = "\n".join(report_lines)
    out_path = Path(args.out).expanduser().resolve() if args.out else default_report_path(mat_path)
    out_path.write_text(report_text, encoding="utf-8")

    print(f"Report written to: {out_path}")
    print(f"Current verdict: {current_verdict}")
    print(f"Biggest blocker: {biggest_blocker}")
    print(f"Next step: {next_action}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
