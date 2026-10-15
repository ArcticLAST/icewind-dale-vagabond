# Icewind Dale for the vagabond-rpg system

This folder is the Foundry module `icewind-dale-vagabond-rpg`. It holds the same content as `../module`
(which targets the community `vagabond` system), converted for
[vagabond-rpg](https://github.com/ArcticLAST/vagabond-rpg) 0.6.18 or later.

| Pack | Contents |
|---|---|
| Adventure | **Icewind Dale (Complete)**: imports everything below with its folders |
| Monsters | 207 creatures in 8 Being Type folders |
| NPCs | 229 NPCs: Villains, Key NPCs, one folder per chapter |
| Magic Items | 67 Relics and potions |
| Encounter Maps | 11 scenes |
| Reference | 3 journals |
| Tables | 10 roll tables |

## Rebuilding

```
npm install
node tools/extract-old.mjs ../scratch/old-json       # old LevelDB packs -> JSON
node tools/convert.mjs ../scratch/old-json            # -> src/packs (needs a vagabond-rpg clone, see below)
node tools/build-packs.mjs                           # src/packs -> packs (LevelDB)
```

`convert.mjs` reads Saves and damage types with the system's own `module/rules.mjs`, so it needs a clone of
vagabond-rpg. It looks in `../../vagabond-rpg` unless `VAGABOND_SYSTEM` says otherwise.

## Conversion choices

- Every document keeps its old `_id`, so the Adventure and folders line up.
- Statblock Actions become `action` Items: the old note becomes the tags (`Cast, Near Cone | Endure`), damage
  reads `12 (d10+7)`, `Cd6` recharges read `Recharge Cd6`, and "2xClaw" Combos read `2×Claw`.
- The old system's `physical` immunity is mundane damage, written `Physical from non-Relics`.
- Vagabond has no Necrotic or Psychic damage: those attacks deal Magic damage. Immune lines keep the words.
- Statuses an attack inflicted stay in its text; the system doesn't apply statuses on hit.
- Items the core system already has are left out (Bag of Holding, Helm of Telepathy, five potions).
- Weapon and armor Relics use a core base item (Battleaxe, Spear for the Trident, Handgun, Rifle, Mace for the
  Wand of Orcus, Medium Armor for Mithral). Charges become Uses. Spell names link to the core Spells compendium.
- Creature tokens and maps are the old module's art. Items use the system's category icons.
