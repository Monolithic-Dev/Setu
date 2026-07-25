import json

with open('functions/setu_api/data/synthetic_cases.json', encoding='utf-8') as f:
    cases = json.load(f)

stations = set(c['location']['station_jurisdiction'] for c in cases)
districts = set(c['location']['district'] for c in cases)

print(f'Total cases: {len(cases)}')
print(f'\nUnique stations ({len(stations)}):')
for s in sorted(stations):
    print(f'  {s}')
print(f'\nUnique districts ({len(districts)}):')
for d in sorted(districts):
    print(f'  {d}')

# Check if any case has "Bengaluru Urban Station 1" as station_jurisdiction
bu_cases = [c for c in cases if c['location']['station_jurisdiction'] == 'Bengaluru Urban Station 1']
print(f'\nCases with station "Bengaluru Urban Station 1": {len(bu_cases)}')

# Check Bengaluru Urban district
bu_district_cases = [c for c in cases if c['location']['district'] == 'Bengaluru Urban']
print(f'Cases with district "Bengaluru Urban": {len(bu_district_cases)}')
