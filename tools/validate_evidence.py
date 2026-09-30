#!/usr/bin/env python3
"""Validate evidence records against the release-gate schema.

Stdlib only. Checks the constraints that matter for the gate rule of Definition 3,
including the invariant that a record may not claim gating authority unless its
measured fidelity clears the threshold.

Usage:
    python3 tools/validate_evidence.py schema/example-record.json [more.json ...]
    python3 tools/validate_evidence.py --tau 0.85 record.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FAMILIES = {"functional", "adversarial", "cyber", "hardware"}
RUNNERS = {"calibrated_sim", "log_replay", "hardware_in_loop", "physical_cell", "static_analysis"}
REQUIRED_TOP = ["record_id", "release", "test", "runner", "system_under_test",
                "outcome", "fidelity", "provenance"]
DEFAULT_TAU = 0.80
DEFAULT_N_MIN = 8


def check(record: dict, tau: float, n_min: int) -> list[str]:
    errors: list[str] = []

    for key in REQUIRED_TOP:
        if key not in record:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors

    fam = record["test"].get("family")
    if fam not in FAMILIES:
        errors.append(f"test.family must be one of {sorted(FAMILIES)}, got {fam!r}")

    kind = record["runner"].get("kind")
    if kind not in RUNNERS:
        errors.append(f"runner.kind must be one of {sorted(RUNNERS)}, got {kind!r}")

    fid = record["fidelity"]
    rho = fid.get("rho")
    if not isinstance(rho, (int, float)) or not -1.0 <= rho <= 1.0:
        errors.append(f"fidelity.rho must be a number in [-1, 1], got {rho!r}")
    authority = fid.get("gating_authority", "advisory")
    used = fid.get("checkpoints_used", 0)

    # The load-bearing invariant of the framework.
    if authority == "gating":
        if not isinstance(rho, (int, float)) or rho < tau:
            errors.append(
                f"gating_authority='gating' requires fidelity.rho >= tau ({tau}); got {rho!r}"
            )
        if fid.get("method") == "not_established":
            errors.append("gating_authority='gating' requires an established fidelity method")
        if used < n_min:
            errors.append(
                f"gating_authority='gating' requires checkpoints_used >= {n_min}; got {used}"
            )

    if record["provenance"].get("immutable") is not True:
        errors.append("provenance.immutable must be true")

    out = record["outcome"]
    if "baseline_value" in out and "value" in out and "delta" in out:
        expected = round(out["value"] - out["baseline_value"], 6)
        if abs(expected - out["delta"]) > 1e-6:
            errors.append(f"outcome.delta {out['delta']} != value - baseline_value ({expected})")

    sha = record["system_under_test"]["policy"].get("weights_sha256")
    if sha is not None and (len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha)):
        errors.append("policy.weights_sha256 must be 64 lowercase hex characters")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("records", nargs="+", type=Path)
    ap.add_argument("--tau", type=float, default=DEFAULT_TAU, help=f"fidelity threshold (default {DEFAULT_TAU})")
    ap.add_argument("--n-min", type=int, default=DEFAULT_N_MIN, help=f"minimum checkpoints (default {DEFAULT_N_MIN})")
    args = ap.parse_args()

    failed = 0
    for path in args.records:
        try:
            record = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            print(f"FAIL {path}: {exc}")
            failed += 1
            continue
        errors = check(record, args.tau, args.n_min)
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            gate = record["fidelity"].get("gating_authority", "advisory")
            print(f"OK   {path}  [{record['test']['family']} / {gate} / rho={record['fidelity']['rho']}]")

    print(f"\n{len(args.records) - failed}/{len(args.records)} records valid (tau={args.tau}, n_min={args.n_min})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
