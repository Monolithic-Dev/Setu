import sys
import os
import json
import time

sys.path.insert(0, os.path.abspath('functions/setu_api/ml/eval'))
from run_eval import run_eval, _query_index

data_paths = [
    ("1x (300 cases)", "data/synthetic_cases.json"),
    ("10x (5000 cases)", "data/synthetic_cases_10x.json"),
    ("50x (25000 cases)", "data/synthetic_cases_50x.json")
]

questions = [
    "functions/setu_api/ml/eval/eval_set_en.json",
    "functions/setu_api/ml/eval/eval_set_kn.json",
    "functions/setu_api/ml/eval/eval_set_codeswitch.json"
]

results = []

for label, path in data_paths:
    print(f"Running eval on {label}...")
    _query_index._DEV_DATA_PATH = os.path.abspath(path)
    _query_index._dev_cases_cache = None
    _query_index._dev_index_cache_en = None
    _query_index._dev_index_cache_kn = None
    
    start_time = time.time()
    res = run_eval(questions)
    elapsed = time.time() - start_time
    
    print(f"{label} -> p50: {res['latency_p50_seconds']:.4f}s, p95: {res['latency_p95_seconds']:.4f}s (Total time: {elapsed:.2f}s)")
    results.append({
        "label": label,
        "p50": res['latency_p50_seconds'],
        "p95": res['latency_p95_seconds']
    })

with open("scalability_results.json", "w") as f:
    json.dump(results, f, indent=2)
