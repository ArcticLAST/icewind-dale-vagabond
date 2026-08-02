# Icewind Dale for Vagabond — Creature Roster Status

**436 actors live in the Foundry world** — 207 creature stat blocks covering **201/201** of the
unnamed types on the adventure roster (`idrotf-creature-list.md`), plus 211 named individuals
and 18 major figures.

```
Actors → Icewind Dale
  ├─ Monsters (207)
  │   ├─ Cryptid (50)      ├─ Beasts (48)       ├─ Humanlike (34)
  │   ├─ Undead (22)       ├─ Artificials (19)  ├─ Outers (17)
  │   ├─ Primordials (12)  └─ Fae (5)
  └─ NPCs (229)
      ├─ Villains (12)                  ├─ Chapter 3: Sunblight (7)
      ├─ Key NPCs (6)                   ├─ Chapter 5: Auril's Abode (13)
      ├─ Introduction (1)               ├─ Chapter 6: Caves of Hunger (10)
      ├─ Chapter 1: Ten-Towns (111)     ├─ Chapter 7: Doom of Ythryn (16)
      ├─ Chapter 2: Icewind Dale (48)   └─ Appendix (5)
```

Monster subfolders follow the live `beingType` field. Villains / Key NPCs holds the 18 major
recurring figures and is deliberately left on the old alignment split; every *other* named
individual is filed by the chapter they primarily appear in.

## Named NPCs (211)

Each is a copy of an existing stat block, renamed, with the individual's own blurb prepended to
the description and a `flags.icewindDale` record of `{namedNpc, statBlock, chapter}` so you can
always see which chassis it came from. Source: `creatures/named_npcs.json`.

Where the roster list and the adventure text disagreed, the **adventure text won**:

| NPC | List said | Book says | Built as |
|---|---|---|---|
| Marta Marthannis | warden | "lawful good human **mage**" | Mage |
| Ertgard | "undead warrior" | an aged, deaf **frost giant** | Frost Giant |
| Mjenir | Reghed shaman | 5e.tools stats him as a **druid** | Druid |
| Hruna / Korux / Storn | "disguised beings" | three **Clan Battlehammer dwarves** with ice picks | Battlehammer Dwarf |
| Manafek | "Karkolohk leader" | the goblin **healer**, not a boss | Goblin, Warrior |
| Jil Torbo | councilor | "neutral halfling **noncombatant**" | Commoner |
| Kingsport | — | Medium **CR 0** giant penguin, 5 HP | Seal chassis (an Axe Beak would have been far too strong) |
| Dzaan | Red Wizard | book reuses his **simulacrum's** stat block | Dzaan's Simulacrum |
| F'yorl | captive mind flayer | **CR 0, ~9 HP** as encountered | full Mind Flayer, with the starvation noted in the description |

**Two creatures were missing from the roster list entirely** and have been added to Monsters:
**Headless Iron Golem** (CR 10, Ythryn) and **Knight of the Black Sword** (cult fanatic, Ythryn).

Nine named NPCs have their own portrait art on 5e.tools rather than a generic stat-block token
(Kadroth, Kingsport, Mjenir, Dzaan, Vaelish Gant/Prisoner 237, F'yorl, Aruk Thundercaller, and
both new Ythryn creatures) — those use it.

**Deliberately not created** (no stat block — corpses, illusions, objects): Vurnis, Meltharond,
Stygiarus, Silksmith Mixyll, Nabira Moarskull. Professor Skant is already a Relic in `items/`.

## How the roster was assembled

| Source | Count | Notes |
|---|---|---|
| Hand-converted, batches 1–5 | 56 | `build_bestiary.py` — the original signature/named pass |
| Hand-converted, batch 6 | 78 | `build_bestiary_2.py` — the full-adventure audit pass |
| Copied from core compendiums | 89 | unmodified `vagabond.bestiary` / `vagabond.humanlike` data, renamed where the book uses a different label |

