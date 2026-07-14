"""
Synthetic Karnataka crime-record dataset generator.

Generates a bilingual (Kannada + English narrative), realistic-but-fictional
case corpus for development, testing, and demo purposes. No real individual,
station, or case is represented.

Deliberately excludes any demographic/socio-economic field, per
docs/Database.md §3 — that exclusion happens here, at generation time, not
just downstream in the application layer, so the sensitive category never
exists in the pipeline at all.

Usage:
    python3 generate_dataset.py --n-cases 500 --seed 42 --out ../../data/synthetic_cases.json
"""

import argparse
import json
import random
import uuid
from datetime import datetime, timedelta

# Fictional Karnataka districts and station jurisdictions used only to give
# geographic spread for hotspot-clustering demos. Not tied to real station data.
DISTRICTS = [
    "Bengaluru Urban", "Mysuru", "Mangaluru", "Belagavi", "Hubballi-Dharwad",
    "Kalaburagi", "Ballari", "Tumakuru", "Shivamogga", "Davanagere",
]

# Rough illustrative lat/lon bounding boxes per district (fictional jitter
# applied around each district's approximate centroid) — good enough for a
# demo geospatial spread, not survey-grade coordinates.
DISTRICT_CENTROIDS = {
    "Bengaluru Urban": (12.9716, 77.5946),
    "Mysuru": (12.2958, 76.6394),
    "Mangaluru": (12.9141, 74.8560),
    "Belagavi": (15.8497, 74.4977),
    "Hubballi-Dharwad": (15.3647, 75.1240),
    "Kalaburagi": (17.3297, 76.8343),
    "Ballari": (15.1394, 76.9214),
    "Tumakuru": (13.3379, 77.1173),
    "Shivamogga": (13.9299, 75.5681),
    "Davanagere": (14.4644, 75.9218),
}

MODUS_OPERANDI = [
    "residential break-in via rear window",
    "residential break-in via forced door lock",
    "two-wheeler theft from parking area",
    "chain snatching on foot near market",
    "chain snatching using two-wheeler",
    "shop burglary after business hours",
    "ATM tampering attempt",
    "pickpocketing in crowded transit area",
    "cyber fraud via phishing call",
    "cyber fraud via fake job offer",
]

# Kannada renderings of the same MO categories, index-aligned with MODUS_OPERANDI.
# NOTE: machine-drafted, not verified by a native Kannada speaker — same caveat
# as docs/PRD.md's naming note. Review before this dataset is used in anything
# demo-facing; wrong terminology here undercuts the whole bilingual pitch.
MODUS_OPERANDI_KN = [
    "ಹಿಂಬದಿ ಕಿಟಕಿಯ ಮೂಲಕ ಮನೆ ಕಳ್ಳತನ",
    "ಬಾಗಿಲಿನ ಬೀಗ ಮುರಿದು ಮನೆ ಕಳ್ಳತನ",
    "ಪಾರ್ಕಿಂಗ್ ಪ್ರದೇಶದಿಂದ ದ್ವಿಚಕ್ರ ವಾಹನ ಕಳ್ಳತನ",
    "ಮಾರುಕಟ್ಟೆ ಬಳಿ ನಡೆದುಕೊಂಡು ಸರಗಳ್ಳತನ",
    "ದ್ವಿಚಕ್ರ ವಾಹನ ಬಳಸಿ ಸರಗಳ್ಳತನ",
    "ವ್ಯಾಪಾರದ ಸಮಯದ ನಂತರ ಅಂಗಡಿ ಕಳ್ಳತನ",
    "ಎಟಿಎಂ ಕುತಂತ್ರ ಪ್ರಯತ್ನ",
    "ಜನನಿಬಿಡ ಸ್ಥಳದಲ್ಲಿ ಜೇಬುಗಳ್ಳತನ",
    "ಫಿಶಿಂಗ್ ಕರೆ ಮೂಲಕ ಸೈಬರ್ ವಂಚನೆ",
    "ನಕಲಿ ಉದ್ಯೋಗ ನೀಡಿಕೆ ಮೂಲಕ ಸೈಬರ್ ವಂಚನೆ",
]

WEAPON_TYPES = ["none", "knife", "blunt object", "none (cyber/no physical weapon)"]

CASE_STATUSES = ["under investigation", "chargesheet filed", "closed", "pending forensic report"]

# Kannada status renderings, index-aligned with CASE_STATUSES. Same review caveat as above.
CASE_STATUSES_KN = ["ತನಿಖೆ ಹಂತದಲ್ಲಿ", "ಆರೋಪಪಟ್ಟಿ ಸಲ್ಲಿಕೆಯಾಗಿದೆ", "ಪ್ರಕರಣ ಮುಕ್ತಾಯ", "ವಿಧಿವಿಜ್ಞಾನ ವರದಿ ಬಾಕಿ"]

# Bilingual narrative templates. Kept generic/templated rather than
# hand-authored per case, since the point is realistic structure and
# bilingual parity for retrieval testing, not literary quality.
NARRATIVE_TEMPLATES_EN = [
    "Complainant reported a {mo} at approximately {time} in {district}. "
    "{weapon_clause} Case status: {status}.",
    "A case of {mo} was registered in {district}. Incident occurred around {time}. "
    "{weapon_clause} Current status: {status}.",
]

NARRATIVE_TEMPLATES_KN = [
    "{district} ನಲ್ಲಿ {time} ಸಮಯದಲ್ಲಿ {mo} ಪ್ರಕರಣ ವರದಿಯಾಗಿದೆ. ಪ್ರಕರಣದ ಸ್ಥಿತಿ: {status}.",
    "{district} ಪ್ರದೇಶದಲ್ಲಿ {mo} ಘಟನೆ ವರದಿಯಾಗಿದ್ದು, ಸಮಯ ಸುಮಾರು {time}. ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ: {status}.",
]


