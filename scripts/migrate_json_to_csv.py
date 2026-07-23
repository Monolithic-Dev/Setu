import json
import csv
import os
import hashlib

def generate_location_id(district, station):
    """Generates a stable location ID based on district and station."""
    s = f"{district}-{station}"
    return "LOC-" + hashlib.md5(s.encode()).hexdigest()[:8]

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    out_dir = os.path.join(data_dir, 'csv_exports')
    os.makedirs(out_dir, exist_ok=True)
    
    cases_file = os.path.join(data_dir, 'synthetic_cases.json')
    network_file = os.path.join(data_dir, 'synthetic_network.json')
    
    # 1. Parse Cases & Locations
    print("Parsing synthetic cases...")
    with open(cases_file, 'r', encoding='utf-8') as f:
        cases_data = json.load(f)
        
    case_records = []
    locations = {}
    
    for case in cases_data:
        # Extract location
        loc = case.get('location', {})
        district = loc.get('district', '')
        station = loc.get('station_jurisdiction', '')
        loc_id = generate_location_id(district, station)
        
        if loc_id not in locations:
            locations[loc_id] = {
                'location_id': loc_id,
                'latitude': loc.get('latitude', 0.0),
                'longitude': loc.get('longitude', 0.0),
                'district': district,
                'station_jurisdiction': station
            }
            
        case_record = {
            'case_id': case.get('case_id', ''),
            'fir_number': case.get('fir_number', ''),
            'filed_date': case.get('filed_date', ''),
            'modus_operandi': case.get('modus_operandi', ''),
            'weapon_type': case.get('weapon_type', ''),
            'status': case.get('status', ''),
            'narrative_kn': case.get('narrative_kn', ''),
            'narrative_en': case.get('narrative_en', ''),
            'location_id': loc_id,
            'sensitivity_level': case.get('sensitivity_level', '')
        }
        case_records.append(case_record)
        
    # Write CASE_RECORD.csv
    case_keys = ['case_id', 'fir_number', 'filed_date', 'modus_operandi', 'weapon_type', 'status', 'narrative_kn', 'narrative_en', 'location_id', 'sensitivity_level']
    with open(os.path.join(out_dir, 'CASE_RECORD.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=case_keys)
        writer.writeheader()
        writer.writerows(case_records)
    print(f"Exported {len(case_records)} rows to CASE_RECORD.csv")
    
    # Write LOCATION.csv
    loc_keys = ['location_id', 'latitude', 'longitude', 'district', 'station_jurisdiction']
    with open(os.path.join(out_dir, 'LOCATION.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=loc_keys)
        writer.writeheader()
        writer.writerows(locations.values())
    print(f"Exported {len(locations)} rows to LOCATION.csv")
    
    # 2. Parse Network (Persons, Links, Edges)
    print("Parsing synthetic network...")
    if os.path.exists(network_file):
        with open(network_file, 'r', encoding='utf-8') as f:
            network_data = json.load(f)
            
        # Write PERSON.csv
        persons = network_data.get('persons', [])
        person_keys = ['person_id', 'name', 'role_in_case']
        with open(os.path.join(out_dir, 'PERSON.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=person_keys)
            writer.writeheader()
            writer.writerows(persons)
        print(f"Exported {len(persons)} rows to PERSON.csv")
        
        # Write CASE_PERSON_LINK.csv
        case_links = network_data.get('case_links', [])
        link_keys = ['case_id', 'person_id', 'relationship']
        with open(os.path.join(out_dir, 'CASE_PERSON_LINK.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=link_keys)
            writer.writeheader()
            writer.writerows(case_links)
        print(f"Exported {len(case_links)} rows to CASE_PERSON_LINK.csv")
        
        # Write NETWORK_EDGE.csv
        edges = network_data.get('network_edges', [])
        edge_keys = ['edge_id', 'person_id_a', 'person_id_b', 'relationship_type', 'confidence']
        with open(os.path.join(out_dir, 'NETWORK_EDGE.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=edge_keys)
            writer.writeheader()
            writer.writerows(edges)
        print(f"Exported {len(edges)} rows to NETWORK_EDGE.csv")
    else:
        print("synthetic_network.json not found, skipping network files.")
        
    print(f"\\nAll CSVs successfully exported to: {out_dir}")

if __name__ == '__main__':
    main()