All 134 hand-converted creatures are cross-validated: a pure-Python port of the TL formula
(`tl_calc.py`) is checked line-for-line against the **actual extracted Creature Forge JS**
run in a Node `vm` (`scratchpad/validate_all.js`). Current status: **all 134 match exactly**.

## Batch 6 contents (the audit pass)

- **Common recurring NPCs** the campaign runs on: Tribal Warrior, Priest, Cult Fanatic, Druid,
  Bandit Captain, Frost Druid, Drow Elite Warrior/Mage, Battlehammer Dwarf, plus elite variants
  (Goblin Boss, Orc War Chief, Orc Eye of Gruumsh, Quaggoth Thonot, Half-Ogre).
- **Ch6–7 content**, previously the weakest area: Remorhaz + Young Remorhaz, Demilich
  (Iriolarthas), Arcanaloth (Scrivenscry), Tomb Tapper, Helmed Horror, Brain in a Jar
  (Veneranda), Night Hag (the three Aunties), the three living spells, and the full slaad trio.
- **Undead/fiend gap-fill**: Specter, Poltergeist, Ogre Zombie, Icewind Kobold Zombie,
  Flameskull, Bearded Devil, Shadow Demon, Nothic, Grell, Phase Spider, Spitting Mimic,
  Gnoll Fang of Yeenoghu, Ice Piercer, Water Weird, Dryad.
- **Id Ascendant crew**: Gnome Ceremorph, Gnome Squidling.
- **Beasts and flavour**: the goat/walrus/seal/raven/fox/hare set, Plesiosaurus, Giant Vulture,
  Awakened White Moose, Knucklehead Trout, three Young Griffon sizes, and Iriolarthas's six
  chimeric animals.
- **Named uniques**: Sephek Kaltro (→ Villains), Spellix Romwod (→ Key NPCs).

## Design decisions worth remembering

- **TL math**: `TL = ceil10( (2*armor + hp/10)/4 + dpr/6 )`. Every hand build is validated
  against the real Creature Forge engine before pushing.
- **CR→TL is calibrated against the core compendium, not raw CR.** Vagabond's own humanlike
  tier is heavily compressed (core Veteran = CR 3 → TL 2.4; core Assassin = CR 8 → TL 2.3;
  core Goblin = CR 1/4 → TL 1.2). Matching the compendium's internal scale matters more than
  hitting CR ±0.5 exactly, especially at the low end where CR 0–1/4 creatures naturally land
  around TL 0.5–1.5.
- **DPR convention**: only steady/at-will attacks are `dpr:true`. Recharge/limited bursts are
  `dpr:false`. For divine/arcane casters, the core Acolyte precedent counts *only* the signature
  offensive cast, not the backup melee weapon.
- **Vagabond's "Small" size derives 1 HP per HD**, not 4.5 — it's reserved for rat/cat-scale
  creatures. Two creatures that are Tiny/Small in D&D (**Demilich**, **Flameskull**) are built
  as **Medium** so the HD→HP derivation gives them sane HP; otherwise the campaign's final boss
  would sit on 36 HP. Noted inline in `build_bestiary_2.py`.
- **Vagabond has no burrow speed** (`climb/cling/fly/phase/swim` only) — burrowers describe it
  in an ability instead (Remorhaz, Ice Tunneler).
- **Valid combat zones are only `frontline`/`midline`/`backline`.** "Skirmish" is not a zone.
- **Vagabond's universal Defending rule already reduces damage on a passed Save** — don't
  restate "half damage on a pass" on breath/AoE actions.
