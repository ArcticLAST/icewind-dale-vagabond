import math, json, sys

def avg_exact(n, d, m):
    if not d:
        return m
    return n * (d + 1) / 2 + m

def calc_dpr(acts):
    total = 0.0
    parts = []
    for a in acts:
        if not a.get("dpr"):
            continue
        n = a.get("n", 0)
        d = a.get("d", 0)
        m = a.get("mod", 0)
        mult = max(1, a.get("mult", 1))
        one = avg_exact(n, d, m)
        if not one:
            continue
        total += one * mult
        parts.append((a.get("name") or a.get("kind"), one, mult, one * mult))
    return total, parts

def calc_tl(creature):
    armor = creature.get("armor", 0)
    hp = creature.get("hp", 0)
    dpr, parts = calc_dpr(creature.get("acts", []))
    a = armor * 2
    b = hp / 10
    c = dpr / 6
    defn = (a + b) / 4
    raw = defn + c
    tl = math.ceil(raw * 10 - 1e-9) / 10
    return {"tl": tl, "a": a, "b": b, "c": c, "def": defn, "raw": raw, "dpr": dpr, "parts": parts}

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    creatures = data.get("creatures", [data]) if isinstance(data, dict) else data
    for c in creatures:
        r = calc_tl(c)
        print(f"{c.get('name'):30s} TL={r['tl']:<6} (def={r['def']:.2f} dpr={r['dpr']:.2f} armor={c.get('armor')} hp={c.get('hp')})")
        for p in r["parts"]:
            print(f"    {p[0]:20s} one={p[1]:.2f} x{p[2]} = {p[3]:.2f}")