def _jitter(lat, lon, spread=0.05):
    return round(lat + random.uniform(-spread, spread), 6), round(lon + random.uniform(-spread, spread), 6)


def _random_datetime(start_year=2024, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 6, 30)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def generate_case(index: int) -> dict:
    district = random.choice(DISTRICTS)
    lat, lon = DISTRICT_CENTROIDS[district]
    lat, lon = _jitter(lat, lon)
    mo_idx = random.randrange(len(MODUS_OPERANDI))
    mo = MODUS_OPERANDI[mo_idx]
    mo_kn = MODUS_OPERANDI_KN[mo_idx]
    weapon = random.choice(WEAPON_TYPES)
    status_idx = random.randrange(len(CASE_STATUSES))
    status = CASE_STATUSES[status_idx]
    status_kn = CASE_STATUSES_KN[status_idx]
    filed_dt = _random_datetime()
    time_str = filed_dt.strftime("%H:%M")

    weapon_clause_en = (
        f"No weapon was involved." if weapon.startswith("none")
        else f"A {weapon} was reportedly involved."
    )

    narrative_en = random.choice(NARRATIVE_TEMPLATES_EN).format(
        mo=mo, time=time_str, district=district, weapon_clause=weapon_clause_en, status=status
    )
    narrative_kn = random.choice(NARRATIVE_TEMPLATES_KN).format(
        mo=mo_kn, time=time_str, district=district, status=status_kn
    )

    return {
        "case_id": f"KA-{filed_dt.year}-{index:05d}",
        "fir_number": f"FIR/{filed_dt.year}/{random.randint(1000, 9999)}",
        "filed_date": filed_dt.strftime("%Y-%m-%d"),
        "modus_operandi": mo,
        "weapon_type": weapon,
        "status": status,
        "narrative_en": narrative_en,
        "narrative_kn": narrative_kn,
        "sensitivity_level": "restricted" if random.random() < 0.05 else "standard",  # docs/Database.md §4a
        "location": {
            "district": district,
            "station_jurisdiction": f"{district} Station {random.randint(1, 12)}",
            "latitude": lat,
            "longitude": lon,
        },
        # Deliberately absent, by design (docs/Database.md §3):
        # no age, gender, caste, religion, income, or any other demographic/
        # socio-economic field anywhere in this record.
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-cases", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="synthetic_cases.json")
    parser.add_argument("--persons-out", type=str, default=None,
                         help="If set, also generate Person + NetworkEdge records (docs/Database.md ER diagram) to this path.")
    args = parser.parse_args()

    random.seed(args.seed)
    cases = [generate_case(i) for i in range(1, args.n_cases + 1)]

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(cases)} synthetic cases -> {args.out}")
    print(f"Districts covered: {len(set(c['location']['district'] for c in cases))}")
    print(f"Restricted-sensitivity cases: {sum(1 for c in cases if c['sensitivity_level'] == 'restricted')}")

    if args.persons_out:
        persons, edges, case_person_links = generate_network(cases)
        with open(args.persons_out, "w", encoding="utf-8") as f:
            json.dump({"persons": persons, "edges": edges, "case_person_links": case_person_links}, f, indent=2)
        print(f"Generated {len(persons)} persons, {len(edges)} network edges -> {args.persons_out}")


def generate_network(cases: list) -> tuple:
    """
    Generates Person and NetworkEdge records (docs/Database.md ER diagram)
    linked to the case corpus — needed for FR-4.1/4.2 (network
    visualization), which had zero backing data until this was added.
    Deliberately uses synthetic ID-style labels ("P-0001"), not invented
    realistic names — this is graph-structure demo data, not a claim about
    what real records look like, and fabricating culturally-specific names
    isn't worth the risk of getting it wrong for data nobody needs to read
    as a name in the first place.
    """
    n_persons = max(20, len(cases) // 4)  # fewer persons than cases, so some recur across cases
    persons = [
        {"person_id": f"P-{i:04d}", "name": f"Person {i:04d}", "role_in_case": ""}
        for i in range(1, n_persons + 1)
    ]
    person_ids = [p["person_id"] for p in persons]

    case_person_links = []
    person_cases: dict = {pid: [] for pid in person_ids}

    for case in cases:
        n_involved = random.choice([1, 1, 2, 2, 3])  # most cases involve 1-2 people, some 3
        involved = random.sample(person_ids, min(n_involved, len(person_ids)))
        roles = ["accused", "witness", "complainant"]
        for i, pid in enumerate(involved):
            role = roles[0] if i == 0 else random.choice(roles)
            case_person_links.append({"case_id": case["case_id"], "person_id": pid, "relationship": role})
            person_cases[pid].append((case["case_id"], role))

    # Build edges from genuine co-occurrence: two people linked in the same
    # case get an edge. This is what makes the graph non-trivial to look at —
    # persons who recur across multiple cases end up with multiple edges,
    # which is the whole point of a network view.
    edges = []
    edge_id = 1
    for case in cases:
        involved_in_case = [link["person_id"] for link in case_person_links if link["case_id"] == case["case_id"]]
        for i in range(len(involved_in_case)):
            for j in range(i + 1, len(involved_in_case)):
                edges.append({
                    "edge_id": f"E-{edge_id:04d}",
                    "person_id_a": involved_in_case[i],
                    "person_id_b": involved_in_case[j],
                    "relationship_type": "co-accused" if len(involved_in_case) > 1 else "associate",
                    "confidence": round(random.uniform(0.6, 0.98), 2),
                })
                edge_id += 1

    return persons, edges, case_person_links


if __name__ == "__main__":
    main()