- **Foundry has no boss HP-doubling.** `health.max` derives from `hd`, so `foundry_export.py`
  doubles an *effective* hd for `boss:true` creatures (Auril's forms, the Demilich).
- **beingType choices are per-install** — confirm live via `CONFIG.VAGABOND.*`, never trust the
  GitHub repo ("Hellspawn" exists upstream but not in this world's v5.4.1).
- **Vagabond has no Radiant or Force damage type** — radiant → `magical`, force → `magical`.
- **Foundry does NOT derive token footprint from `system.size`.** `prototypeToken.width/height`
  is a separate field, and an actor that omits it silently renders as a 1×1 Medium no matter what
  its stat block says. The core compendium's convention (confirmed against `vagabond.bestiary`) is
  **small/medium 1×1, large 2×2, huge 3×3, giant 4×4, colossal 5×5**; `foundry_export.py` now
  emits it via `TOKEN_SCALE`, and deliberately raises a `KeyError` on an unmapped size rather than
  defaulting. This bit every hand-built creature once — 46 actors (Remorhaz, Arveiaturace, every
  frost giant, all the Large slaadi) were fighting on a single square. Note that **re-seating an
  actor onto a different stat block does not update its footprint either**, so fix it explicitly
  after any chassis swap.

## Token art

All 223 actors use locally-stored art in `<FoundryData>/worlds/vagabond-game/tokens/`.

**Hotlinking to 5e.tools cannot work for tokens.** Portraits render fine from a remote URL, but
Foundry's canvas uses WebGL/PIXI, which requires CORS headers for texture loading; 5e.tools
sends none. Confirmed by a three-way test — plain `<img>` loads, `crossOrigin="anonymous"`
fails, `fetch(mode:"cors")` throws. Files must be downloaded (PowerShell bypasses CORS
entirely) and served same-origin by Foundry itself.

Fixed along the way: 19 actors whose `prototypeToken.name` still carried the *source*
compendium name (Snowy Owlbear read "Owl Bear", Awakened Tree read "Treant", Telepathic
Pentacle read "Hydra"), and the core Assassin's token, which pointed at an uninstalled
`too-many-tokens-dnd` module path with `randomImg` on.

## Deliberate substitutions
Mammoth↔Mastodon · Sea Lion↔Giant Walrus art · Sperm Whale←core Whale, Blue ·
Axe Beak←Phorusrhacos · Elk←Deer · Lonelywood Banshee←Banshee · Telepathic Pentacle←Hydra
(the book states it *is* a reskinned hydra) · Silver Dragon Wyrmling←white-hatchling chassis
with silver breath.

## Not built (deliberate)
- **F'yorl** — CR 0, no attacks, pure roleplay filler.
- **Named individuals who reuse a generic stat block** (most town Speakers, innkeepers, the
  goliath tribe rosters, Iriolarthas's eight apprentices, Tekeli-li, Ajka/Grava, Krintaas…).
  Every stat block they need now exists; they're a naming exercise, not a conversion one.

## Files
- `bestiary.json` / `bestiary_all.json` — Creature Forge bundles (56 / all 134)
- `build_bestiary.py` (batches 1–5) · `build_bestiary_2.py` (batch 6) · `tl_calc.py` ·
  `foundry_export.py` · `write_bundle_all.py`
- `foundry_actors.json` (56) · `foundry_actors_batch6.json` (78)
- `notes/creature-audit-full-crossref.md` — the audit this pass was built from

## Magic Items (74 live, covering 65/65 on the roster)

```
Items → Icewind Dale
  ├─ Wands, Staffs & Rings (10)   ├─ Scrolls (11)
  ├─ Weapons & Armor (6)          ├─ Potions (11)
  ├─ Wondrous Items (33)          └─ Unique & Plot Items (3)
```

### How Vagabond actually builds items — the conventions that matter

- **A magic item is `type:"equipment"` with `system.equipmentType:"relic"`.**
- **`system.lore` is a short CLASSIFIER, not flavour text.** The core compendium uses
  `"Relic Helmet (Bound)"`, `"Fabled Relic Longsword"`, `"Relic Furs (Consumable)"` — i.e.
  `[Fabled] Relic <Kind> [(Bound)] [(Consumable)]`. The original 12 items had narrative prose in
  this field; that has been corrected and the flavour moved into the description.
- **Descriptions are structured**: one flavour sentence, "…has the following Powers:", then a
  `<ul>` of `<li><strong>Power:</strong> effect</li>`.
- **Cost is the SUM of the item's Powers**, taken from the official Powers table that lives in
  `vagabond.relics` (`Bonus - Weapon +1` = 100g, `Utility - Burning I` = 4000g,
  `Fabled - Vorpal` = 50000g, and so on). `build_items_2.py` transcribes that table verbatim and
  derives every price from it rather than inventing numbers.
- **Potions are NOT relics.** They are `equipmentType:"alchemical"` / `alchemicalType:"potion"`
  and cost *tens* of gold (Healing I = 2g50s, Healing III = 250g), not thousands.
- **Bags and quivers are `type:"container"`** with `slots` + `capacity`, not equipment.
- **The metal is spelled `mythral`**, not "mithral". A wrong value fails validation *silently* —
  the item simply never gets created, with no thrown error. Cost me one item on the first push.
- **Never leave a Power on its bare category label or its generic table text.** This is the single
  easiest thing to get wrong. The Powers table entries are *pricing categories*, not finished rules:
  `Fabled - Blasting` reads "Can send a beam of magic energy to attack", which says nothing about
  damage, range or charges. Core always does two things to them:
  1. **Renames** the Power to something item-specific — Dyrnwyn's Bane is "Evil's Bane", Sunder's is
     "Giants Bane", Skyhowel has "Shocktongue" and "Crack the Sky", Voidedge has "Haste". A label
     reading just "Unique", "General" or "Blasting" is an unfinished item.
  2. **Specialises the text** with the actual numbers — Moonlit Blade's Blasting names the delivery,
     range and rider; Boots of Levitation restate Levitation in terms of Speed.

  The exceptions are flat bonuses (`(+2) Weapon: Deals an extra +2 damage.`) and self-contained
  Fabled powers (Vorpal Blade restates Vorpal verbatim) — those are complete as written.
  `build_items_2.py` enforces this with a `LABELS` map, and there is a standing audit that flags any
  Power whose text still matches the compendium default.

### Charges — house rule (deliberate divergence from D&D)

Vagabond is a low-bookkeeping system, so **no item rolls to recover charges and none has a large
pool**. Every charged item uses one of two shapes:

- **3 charges** — wands, and the Ring of the Ram
- **5 charges** — staffs, and the Abracadabrus

All of them return **in full after a Rest**. No `1d6+1 at dawn`, no 20-charge pools, no
"regains half its charges", and no d20 to see if the item crumbles. Items with a fixed number of
physical uses (Chime of Opening, Bag of Tricks, Necklace of Fireballs beads) were cut down to
3–5 as well, and "once per day" was reworded to "once per Rest" throughout so everything keys off
the same clock. There is a standing audit that flags any reappearance of `at dawn`, `per day`,
`regains Nd…`, or a pool larger than 5.

### Icons
All 74 items use one of **20 category icons** in
`<FoundryData>/worlds/vagabond-game/item-icons/`. The mapping is keyed off the **kind** parsed out
of `system.lore` (`Fabled Relic Staff (Bound)` → `Staff`), so a new item inherits the right icon
automatically provided its `lore` classifier is correct — see `items/icon_map.md` for the table and
the four deliberate approximations.

### Sourcing
Copied straight from core where an equivalent existed: Bag of Holding, Helm of Telepathy, and six
potions (Healing I/II, Cold Resistance, Gaseous Form, Invisibility, Control Beast→Animal
Friendship). Everything else is a hand conversion in `items/build_items_2.py`.

Spell scrolls map D&D spells onto the Vagabond spell list: animal friendship→Beast,
divination→Guide, fireball→Erupt, invisibility→Fade, knock→Knock, lesser restoration→Cure,
mass cure wounds→Cure, plane shift→Portal, remove curse→Dispel.

**Vagabond has no Radiant damage type**, so Rime's *potion of radiant resistance* is built as a
**Potion of Warding** (resistance to magical damage) — same reflavour rule already used for
Auril's radiant vulnerability and the Chardalyn Dragon's breath.

`Ythryn Mythallar` carries `Fabled Relic Fixture` with no `(Bound)` tag — it's a plot fixture
nobody carries or attunes to, so forcing `requiresBound` on it would be wrong.
