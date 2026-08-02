# Icewind Dale: Rime of the Frostmaiden — Vagabond conversion

A complete conversion of *Rime of the Frostmaiden* for the **Vagabond** system in Foundry VTT,
packaged as a portable module.

> **Keep this repository private.** It contains stat blocks and magic items converted from
> published Wizards of the Coast material. Fine for your own table and your own machines;
> not something to publish.

## Layout

```
module/           the Foundry module — this is the deliverable
  module.json
  assets/         231 creature tokens · 20 item icons · 11 maps + thumbs
  packs/          7 LevelDB compendiums

creatures/        the conversion pipeline (Python)
  tl_calc.py              pure port of Vagabond's TL/DPR formula
  build_bestiary.py       batches 1–5   (56 creatures)
  build_bestiary_2.py     batch 6       (78 creatures)
  foundry_export.py       Creature Forge schema -> Foundry actor schema
  named_npcs.json         211 named NPCs -> which stat block each reuses

items/            item pipeline + the 20-icon mapping
notes/            design decisions, audits, packaging notes
```

## Contents

| | |
|---|---|
| Actors | **436** — 207 monsters, 229 NPCs |
| Magic items | **74** |
| Encounter maps | **11** (25×25 @ 100px) |
| Roll tables | **10** |
| Journals | **3** |

Covers **201/201** unnamed creature types and **65/65** magic items on the adventure roster.

## Backing up

Foundry is the live copy; this repo is the backup. Before committing:

```powershell
.\sync-module.ps1        # copies the live module into module/
git add -A
git commit -m "…"
git push
```

**Shut Foundry down first.** Compendium packs are LevelDB and buffer writes in memory — they
only flush to disk on a clean world shutdown, so copying a pack while the world is open can
capture a half-written database.

## Restoring, or setting up on a new machine

```powershell
git clone <your-repo-url>
cd "Icewind Dale Vagabond"
.\sync-module.ps1 -Restore      # copies module/ into this machine's Foundry
```

Then in Foundry: enable the module, open **Compendiums → Icewind Dale — Adventures →
*Icewind Dale (Complete)*** and import. All 436 actors, 74 items, 11 scenes, 10 tables,
3 journals and 31 folders land with folder structure intact.

Requires the **Vagabond** system, 5.4.1 or later.

## Regenerating creatures from source

```bash
cd creatures
py build_bestiary.py        # writes bestiary.json
py write_bundle_all.py      # writes bestiary_all.json  (all 134 hand-converted)
py foundry_export.py        # writes the Foundry actor JSON
```

`notes/session-01-signature-batch.md` documents every design decision and house rule —
read it before changing conversion maths.
