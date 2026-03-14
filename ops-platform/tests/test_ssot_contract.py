"""Test that SSOT validators pass on committed YAML files."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_validate_ssot():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_ssot.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_repo_boundaries():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_repo_boundaries.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
