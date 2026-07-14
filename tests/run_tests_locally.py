"""
Minimal local test runner — used ONLY because this sandbox has no network
access to `pip install pytest` (see docs — bash tool network is disabled
here). The test files in tests/unit/ are ordinary pytest-style code and
should be run with real pytest once you have network: `pytest tests/unit/`.

This script exists purely to actually verify the test logic works right
now, rather than shipping test files nobody has confirmed pass.
"""

import importlib.util
import sys
import types
from pathlib import Path
from contextlib import contextmanager

# Minimal shim so `import pytest; pytest.raises(...)` in test_auth_middleware.py
# works without the real pytest package installed. Only implements what
# this test suite actually uses.
pytest_shim = types.ModuleType("pytest")


@contextmanager
def _raises(exc_type):
    try:
        yield
    except exc_type:
        return
    else:
        raise AssertionError(f"Expected {exc_type.__name__} to be raised, but nothing was raised.")


pytest_shim.raises = _raises
sys.modules["pytest"] = pytest_shim


def run_test_file(path: Path) -> tuple[int, int, list[str]]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    passed, failed = 0, 0
    failures = []
    for name in dir(module):
        if name.startswith("test_"):
            fn = getattr(module, name)
            try:
                fn()
                passed += 1
            except Exception as e:
                failed += 1
                failures.append(f"{path.name}::{name} -> {type(e).__name__}: {e}")
    return passed, failed, failures


def main():
    # Ensure test prerequisites exist before any test needs them — same
    # functions real pytest's conftest.py calls automatically; this runner
    # calls them explicitly since it doesn't have pytest's fixture system.
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from conftest import ensure_synthetic_data, ensure_question_set, ensure_network_data
    data_path = ensure_synthetic_data()
    question_set_path = ensure_question_set()
    network_path = ensure_network_data()
    print(f"Synthetic dataset ready: {data_path}")
    print(f"Eval question set ready: {question_set_path}")
    print(f"Network data ready: {network_path}\n")

    total_passed, total_failed = 0, 0
    all_failures = []

    for subdir in ["unit", "integration", "eval"]:
        test_dir = Path(__file__).parent / subdir
        for test_file in sorted(test_dir.glob("test_*.py")):
            passed, failed, failures = run_test_file(test_file)
            total_passed += passed
            total_failed += failed
            all_failures.extend(failures)
            status = "OK" if failed == 0 else "FAIL"
            print(f"[{status}] {subdir}/{test_file.name}: {passed} passed, {failed} failed")

    print(f"\n{total_passed} passed, {total_failed} failed total")
    if all_failures:
        print("\nFailures:")
        for f in all_failures:
            print(f"  - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
