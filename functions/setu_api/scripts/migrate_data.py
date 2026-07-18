import sys
import os
import json
import zcatalyst_sdk

def migrate():
    print("Starting migration to Catalyst Data Store...")
    try:
        app = zcatalyst_sdk.initialize()
        datastore = app.datastore()
    except Exception as e:
        print("Failed to initialize Catalyst SDK. Make sure you have Catalyst credentials.")
        print(e)
        return

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_cases.json")
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        cases = json.load(f)
    
    print(f"Found {len(cases)} cases. Migrating...")
    
    case_table = datastore.table("CASE_RECORD")
    
    success_count = 0
    error_count = 0
    
    for case in cases:
        row = {
            "case_id": case.get("case_id"),
            "fir_number": case.get("fir_number"),
            "filed_date": case.get("filed_date"),
            "modus_operandi": case.get("modus_operandi"),
            "weapon_type": case.get("weapon_type"),
            "status": case.get("status"),
            "narrative_en": case.get("narrative_en", ""),
            "narrative_kn": case.get("narrative_kn", ""),
            "location_id": case.get("location", {}).get("station_jurisdiction", ""),
            "sensitivity_level": case.get("sensitivity_level", "standard")
        }
        
        try:
            case_table.insert_row(row)
            success_count += 1
            if success_count % 10 == 0:
                print(f"Inserted {success_count} rows...")
        except Exception as e:
            print(f"Error inserting case {case.get('case_id')}: {e}")
            error_count += 1
            
    print(f"Migration completed. Success: {success_count}, Errors: {error_count}")

    # Network Data
    network_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_network.json")
    if os.path.exists(network_path):
        print("Migrating network data...")
        with open(network_path, "r", encoding="utf-8") as f:
            network = json.load(f)
        
        person_table = datastore.table("PERSON")
        edge_table = datastore.table("NETWORK_EDGE")
        location_table = datastore.table("LOCATION")
        
        for person in network.get("persons", []):
            try:
                person_table.insert_row(person)
            except Exception as e:
                pass
                
        for edge in network.get("edges", []):
            try:
                edge_table.insert_row(edge)
            except Exception as e:
                pass
                
        for loc in network.get("locations", []):
            try:
                location_table.insert_row(loc)
            except Exception as e:
                pass
                
        print("Network data migration attempted.")

if __name__ == "__main__":
    migrate()
