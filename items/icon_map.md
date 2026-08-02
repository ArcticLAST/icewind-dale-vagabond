# Item icon mapping (Option B — 20 icons)

Icons live in `<FoundryData>/worlds/vagabond-game/item-icons/` and are referenced as
`worlds/vagabond-game/item-icons/<file>.png`. Mapping is driven by the item's **kind**, which is
parsed out of its `system.lore` classifier (`Fabled Relic Staff (Bound)` → `Staff`), so any new
item picks up the right icon automatically as long as its `lore` is set correctly.

| Icon file | Kinds it covers | Items |
|---|---|---|
| `potion-ball.png` | Potion, Vial | 12 |
| `tied-scroll.png` | Scroll | 11 |
| `minerals.png` | Stone, Gem, Crystal, Cube, Pearl, Figurine | 7 |
| `orb-wand.png` | Wand | 5 |
| `swap-bag.png` | Bag, Container | 4 |
| `cape.png` | Cloak | 4 |
| `crystal-ball.png` | Orb, Fixture, Lenses | 4 |
| `jug.png` | Jug, Cauldron, Chest | 3 |
| `gem-chain.png` | Amulet, Necklace | 3 |
| `energise.png` | Cell, Pistol, Rifle | 3 |
| `wizard-staff.png` | Staff | 3 |
| `bugle-call.png` | Horn, Chime | 2 |
| `lantern-flame.png` | Lantern, Globe | 2 |
| `visored-helm.png` | Hat, Helmet | 2 |
| `trident.png` | Trident, Hook | 2 |
| `power-ring.png` | Ring | 2 |
| `black-book.png` | Tome, Spellbook | 2 |
| `battle-axe.png` | Battleaxe | 1 |
| `boots.png` | Boots | 1 |
| `chest-armor.png` | Chain (armor) | 1 |

## Four deliberate compromises

These are the only items where the icon is an approximation rather than a match. Everything else
is literal.

- **Hook of Fisher's Delight → `trident`** — it's a tiny silver fishhook; the trident is the only
  fishing-adjacent icon in the set.
- **Eyes of Minute Seeing → `crystal-ball`** — worn lenses, matched on "optical glass".
- **Figurine of Wondrous Power (Silver Raven) → `minerals`** — a small carved object.
- **Abracadabrus → `jug`** — it's a gemstone-studded chest, filed under the vessel icon.

If you ever want these exact, the four extra icons to supply would be: **fishhook**, **spectacles /
lenses**, **bird figurine**, **treasure chest**.
