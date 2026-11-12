import openpyxl, json, re
ws = openpyxl.load_workbook('/mnt/user-data/uploads/Claudework/joltpowerbank.com/Ireland_Best_200_Accounts.xlsx', read_only=True).active
rows = [r[0] for r in list(ws.iter_rows(values_only=True))[1:] if r[0]]
logos = json.load(open("logo_map.json"))

# cleaned display name -> merges duplicates (departments, entrances, floors)
CLEAN = [
 (r"^Clayton Hotel (Ballsbridge|Liffey Valley|Cardiff Lane|Leopardstown)$", lambda m: "Clayton Hotel " + m.group(1)),
 (r"^Cork University (Maternity )?Hospital.*", lambda m: "Cork University Maternity Hospital" if m.group(1) else "Cork University Hospital"),
 (r"^St Vincent's University Hospital.*", "St Vincent's University Hospital"),
 (r"^St James's Hospital.*", "St James's Hospital"),
 (r"^Beaumont Hospital.*", "Beaumont Hospital"),
 (r"^Connolly Hospital.*", "Connolly Hospital"),
 (r"^Portiuncula.*", "Portiuncula University Hospital"),
 (r"^Wexford General Hospital.*", "Wexford General Hospital"),
 (r"^Our Lady's Hospital", "Children's Health Ireland at Crumlin"),
 (r"^The Martello Hotel.*", "The Martello Hotel"),
 (r"^The Square.*", "The Square"),
 (r"^O'Donoghue'?s Bar( Dublin)?$", "O'Donoghue's"),
 (r"^O'Donoghues Bar Dublin$", "O'Donoghue's"),
 (r"^.*Liffey Valley$", "Liffey Valley"),
 (r"^Foodcourt Liffey Valley$", "Liffey Valley"),
 (r"^Blue Corridor Liffey Valley$", "Liffey Valley"),
 (r"^The Quays Dublin - Temple Bar$", "The Quays Temple Bar"),
 (r"^The Quays Bar and Restaurant Galway$", "The Quays Galway"),
 (r"^Merchants Quay.*", "Merchants Quay Shopping Centre"),
 (r"^Dublin Zoo.*", "Dublin Zoo"),
 (r"^The Convention Center Dublin.*", "The Convention Centre Dublin"),
 (r"^The Kingswood Lodge.*", "The Kingswood Lodge"),
 (r"^Capitol Lounge.*", "Capitol Lounge"),
 (r"^Junction 14 .*", "Junction 14 Mayfield"),
 (r"^Gibney's Of Malahide.*", "Gibney's of Malahide"),
 (r"^The Merlin Bar.*", "The Merlin Bar"),
 (r"^Tattersalls Ireland.*", "Tattersalls Ireland"),
 (r"^Shelbourne Park.*", "Shelbourne Park"),
 (r"^Tesco.*", "Tesco"),
 (r"^Londis.*", "Londis"),
 (r"^J\.R\. Mahon’s.*", "J.R. Mahon's"),
 (r"^Alfies.*", "Alfie's"),
 (r"^Jameson Distillery Bow St\.$", "Jameson Distillery Bow St"),
 (r"^Cork University Maternity Hospital.*", "Cork University Maternity Hospital"),
 (r"^Mater Misericordiae University Hospital$", "Mater Hospital"),
 (r"^The Manhattan-Beer & Food Co$", "The Manhattan"),
 (r"^Connolly Hospital Main Entrance One Shop$", "Connolly Hospital"),
 (r"^LoSt LaNe$", "Lost Lane"),
 (r"^ABBEYDORNEY GAA CLUB$", "Abbeydorney GAA Club"),
 (r"^The Deadman's lnn$", "The Deadman's Inn"),
 (r"^MEMA'S$", "Mema's"),
 (r"^Point Square Entrance$", "Point Square"),
 (r"^O'Reilly's bar$", "O'Reilly's"),
 (r"^The Stags Head$", "The Stag's Head"),
 (r"^Devitts Pub$", "Devitt's"),
 (r"^Kehoes Pub$", "Kehoe's"),
 (r"^Gleeson's$", "Gleeson's Fresh Foods"),
 (r"^The Student Centre \(UCC\)$", "UCC Student Centre"),
 (r"^J\.Kavanagh's, Dalkey$", "J. Kavanagh's Dalkey"),
]
def clean(n):
    n = n.strip()
    for pat, rep in CLEAN:
        m = re.match(pat, n)
        if m: return rep(m) if callable(rep) else rep
    return n

def cat(n, raw):
    s = (n + " " + raw).lower()
    if re.search(r"hospital|maternity|a&e|a\+e|emergency|children's health|pharmacia", s): return "Hospitals & healthcare"
    if re.search(r"hotel|lodge|kilford arms|court yard", s): return "Hotels"
    if re.search(r"copper face|pygmalion|tapped|soho|disndat|the george|grand social|workman|whelan|the palm|capitol|dicey|harley|nolita|arcadia|pawn shop|lost lane|myos|church cafe", s): return "Nightclubs & late bars"
    if re.search(r"rds|zoo|convention|shelbourne park|goffs|tattersall|equestrian|jameson|gaa|clubhouse bar|sporting emporium", s): return "Venues, sport & attractions"
    if re.search(r"tesco|londis|shopping|liffey valley|the square|point square|marina market|coach station|junction 14|mv cill|gleeson|merchants quay|ucc|ucd|bewley|thunder road|cafe|café|pizza|mema|pye|lemon & duke|restaurant & cocktail|fade street|alfie|the comet|goat bar", s):
        return "Restaurants & cafés" if re.search(r"cafe|café|pizza|mema|pye|lemon|bewley|fade|alfie|comet|goat|thunder|poolside|gleeson", s) else "Retail, transport & campus"
    return "Pubs & bars"

