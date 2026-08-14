# Vagabond system bug: Active Effects never apply

**Status: diagnosed, fixed, verified.** The fix is **bundled into the Icewind Dale module**
(`module/scripts/effect-changes-shim.mjs`, declared as an `esmodule` in its `module.json`).

It briefly lived as a standalone `vagabond-effect-fix` module. That is architecturally tidier -
a global monkeypatch really shouldn't ride along with content - but it meant the Forge install
needed a second manifest, and an adventure whose relic Powers all silently do nothing unless you
remember a second module is a worse failure mode than an unexpected patch. Bundled wins on
reliability here, since the audience is one GM and their players.

The bundled shim stands down automatically if the standalone module is also active, so both can
coexist during a migration.

Found while investigating a report that the **Secret of Mana** perk didn't increase max mana.
It isn't a perk problem - almost nothing in the system applies.

## The bug

Every ActiveEffect in Vagabond stores its data like this:

```json
"changes": [],                                              <- Foundry applies THIS
"system": { "changes": [{ key, value, type, priority }] }   <- the data actually lives here
```

Foundry's `Actor#applyActiveEffects()` only ever iterates the native `changes` array. In the
whole system, `system.changes` is read in exactly one place - `getRollDataWithItemEffects()` in
`documents/actor.mjs` - and that only handles effects flagged `applicationMode: "on-use"`.
`applyActiveEffects` is never overridden, nothing copies one array to the other, and no
ActiveEffect data model is registered (`CONFIG.ActiveEffect.dataModels` is empty).

So every **permanent** and **when-equipped** effect is inert. Note the config UI writes to the
*native* `changes.N.key` path, so effects authored by hand in the UI work fine - only the
bundled compendium content is affected.

### Measured against Vagabond 5.4.1 - 61 of 62 effects

| Pack | Stranded |
|---|---|
| ancestries | **6 / 6** - Orc *Hulking*, Dwarf *Tough*, Elf *Naturally Attuned* |
| classes | **7 / 7** - Sorcerer *Spell-Slinger*, Merchant *Deep Pockets* |
| perks | **7 / 7** (+1 with no changes at all) |
| gear | **2 / 2** - Backpack bonus slots |
| weapons | **14 / 14** - every *Keen Property* |
| relics | **25 / 25** - every modular Power |

Zero effects anywhere used the native array.

### Proof

Level-5 Wizard, 20 max mana. Add *Secret of Mana* (`system.mana.bonus += @lvl`, so 25 expected):
mana stayed at **20**, `mana.bonus` never received anything, and `actor.appliedEffects` listed
the effect as applied with **`changes: 0`**.

> Measurement trap: read `effect._source.changes`, not `effect.changes`. Once the fix is active
> the prepared document shows a populated array, which makes the bug look like it was never there.
> An early scan reported "0 stranded" for exactly this reason.

## The fix

`module-effect-fix/scripts/effect-changes-shim.mjs` mirrors `system.changes` onto `changes` in
`ActiveEffect#prepareBaseData`, mapping Vagabond's `type` string onto Foundry's numeric
`ACTIVE_EFFECT_MODES`.

Deliberately conservative:
- only fills a `changes` array that is **already empty**, so hand-authored effects are untouched;
- becomes a silent no-op if the system is ever fixed upstream;
- writes to the prepared document only, never to stored data;
- skips entries with no `key`.

**Kept as a separate module on purpose.** It is a global monkeypatch on the system; bundling it
into the Icewind Dale content module would mean anyone importing that adventure silently gets a
system patch too.

### Verified after enabling

- 60 of 61 stranded effects now present populated changes
- Wizard + Secret of Mana: mana **20 -> 25**
- Orc ancestry: inventory slots **0 -> 2**
- Tough: max HP **1 -> 5**
- Pack Mule: slots **2 -> 4**
- Relic *Movement - Swiftness II*: speed bonus **0 -> 10** once `system.equipped` is true
  (relics gate on `when-equipped`, so carrying one is not enough)

The single unrepaired effect is the system's **Warhammer**, whose change is blank
(`key: ""`) - there is nothing to apply, and the shim correctly skips keyless entries.

## Separate content bugs found (not fixed by the shim)

- **Second Wind** - has an ActiveEffect containing zero changes. Dead regardless.
- **Warhammer** - as above, a blank placeholder change.
- **Skirmisher** - "a 5 foot bonus to Speed" with no automation at all, though
  `system.speed.bonus` exists for exactly this. A handful of other perks are similar, but most
  unautomated perks genuinely need GM adjudication and are fine as prose.

## Worth reporting upstream

This is a system bug, not a content one. The maintainer could fix it in one line by having the
effect data model expose `system.changes` as `changes`, which would make this module unnecessary.
