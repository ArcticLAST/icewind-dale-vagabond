# Portable module — `icewind-dale-vagabond`

**Status: built and populated.** 33.6 MB, fully self-contained.

## What it is

```
Data/modules/icewind-dale-vagabond/
  module.json              v1.0.0 · compat Foundry 12–13 · requires vagabond 5.4.1+
  assets/tokens/           231 creature tokens
  assets/item-icons/        20 item icons
  packs/
    idrotf-adventure       1  Adventure  — "Icewind Dale (Complete)"
    idrotf-monsters      207  Actors     in 8 Being Type folders
    idrotf-npcs          229  Actors     in 10 folders (Villains, Key NPCs, per chapter)
    idrotf-items          74  Items      in 6 folders
    idrotf-journals        3  Journals
    idrotf-tables         10  RollTables
```

## Using it

**Same machine, any world** — enable the module, open *Compendiums → Icewind Dale — Adventures →
**Icewind Dale (Complete)*** → Import. All 436 actors, 74 items, 3 journals, 10 tables and all
30 folders land in the world with structure intact.

**A different machine** — copy the whole `icewind-dale-vagabond` folder into that install's
`Data/modules/`, enable, import. Nothing else to do; the system just has to be Vagabond 5.4.1+.

The five content packs can also be browsed and drag-dropped individually if you only want part of it.

## The two things that made it portable

**1. Assets moved out of the world.** Everything used to sit in `worlds/vagabond-game/`, which is
machine- and world-locked. All 251 images now live in the module, and all **510 image paths on
actors and items were re-pointed** to `modules/icewind-dale-vagabond/assets/…` and verified to
resolve. Foundry serves files from `Data/modules/` whether or not the module is *active*, so this
also can't break the source world.

**2. Roll table results are TEXT, not document links.** Document-type results store a UUID that has
to be remapped on import; that is the classic way a shipped table ends up pointing at nothing. Text
results always survive.

## Gotcha worth remembering: LevelDB does not flush on write

Foundry v11+ compendiums are LevelDB. After populating the packs, they read back perfectly in the
running session while the on-disk `.log` files were still **0 bytes** — the writes sit in an
in-memory memtable. They are only flushed when the world shuts down cleanly.

So: **after writing to a compendium pack, cycle the world and re-check the file sizes on disk
before believing the data is really there.** Post-shutdown the packs went from 66 bytes each to
337 KB / 340 KB / 384 KB / 65 KB / 17 KB / 8 KB.

Note that relaunching a world needs the Foundry **administrator password**, so don't shut a world
down without it to hand.

## Verification (post-restart, read back out of the packs)

Everything below was checked against the **compendium contents**, not the world documents, so it
reflects what actually ships:

- 436 actors / 74 items / 10 tables / 3 journals present after a full world restart
- **251 unique asset paths, all resolving**, all inside `modules/icewind-dale-vagabond/`
- every actor: `img` == `prototypeToken.texture.src`, token name matches, in a folder, HP > 0,
  and token footprint matches its size band
- every relic carries a Powers list; all 10 tables roll successfully; all journals have pages
- folder tree reconstructs exactly: `Icewind Dale → Monsters → 8 Being Types` and
  `Icewind Dale → NPCs → Villains / Key NPCs / 7 chapters / Appendix`
- `Adventure#prepareImport({})` dry-run resolves all **553 documents** with no errors

One check fired 11 false positives — the potions, which correctly have no Powers list because they
are `alchemical`, not relics. Core's own potions are the same.

## Scenes

11 general encounter maps live in `assets/scenes/` (2500×2500 WebP, 25×25 squares at 100px —
matching the world grid exactly) with generated thumbnails in `assets/scenes/thumbs/`.

**Lighting is set for the Everlasting Rime:**

| Setting | Value | Why |
|---|---|---|
| `tokenVision` | **true** | torches and darkvision have to matter |
| `environment.darknessLevel` | **1** (+ `darknessLock`) | Icewind Dale is in perpetual night |
| `globalLight.enabled` | **false** | pitch black — a player sees **nothing** without a light source |

Verified on canvas: darkness 1, `globalLightSource.active === false`, a token with no light emits
nothing, and a token given a 20/40 torch produces a working light source.

Note this is deliberately harsher than Foundry's usual outdoor default. Dim ambient light was tried
first and rejected — the intent is that parties must carry torches into every night encounter,
which is all of them.

These maps have **no walls**, so line-of-sight isn't blocked — the darkness is what limits vision.
If you ever wall one, that scene will start blocking sight properly with no other changes needed.

Each scene carries `flags["icewind-dale-vagabond"].encounterTable` naming its matching roll table.

### Trap: `Scene#createThumbnail()` writes into the *world*, not the module

Generated thumbs landed in `worlds/vagabond-game/assets/scenes/` — a world-locked path that would
404 on any other install, silently. They were copied into the module and every reference
re-pointed (world scenes, the scene pack, and the scenes embedded in the Adventure). **Re-check
`scene.thumb` after generating thumbnails for a module.**

## Not included
No published adventure text, and no location/dungeon maps — the 11 scenes are general-purpose
encounter terrain only.
