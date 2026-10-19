import json, re, sys
html = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S)
d = json.loads(m.group(1))
# Persoenliches entfernen (Repository ist oeffentlich)
def sauber(s):
    s = re.sub(r'\s*\((Tickets gekauft|gebucht[^)]*)\)', '', s)
    return s.replace('Tickets gekauft', '').strip()
for k in d.get("kuenstler", []):
    for t in k.get("t", []):
        for f in ("o", "s"):
            if f in t: t[f] = sauber(t[f])
q = d.get("quellen", "")
hinweise = []
for key in ("Twente-Bricks", "Meyer Werft"):
    i = q.find(key)
    if i >= 0:
        teil = q[i:]
        nxt = [teil.find(x, 1) for x in ("Twente-Bricks", "Meyer Werft") if teil.find(x, 1) > 0]
        teil = teil[:min(nxt)] if nxt else teil
        hinweise.append(teil.strip().rstrip('.'))
d["hinweise"] = hinweise
json.dump(d, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(d.get("stand"), "|", len(d["kuenstler"]), "Künstler |", hinweise)
