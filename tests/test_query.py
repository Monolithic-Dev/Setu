import requests

BASE = 'https://setu-60077881047.development.catalystserverless.in/server/setu_api'

# Test 1: Dashboard stats
print("=== TEST 1: Dashboard Stats ===")
res = requests.get(f'{BASE}/api/dashboard/stats')
print(f'Status: {res.status_code}')
data = res.json()
print(f'Total cases: {data.get("data", {}).get("totalCases")}')
print(f'Hotspots: {data.get("data", {}).get("activeHotspots")}')
print()

# Test 2: Alerts
print("=== TEST 2: Hotspot Alerts ===")
res = requests.get(f'{BASE}/api/alerts/hotspots')
print(f'Status: {res.status_code}')
alerts = res.json().get('alerts', [])
print(f'Alert count: {len(alerts)}')
print()

# Test 3: Query with NO headers (simulates browser with no X-Dev-Role — should now default to SCRB Analyst)
print("=== TEST 3: Query (no auth headers, should default to SCRB Analyst) ===")
res = requests.post(f'{BASE}/api/query', json={
    'session_id': 'smoke_test',
    'text': 'Show me cyber fraud cases in Tumakuru',
    'language': 'en'
})
print(f'Status: {res.status_code}')
body = res.json()
print(f'Answer: {body.get("answer", "")[:200]}')
print(f'Sources: {body.get("sources", [])}')
print()

# Test 4: OPTIONS preflight
print("=== TEST 4: CORS Preflight (OPTIONS) ===")
res = requests.options(f'{BASE}/api/query', headers={
    'Origin': 'https://setu-60077881047.development.catalystserverless.in',
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'Content-Type'
})
print(f'Status: {res.status_code}')
print(f'CORS Allow-Origin: {res.headers.get("Access-Control-Allow-Origin", "MISSING")}')
print(f'CORS Allow-Methods: {res.headers.get("Access-Control-Allow-Methods", "MISSING")}')
print()

# Test 5: Network graph
print("=== TEST 5: Network Graph ===")
res = requests.get(f'{BASE}/api/network/Person%200001')
print(f'Status: {res.status_code}')
net = res.json()
print(f'Nodes: {len(net.get("nodes", []))}, Edges: {len(net.get("edges", []))}')
