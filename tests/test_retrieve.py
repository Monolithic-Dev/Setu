import sys
import os
sys.path.insert(0, os.path.abspath('functions/setu_api'))
from queryFunction.index import retrieve, extract_structured_filters
from shared.models import RoleName, User

user = User("demo", "all", "S-101", "D-10")
role_name = RoleName.SCRB_ANALYST
query = "Show me cyber fraud cases in Tumakuru"

print("Filters extracted:", extract_structured_filters(query))
results, filters = retrieve(query, user, role_name)
print(f"Retrieved {len(results)} results")
for r in results:
    print(r.get('case_id'), r.get('modus_operandi'), r.get('match_type'))
