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

## Backing up (after you change anything in Foundry)

Foundry holds the live copy; this repo is the backup. To save changes:

1. **Shut the Foundry world down.** Not optional — compendium packs are LevelDB and buffer
   writes in memory, flushing to disk only on a clean world shutdown. Sync with the world
   open and you can capture a half-written database.
2. **Open PowerShell** and paste this in one line:

   ```powershell
   cd "D:\claude projects\Icewind Dale Vagabond"; .\sync-module.ps1; git add -A; git commit -m "what changed"; git push
   ```

`sync-module.ps1` copies the live module out of Foundry's data folder into `module/` here,
then git saves and uploads it.

## Restoring, or setting up on a new machine

1. Install Foundry and the **Vagabond** system (5.4.1+).
2. **Open PowerShell** and run:

   ```powershell
   git clone https://github.com/ArcticLAST/icewind-dale-vagabond.git
   cd icewind-dale-vagabond
   .\sync-module.ps1 -Restore
   ```

   That last line copies `module/` into that machine's Foundry data folder.
3. Launch Foundry, open your world, and enable the module in
   **Settings -> Manage Modules**. The world reloads.
4. Open **Compendiums -> Icewind Dale - Adventures -> *Icewind Dale (Complete)*** and click
   **Import**.

All 436 actors, 74 items, 11 scenes, 10 tables, 3 journals and 31 folders land with folder
structure intact.

## Regenerating creatures from source

```bash
cd creatures
py build_bestiary.py        # writes bestiary.json
py write_bundle_all.py      # writes bestiary_all.json  (all 134 hand-converted)
py foundry_export.py        # writes the Foundry actor JSON
```

`notes/session-01-signature-batch.md` documents every design decision and house rule —
read it before changing conversion maths.