seen = {}
for raw in rows:
    n = clean(raw)
    if n in seen: seen[n]["locations"] += 1; continue
    logo = logos.get(raw) or next((v for k, v in logos.items() if clean(k) == n), None)
    seen[n] = {"name": n, "category": cat(n, raw), "logo": logo, "locations": 1}
venues = list(seen.values())
# logos first in their original "best accounts" order, then the rest
json.dump(venues, open("venues.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(rows), "rows ->", len(venues), "brands;", sum(1 for v in venues if v["logo"]), "with logos")
print(Counter(v["category"] for v in venues))
missing = set(logos) - {r for r in rows}
print("logo keys not in sheet:", missing)
for c in sorted(set(v["category"] for v in venues)):
    print("\n##", c, ":", ", ".join(v["name"] for v in venues if v["category"] == c))

# Locations for the logo venues (street/area where well known). Unknown ones are left blank and fall back to the venue type.
LOC = {
 "37 Dawson Street": "Dawson Street, Dublin 2", "Alfie's": "South William Street, Dublin 2", "Beaumont Hospital": "Beaumont, Dublin 9",
 "Café en Seine": "Dawson Street, Dublin 2", "Clayton Hotel Ballsbridge": "Ballsbridge, Dublin 4", "Connolly Hospital": "Blanchardstown, Dublin 15",
 "Copper Face Jacks": "Harcourt Street, Dublin 2", "Cork University Hospital": "Wilton, Cork", "Devitt's": "Camden Street, Dublin 2",
 "Dicey's Garden": "Harcourt Street, Dublin 2", "Doheny & Nesbitt": "Baggot Street, Dublin 2", "Dublin Zoo": "Phoenix Park, Dublin 8",
 "Flannery's Bar": "Camden Street, Dublin 2", "Liffey Valley": "Clondalkin, Dublin 22", "Gibney's of Malahide": "Malahide, Co. Dublin",
 "Harcourt Hotel": "Harcourt Street, Dublin 2", "J. T. Pim's": "South Great George's Street, Dublin 2", "Jameson Distillery Bow St": "Smithfield, Dublin 7",
 "Kehoe's": "South Anne Street, Dublin 2", "McDonnell's Bar & Beer Garden": "Newbridge, Co. Kildare", "Merchants Quay Shopping Centre": "Cork city",
 "O'Donoghue's": "Merrion Row, Dublin 2", "O'Reilly's": "Tara Street, Dublin 2", "Children's Health Ireland at Crumlin": "Crumlin, Dublin 12",
 "Portiuncula University Hospital": "Ballinasloe, Co. Galway", "Pygmalion": "South William Street, Dublin 2", "RDS": "Ballsbridge, Dublin 4",
 "Searsons": "Baggot Street, Dublin 4", "Shelbourne Park": "Ringsend, Dublin 4", "St James's Hospital": "James's Street, Dublin 8",
 "St Vincent's University Hospital": "Elm Park, Dublin 4", "Temple Bar Hotel Dublin": "Temple Bar, Dublin 2", "Tesco": "Temple Bar, Dublin 2",
 "The Auld Dubliner": "Temple Bar, Dublin 2", "The George": "South Great George's Street, Dublin 2", "The Gibson Hotel": "Point Square, Dublin 1",
 "The Gleneagle Hotel & Apartments": "Killarney, Co. Kerry", "The Harbour Bar": "Bray, Co. Wicklow", "The Lombard": "Dublin 2",
 "The Martello Hotel": "Bray, Co. Wicklow", "The National Maternity Hospital": "Holles Street, Dublin 2", "The Norseman": "Temple Bar, Dublin 2",
 "The Old Storehouse Bar and Restaurant": "Temple Bar, Dublin 2", "The Quays Galway": "Quay Street, Galway", "The Quays Temple Bar": "Temple Bar, Dublin 2",
 "The Sallynoggin Inn": "Sallynoggin, Co. Dublin", "The Stag's Head": "Dame Court, Dublin 2", "The Workman's Club": "Wellington Quay, Dublin 2",
 "Wexford General Hospital": "Wexford", "Whelan's": "Wexford Street, Dublin 2",
 "Pawn Shop": "Dame Street, Dublin 2", "Tapped Late Bar": "Nassau Street, Dublin 2", "Disndat": "Dame Court, Dublin 2",
 "Lemon & Duke": "Off Grafton Street, Dublin 2", "J.R. Mahon's": "Burgh Quay, Dublin 2", "The Galway Hooker Bar": "Heuston Station, Dublin 8",
 "Slattery's": "Capel Street, Dublin 1",
}
for v in venues: v["location"] = LOC.get(v["name"], "")
json.dump(venues, open("venues.json", "w"), indent=1, ensure_ascii=False)
print("logo venues without location:", [v["name"] for v in venues if v["logo"] and not v["location"]])
