"""
Shared test helper — loads a function's index.py under a unique module
alias instead of `sys.path.insert(...); from index import ...`.

Why this exists: functions/queryFunction/index.py, functions/networkFunction/
index.py, etc. are all literally named index.py (following what's likely
the Catalyst convention — see the caveat in functions/queryFunction/index.py).
Importing them all via sys.path + `from index import` in the same test
process causes a real module-cache collision: whichever one gets imported
first wins, and every subsequent `from index import` silently returns the
WRONG module instead of failing loudly. Found this by running the full
test suite together, not by running test files individually — each one
passed in isolation, which is exactly why it's worth a shared, correct
fix rather than a one-off workaround in whichever test happened to fail.
"""

import importlib.util
import os
import sys


def load_function_module(function_dir_name: str, repo_root: str):
    """
    Loads functions/<function_dir_name>/index.py under the unique module
    name f"_fn_{function_dir_name}", sys.path additions for its own
    imports (of functions/shared/*) still apply globally, but the module
    itself is cached under a collision-proof name.
    """
    shared_path = os.path.join(repo_root, "catalyst_functions", "setu_api", "shared")
    shared_path = os.path.join(repo_root, "functions", "setu_api", "shared")
    shared_retrieval_path = os.path.join(shared_path, "retrieval")
    if shared_path not in sys.path:
        sys.path.insert(0, shared_path)
    if shared_retrieval_path not in sys.path:
        sys.path.insert(0, shared_retrieval_path)

    module_path = os.path.join(repo_root, "functions", "setu_api", function_dir_name, "index.py")
    unique_name = f"_fn_{function_dir_name}"

    if unique_name in sys.modules:
        return sys.modules[unique_name]

    spec = importlib.util.spec_from_file_location(unique_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = module
    spec.loader.exec_module(module)
    return module
