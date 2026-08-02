# -*- coding: utf-8 -*-
"""Writes the combined Creature Forge bundle (batches 1-5 + batch 6)."""
import json, datetime
from build_bestiary import creatures
from build_bestiary_2 import creatures2

all_creatures = creatures + creatures2

names = [c["name"] for c in all_creatures]
dupes = sorted({n for n in names if names.count(n) > 1})
if dupes:
    raise SystemExit(f"Duplicate creature names in the combined bundle: {dupes}")

bundle = {
    "format": "vagabond-bestiary",
    "version": 1,
    "exported": datetime.datetime.utcnow().isoformat() + "Z",
    "count": len(all_creatures),
    "creatures": all_creatures,
}
out = r"D:\claude projects\Icewind Dale Vagabond\creatures\bestiary_all.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(bundle, f, indent=2, ensure_ascii=False)
print(f"Wrote {out} with {len(all_creatures)} creatures "
      f"({len(creatures)} original + {len(creatures2)} new)")
