import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).parent


def test_good_usage_passes_mypy():
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(HERE / "_good_usage.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"mypy unexpectedly failed:\n{result.stdout}\n{result.stderr}"


def test_bad_usage_without_ignores_fails_mypy(tmp_path):
    # Copy _bad_usage.py into tmp and strip the `# type: ignore[arg-type]` comments,
    # then assert mypy reports errors.
    source = (HERE / "_bad_usage.py").read_text()
    stripped = "\n".join(
        line.split("  # type: ignore")[0].rstrip() for line in source.splitlines()
    )
    probe = tmp_path / "_probe.py"
    probe.write_text(stripped)
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(probe)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "mypy should have rejected raw strings"
    assert "arg-type" in result.stdout or "arg-type" in result.stderr


def test_bad_usage_with_ignores_passes_mypy():
    # The file as-committed uses `# type: ignore[arg-type]` and must be clean.
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(HERE / "_bad_usage.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"expected clean:\n{result.stdout}\n{result.stderr}"
