# -*- coding: utf-8 -*-
"""
Icewind Dale magic items -> Vagabond.

Conventions taken directly from the core `vagabond.relics` / `vagabond.alchemical-items`
compendiums (Dyrnwyn, Helm of Telepathy, Phoenix Down, Potion Healing I-III):

  * A magic item is `type: "equipment"` with `system.equipmentType: "relic"`.
  * `system.lore` is a SHORT CLASSIFIER, not flavour text:
        "Relic Helmet (Bound)"   "Fabled Relic Longsword"   "Relic Furs (Consumable)"
    Flavour belongs in the description's opening sentence.
  * `system.description` is: one flavour sentence, then "...has the following Powers:",
    then a <ul> of  <li><b>Power:</b> effect</li>.
  * Cost is the SUM of its Powers, taken from the official Powers table in the
    relics compendium (POWERS below is transcribed from it verbatim).
  * Potions are NOT relics - they are `equipmentType: "alchemical"`,
    `alchemicalType: "potion"`, and cost tens of gold, not thousands.
  * Bags/quivers are `type: "container"` with slots + capacity.
"""
import json
import re

# ---------------------------------------------------------------------------
# Official Powers table, transcribed from vagabond.relics (name -> (gold, text))
# ---------------------------------------------------------------------------
POWERS = {
    "Ace - Entangle": (1000, "Target is considered Vulnerable for ending the Restrained Status."),
    "Ace - Keen": (2000, "Crit on Attack Checks 2 lower, rather than 1 lower."),
    "Ace - Long": (1000, "Its Range is 10 feet further, rather than 5 feet further."),
    "Ace - Thrown": (2000, "Deals an extra damage die when attacking by throwing it."),
    "Bane - General": (5000, "Applies to an entire Being Type."),
    "Bonus - Armor +1": (100, "+1 bonus to Armor."),
    "Bonus - Armor +2": (5000, "+2 bonus to Armor."),
    "Bonus - Protection +1": (1000, "+1 bonus to Saves."),
    "Bonus - Protection +2": (1000, "+2 bonus to Saves."),
    "Bonus - Trinket +1": (200, "+1 bonus to Spell damage."),
    "Bonus - Trinket +2": (2500, "+2 bonus to Spell damage."),
    "Bonus - Weapon +1": (100, "+1 bonus to Attack damage."),
    "Bonus - Weapon +2": (1250, "+2 bonus to Attack damage."),
    "Bonus - Weapon +3": (5000, "+3 bonus to Attack damage."),
    "Cursed - Anger": (0, "Wearer always fails Saves against Berserk."),
    "Cursed - Doom": (0, "Wearer only regains 1 Hit Point per die used for healing rolls Targeting it."),
    "Fabled - Blasting": (5000, "Can send a beam of magic energy to attack."),
    "Fabled - Soul Eater": (50000, "Those killed by it can't be resurrected unless a wish is granted to do so."),
    "Fabled - Vicious": (25000, "On a Crit, the Target takes extra damage equal to twice its HD."),
    "Movement - Levitation": (500, "Wearer is under the effects of the Levitate Spell."),
    "Movement - Swiftness I": (250, "Wearer gains a bonus +5 feet to Speed."),
    "Resistance - Repulsing": (150, "Grants Favor on Saves against the Charmed Status."),
    "Resistance - Resistance": (2500, "Favor on Saves and damage reduction against a damage source."),
    "Senses - Nightvision": (100, "Grants Darksight."),
    "Senses - Telepathy": (10000, "Grants Telepathy (Bound)."),
    "Senses - True-Seeing": (20000, "Grants All-Sight (Bound)."),
    "Utility - Ambassador": (1250, "Wielder can speak with certain Beings they normally couldn't otherwise."),
    "Utility - Holding (Rank)": (200, "Gives bonus Item Slots (Value is per bonus slot)."),
    "Utility - Infinite": (1000, "Provides an endless amount of a detailed Item that disappears in 1 Round."),
    "Utility - Invisibility I": (5000, "Skip Move to become Invisible until after it takes an Action."),
    "Utility - Radiant I": (2000, "Sheds Sunlight out to Close while Equipped."),
    "Utility - Store Spell": (0, "Reduce Caster's Maximum Mana to store a Casting of a Spell."),
    "Utility - Unique": (0, "Powers that provide special interactions that can't be priced."),
    "Utility - Warning": (7500, "Bound Being can't be surprised, and is awoken if foes are Near."),
}

items = []

# Core never leaves a Power on its bare category label - Dyrnwyn calls its Bane "Evil's Bane",
# Skyhowel calls its Utility "Crack the Sky", Sunder calls its Bane "Giants Bane". Catch-all
# categories (Unique / Blasting / Store Spell / Bane - General) therefore get an item-specific
# name here, keyed by (item, power).
LABELS = {
    ("Alchemy Jug", "Utility - Infinite"): "Endless Draught",
    ("Amulet of Health", "Utility - Unique"): "Vigour",
    ("Bag of Beans", "Utility - Unique"): "Sprouting",
    ("Bag of Tricks (Gray)", "Utility - Unique"): "Menagerie",
    ("Boots of the Winterlands", "Utility - Unique"): "Snowstrider",
    ("Chime of Opening", "Utility - Unique"): "Opening",
    ("Crystal Ball", "Utility - Unique"): "Scrying",
    ("Elemental Gem (Yellow Diamond)", "Utility - Unique"): "Summon Elemental",
    ("Energy Cell", "Utility - Unique"): "Charge Store",
    ("Eyes of Minute Seeing", "Utility - Unique"): "Minute Seeing",
    ("Figurine of Wondrous Power (Silver Raven)", "Utility - Unique"): "Silver Raven",
    ("Hat of Disguise", "Utility - Unique"): "Disguise",
    ("Horn of Blasting", "Fabled - Blasting"): "Thunderblast",
    ("Laser Pistol", "Utility - Unique"): "Energy Bolt",
    ("Laser Rifle", "Utility - Unique"): "Energy Lance",
    ("Mithral Armor", "Utility - Unique"): "Featherweight",
    ("Necklace of Fireballs", "Utility - Unique"): "Fireball Beads",
    ("Orc Stone", "Utility - Unique"): "The Eyebiter's Shade",
    ("Pearl of Power", "Utility - Store Spell"): "Recall",
    ("Ring of the Ram", "Fabled - Blasting"): "Ram's Charge",
    ("Shield Guardian Amulet", "Utility - Unique"): "Guardian Bond",
    ("Sovereign Glue", "Utility - Unique"): "Sovereign Bond",
    ("Staff of Charming", "Utility - Unique"): "Charming",
    ("Staff of Frost", "Utility - Unique"): "Winter's Reach",
    ("Staff of Power", "Fabled - Blasting"): "Force Bolt",
    ("Staff of Power", "Utility - Unique"): "Retributive Strike",
    ("Wand of Binding", "Utility - Unique"): "Binding",
    ("Wand of Magic Missiles", "Fabled - Blasting"): "Magic Missile",
    ("Wand of Orcus", "Bane - General"): "Bane of the Living",
    ("Wand of Web", "Utility - Unique"): "Webbing",
}


def relic(name, kind, flavour, powers, *, bound=False, consumable=False, fabled=False,
          slots=1, gold=None, weapon=None, armor=None, metal="none", extra_html=""):
    """powers: list of (PowerName, override_text or None) -- name must exist in POWERS."""
    total = 0
    lis = []
    for entry in powers:
        pname, override = entry if isinstance(entry, tuple) else (entry, None)
        cost, default = POWERS[pname]
        total += cost
        label = LABELS.get((name, pname)) or (pname.split(" - ", 1)[1] if " - " in pname else pname)
        # Core writes flat bonuses as "(+2) Weapon:", not "Weapon +2:" (see Dyrnwyn).
        m = re.match(r"^(\w+) ([+-]\d)$", label)
        if m:
            label = f"({m.group(2)}) {m.group(1)}"
        lis.append(f"<li><strong>{label}:</strong> {override or default}</li>")
    cost_gold = total if gold is None else gold

    lore = ("Fabled " if fabled else "") + "Relic " + kind
    if bound:
        lore += " (Bound)"
    if consumable:
        lore += " (Consumable)"

    desc = f"<p>{flavour} It has the following Powers:</p><ul>{''.join(lis)}</ul>{extra_html}"

    sys = {
        "description": desc,
        "equipmentType": "relic",
        "locked": False,
        "equipped": False,
        "quantity": 1,
        "baseCost": {"gold": cost_gold, "silver": 0, "copper": 0},
        "baseSlots": slots,
        "metal": metal,
        "damageType": "-",
        "damageAmount": "",
        "properties": [],
        "weaponSkill": (weapon or {}).get("skill", "melee"),
        "range": (weapon or {}).get("range", "close"),
        "grip": (weapon or {}).get("grip", "1H"),
        "damageOneHand": (weapon or {}).get("d1", "d6"),
        "damageTwoHands": (weapon or {}).get("d2", "d8"),
        "damageTypeOneHand": (weapon or {}).get("type", "-"),
        "damageTypeTwoHands": (weapon or {}).get("type", "-"),
        "equipmentState": "unequipped",
        "armorType": armor or "light",
        "immunities": [],
        "gearCategory": "",
        "alchemicalType": "",
        "lore": lore,
        "requiresBound": bound,
        "bound": False,
        "gridPosition": 0,
        "containerId": None,
        "canExplode": False,
        "explodeValues": "",
        "isSupply": False,
        "isBeverage": False,
        "isConsumable": consumable,
        "linkedConsumable": "",
        "passiveCausedStatuses": [],
        "causedStatuses": [],
        "critCausedStatuses": [],
        "blockedStatuses": [],
        "resistedStatuses": [],
        "coating": {"sourceName": "", "charges": 0, "causedStatuses": []},
        "itemFx": {"enabled": False, "animType": "auto", "hitFile": "", "hitScale": 1,
                   "hitOffsetX": 0, "hitDuration": 800, "hitSound": "", "missFile": "",
                   "missScale": 1, "missDuration": 600, "missSound": "", "soundVolume": 0.6},
    }
    items.append({"name": name, "type": "equipment",
                  "img": "icons/magic/symbols/circled-gem-pink.webp", "system": sys})


def potion(name, flavour, effect, gold=0, silver=0):
    """Potions follow the alchemical convention, not the relic one."""
    sys = {
        "description": f"<p>{flavour}</p><p>{effect}</p>",
        "equipmentType": "alchemical",
        "alchemicalType": "potion",
        "locked": False, "equipped": False, "quantity": 1,
        "baseCost": {"gold": gold, "silver": silver, "copper": 0},
        "baseSlots": 1, "metal": "none", "damageType": "-", "damageAmount": "",
        "properties": [], "weaponSkill": "melee", "range": "close", "grip": "1H",
        "damageOneHand": "d6", "damageTwoHands": "d8",
        "damageTypeOneHand": "-", "damageTypeTwoHands": "-",
        "equipmentState": "unequipped", "armorType": "light", "immunities": [],
        "gearCategory": "", "lore": "", "requiresBound": False, "bound": False,
        "gridPosition": 0, "containerId": None, "canExplode": False, "explodeValues": "",
        "isSupply": False, "isBeverage": True, "isConsumable": False, "linkedConsumable": "",
        "passiveCausedStatuses": [], "causedStatuses": [], "critCausedStatuses": [],
        "blockedStatuses": [], "resistedStatuses": [],
        "coating": {"sourceName": "", "charges": 0, "causedStatuses": []},
        "itemFx": {"enabled": False, "animType": "auto", "hitFile": "", "hitScale": 1,
                   "hitOffsetX": 0, "hitDuration": 800, "hitSound": "", "missFile": "",
                   "missScale": 1, "missDuration": 600, "missSound": "", "soundVolume": 0.6},
    }
    items.append({"name": name, "type": "equipment",
                  "img": "icons/consumables/potions/bottle-round-corked-pink.webp", "system": sys})


def scroll(name, spell, flavour):
    LABELS[(name, "Utility - Store Spell")] = "Inscribed Casting"
    relic(name, "Scroll", flavour,
          [("Utility - Store Spell", f"Holds a single Casting of <em>{spell}</em>, at the Rank it "
                                     "was scribed. Reading it aloud Casts the Spell without spending "
                                     "Mana and consumes the scroll.")],
          consumable=True, gold=100)


def container(name, flavour, capacity, gold, slots=1):
    items.append({
        "name": name, "type": "container",
        "img": "icons/containers/bags/sack-leather-brown.webp",
        "system": {
            "description": f"<p>{flavour}</p><ul><li><strong>Holding {capacity}:</strong> "
                           f"Occupies {slots} Inventory Slot, but can hold {capacity} Slots of "
                           "Items without counting against the carrier's Inventory Slots.</li></ul>",
            "slots": slots, "capacity": capacity, "gridPosition": 0,
            "items": [], "baseCost": {"gold": gold, "silver": 0, "copper": 0}, "locked": False,
        },
    })


# ===========================================================================
# WANDS, STAFFS & RODS
# ===========================================================================
relic("Wand of the War Mage +1", "Wand",
      "A slender rod of blackened ash, warm to the touch when a spell is on the wielder's lips.",
      [("Bonus - Trinket +1", "Deals an extra +1 Spell damage, and the wielder ignores half-Cover "
                              "when Casting.")], bound=True)

relic("Wand of Binding", "Wand",
      "Taken from the warden's quarters at Revel's End, where it was used far more often than the paperwork admits.",
      [("Utility - Unique", "Holds 3 charges, all of which return after a Rest. Expend a charge to Restrain "
                            "a Being you can see within Near ([Might] negates, repeatable at the end "
                            "of each of its Turns), or to immediately end a Restrained or Grappling "
                            "Status on yourself."),
       ("Ace - Entangle", "A Being Restrained by the wand is Vulnerable for as long as it stays "
                          "Restrained.")], bound=True, gold=5000)

relic("Wand of Magic Missiles", "Wand",
      "Vellynne Harpell keeps one on her belt and reaches for it more readily than she admits.",
      [("Fabled - Blasting", "Holds 3 charges, all of which return after a Rest. Expend a charge to send "
                             "three darts of force at Beings you can see within Far, dealing 1d4+1 "
                             "damage each. The darts never miss. Spend up to 3 further charges to "
                             "send one extra dart each.")])

relic("Wand of Orcus", "Wand",
      "A skull-topped rod of the Demon Prince of Undeath. The one in the White Wyrm's hoard is a "
      "replica - though nothing about holding it feels like a replica.",
      [("Bonus - Weapon +3", "Deals an extra +3 damage."),
       "Fabled - Soul Eater", "Fabled - Vicious",
       ("Bane - General", "Deals an extra damage die to the living; Undead who see it must pass "
                          "[Will] or serve the wielder."),
       ("Cursed - Doom", "The wielder only regains 1 HP per die rolled to heal them, and Undead "
                         "everywhere become aware of where the wand is.")],
      bound=True, fabled=True,
      weapon={"skill": "melee", "d1": "d8", "d2": "d10", "type": "necrotic"})

relic("Wand of Web", "Wand",
      "Duergar looted it from a drow caravan and never worked out how to stop it sticking to things.",
      [("Utility - Unique", "Holds 3 charges, all of which return after a Rest. Expend a charge to fill a "
                            "Near Cube with thick webbing: it is Difficult Terrain, and a Being that "
                            "enters it or starts its Turn in it must pass [Reflex] or be Restrained."),
       ("Ace - Entangle", "A Being Restrained by the webs is Vulnerable until it breaks free.")],
      bound=True, gold=2500)

relic("Staff of Charming", "Staff",
      "Recovered from Drakareth's Doom, still faintly warm from whatever the wraith was doing with it.",
      [("Utility - Unique", "Holds 5 charges, all of which return after a Rest. Expend a charge to Cast "
                            "<em>Charm</em>. As a Reaction to an enchantment Spell targeting you, "
                            "absorb it instead and regain a charge."),
       ("Resistance - Repulsing", "The wielder has Favor on Saves against the Charmed Status.")],
      bound=True, gold=5000)

relic("Staff of Frost", "Staff",
      "Avarice keeps it close, and the cold that clings to it is noticeably worse than the weather outside.",
      [("Bonus - Trinket +2", "Deals an extra +2 damage with Cold Spells."),
       ("Resistance - Resistance", "Favor on Saves and damage reduction against Cold."),
       ("Utility - Unique", "Holds 5 charges, all of which return after a Rest. Expend a charge to Cast "
                            "<em>Freeze</em> or <em>Frostburn</em>. If it is broken while empty, it melts into water." "")],
      bound=True, gold=15000)

relic("Staff of Power", "Staff",
      "One of Iriolarthas's own, and still the single most dangerous thing a character can pick up in Ythryn.",
      [("Bonus - Trinket +2", "Deals an extra +2 Spell damage."),
       ("Bonus - Armor +2", "+2 bonus to Armor while the staff is held."),
       ("Bonus - Protection +2", "+2 bonus to Saves while the staff is held."),
       ("Fabled - Blasting", "Expend a charge to strike a Being within Far with a bolt of force for "
                             "5d6 damage, or swing the staff in melee for an extra 1d6."),
       ("Utility - Unique", "Holds 5 charges, all of which return after a Rest. Break the staff to release "
                            "its remaining power in a Far Sphere for 16d6 damage, halved by "
                            "distance. The wielder is destroyed.")],
      bound=True, fabled=True, gold=25000)

# ===========================================================================
# RINGS
# ===========================================================================
relic("Ring of the Ram", "Ring",
      "A band of bronze cast as a curled ram's head, found in the wreck of a Netherese skycoach.",
      [("Fabled - Blasting", "Holds 3 charges, all of which return after a Rest. Expend a charge to strike a Being within Far with a spectral ram: "
                             "2d10 damage and shoved 15 feet.")], bound=True)

relic("Ring of Warmth", "Ring",
      "Worth more than gold on the Eastside of Termalaine, and everybody there knows it.",
      [("Resistance - Resistance", "Favor on Saves and damage reduction against Cold. The wearer is "
                                   "unharmed by Blistering Cold.")], bound=True)

# ===========================================================================
# WEAPONS & ARMOR
# ===========================================================================
relic("Trident +2", "Trident",
      "Pried out of a shipwreck frozen into the ice off Solstice.",
      [("Bonus - Weapon +2", "Deals an extra +2 damage.")],
      weapon={"skill": "melee", "d1": "d6", "d2": "d8", "type": "piercing"})

relic("Berserker Axe", "Battleaxe",
      "Vassavicken's axe. It wants to be swung, and it is not especially concerned at what.",
      [("Bonus - Weapon +2", "Deals an extra +2 damage."),
       ("Bonus - Armor +1", "+1 bonus to Armor while the axe is carried."),
       ("Cursed - Anger", "The wielder always fails Saves against Berserk. While Berserk they must "
                          "Attack the nearest Being each Turn, and cannot willingly part with the axe.")],
      bound=True, weapon={"skill": "melee", "d1": "d8", "d2": "d10", "type": "slashing"})

relic("Mithral Armor", "Chain",
      "Dwarven-made and light as cloth, it never announces the wearer the way steel does.",
      [("Utility - Unique", "Counts as Chain armor, but never imposes Hinder on Checks to move "
                            "quietly and has no Might requirement.")],
      # NB: this system spells the metal "mythral" (CONFIG.VAGABOND.metalTypes).
      # "mithral" fails validation silently - the item just never gets created.
      gold=1000, armor="medium", metal="mythral")

# ===========================================================================
# WONDROUS ITEMS
# ===========================================================================
relic("Alchemy Jug", "Jug",
      "A ceramic jug that produces whatever it feels like producing, within reason.",
      [("Utility - Infinite", "Once per Rest, name a liquid - water, ale, oil, honey, vinegar, wine, "
                              "or mayonnaise - and the jug fills with it.")])

relic("Amulet of Health", "Amulet",
      "Found in the Black Cabin, where Macreadus apparently valued it less than his machine.",
      [("Utility - Unique", "The wearer's Might score becomes 19 if it isn't already higher.")],
      bound=True, gold=10000)

relic("Bag of Beans", "Bag",
      "Perfectly ordinary beans. That is the problem.",
      [("Utility - Unique", "Plant a bean and something happens - a treant, a geyser, a rain of "
                            "toads, or a small, extremely angry monster. Roll on the DM's table.")],
      consumable=True, gold=2000)

relic("Bag of Tricks (Gray)", "Bag",
      "Confiscated from Dzaan by the Easthaven militia and never entered into evidence.",
      [("Utility - Unique", "Reach in and pull out a fuzzy object, which becomes a random Beast that "
                            "obeys you. Three uses, which return after a Rest.")], gold=3000)

relic("Boots of the Winterlands", "Boots",
      "Hilda's thanks for bringing her children home.",
      [("Resistance - Resistance", "Favor on Saves and damage reduction against Cold; the wearer is "
                                   "unharmed by Blistering Cold."),
       ("Utility - Unique", "Ice and deep snow are never Difficult Terrain for the wearer.")],
      bound=True)

relic("Chime of Opening", "Chime",
      "A hollow mithral tube that Netherese librarians used instead of keys.",
      [("Utility - Unique", "Strike the chime to Cast <em>Knock</em> on one object within Near. "
                            "Three uses, after which the chime cracks and is spent.")], gold=2500)

relic("Cloak of Elvenkind", "Cloak",
      "The wearer is easy to overlook, and the cloak's colour never quite settles.",
      [("Utility - Invisibility I", "While the hood is up, skip your Move to become Invisible until "
                                    "after you take an Action. Beings have Hinder on Checks to notice "
                                    "you even after that.")], bound=True)

relic("Piwafwi", "Cloak",
      "The drow cut of the same enchantment, black as the Underdark and twice as smug about it.",
      [("Utility - Invisibility I", "While the hood is up, skip your Move to become Invisible until "
                                    "after you take an Action. Beings have Hinder on Checks to notice "
                                    "you even after that.")], bound=True)

relic("Cloak of Protection", "Cloak",
      "Wyrmdoom Crag's goliaths have kept this one in the main hall for generations.",
      [("Bonus - Armor +1", "+1 bonus to Armor while worn."),
       ("Bonus - Protection +1", "+1 bonus to all Saves while worn.")], bound=True)

relic("Crystal Ball", "Orb",
      "Nass Lantomir wanted one badly enough to die over it.",
      [("Utility - Unique", "Gaze into it to Scry on a Being or place you name, seeing and hearing "
                            "it as though standing there. An unwilling Being resists with [Will], and "
                            "knows it is being watched on a pass."),
       ("Senses - True-Seeing", "While Scrying, the viewer sees through illusions, invisibility and "
                                "disguises within the scried area.")],
      bound=True, gold=50000)

relic("Driftglobe", "Globe",
      "A glass sphere the size of a fist that follows its owner around like a patient dog.",
      [("Utility - Radiant I", "Speak the command word to make it shed sunlight out to Close, and "
                               "again to douse it."),
       ("Movement - Levitation", "The globe itself hovers, and follows within Close of whoever spoke "
                                 "the command word. It can be sent up to Far away and recalled.")])

relic("Elemental Gem (Yellow Diamond)", "Gem",
      "A flawed yellow diamond with something restless behind the facets.",
      [("Utility - Unique", "Shatter it to summon a friendly Earth Elemental for 1 Hour.")],
      consumable=True, gold=5000)

relic("Eyes of Minute Seeing", "Lenses",
      "Netherese reading glasses, found in the captains' quarters of the Id Ascendant.",
      [("Utility - Unique", "The wearer has Favor on Checks to examine anything within 1 foot.")],
      gold=500)

relic("Figurine of Wondrous Power (Silver Raven)", "Figurine",
      "A goliath peace offering, and a rather good messenger.",
      [("Utility - Unique", "Becomes a living silver raven for up to 12 Hours, then reverts and can't be used again until after a Rest." " It can carry a message.")], gold=5000)

relic("Hat of Disguise", "Hat",
      "Pekoe Quint's, and it explains a great deal about Pekoe Quint.",
      [("Utility - Unique", "Cast <em>Mirage</em> on yourself at will to change your appearance. "
                            "The illusion ends if the hat leaves your head.")], bound=True, gold=5000)

relic("Horn of Blasting", "Horn",
      "Blowing it is always louder than anyone expects, including the person blowing it.",
      [("Fabled - Blasting", "Blow the horn to deal 5d6 damage in a Far Cone; those who fail "
                             "[Endure] are also Dazed. On a roll of 1-4 on a d100, the horn explodes "
                             "and is destroyed, dealing 10d6 to the user.")])

relic("Mantle of Spell Resistance", "Cloak",
      "Drakareth wore it, and it is a large part of why Drakareth was a problem.",
      [("Bonus - Protection +2", "+2 bonus to Saves against Spells and other magical effects."),
       ("Resistance - Resistance", "Favor on Saves and damage reduction against magical damage.")],
      bound=True)

relic("Necklace of Fireballs", "Necklace",
      "Five beads on a chain, each one a small argument waiting to happen.",
      [("Utility - Unique", "Detach a bead and throw it up to Far: it detonates for 3d6 Fire damage "
                            "in a Near Sphere ([Reflex] to reduce). Multiple beads can be thrown at "
                            "once, adding 1d6 each.")], consumable=True, gold=4000)

relic("Orc Stone", "Stone",
      "A fist-sized rock carved with an orcish eye, which watches back.",
      [("Utility - Unique", "Once per Rest, summon the spirit of Vokarr the Eyebiter for 1 Hour. It "
                            "answers questions about war and about orcs, and lies about everything else.")],
      bound=True, gold=2500)

relic("Pearl of Power", "Pearl",
      "Sealed in an ancient tomb beneath Good Mead, alongside somebody who clearly wanted it kept there.",
      [("Utility - Store Spell", "Once per Rest, regain Mana equal to a Spell you have already Cast.")],
      bound=True, gold=5000)

relic("Shield Guardian Amulet", "Amulet",
      "Somewhere out in the ice, a construct is still waiting for whoever wears this.",
      [("Utility - Unique", "The bonded Shield Guardian obeys your spoken commands, tries to stay "
                            "within Far of you, and takes half of any damage dealt to you while it "
                            "is within Close."),
       ("Senses - Telepathy", "Telepathy (Far) with the bonded Shield Guardian only, which does not "
                              "require Focus.")], bound=True, gold=10000)

relic("Sovereign Glue", "Vial",
      "One ounce. There is no second ounce, and no known solvent short of Alkahest.",
      [("Utility - Unique", "Permanently bonds two objects. Only Alkahest will separate them.")],
      consumable=True, fabled=True, gold=10000)

relic("Stone of Good Luck", "Stone",
      "A polished agate from the Chain Lightning Stadium, warm in the pocket.",
      [("Bonus - Protection +1", "+1 bonus to Saves and to all Checks.")], bound=True)

# --- containers ------------------------------------------------------------
container("Quiver of Ehlonna", "A three-compartment quiver, each compartment far deeper than the "
          "outside of it suggests.", 3, 1000)

# ===========================================================================
# FUTURISTIC TECH (crashed nautiloid Id Ascendant)
# ===========================================================================
relic("Laser Pistol", "Pistol",
      "Salvage from the Id Ascendant. Nobody in Icewind Dale has the faintest idea what it is.",
      [("Utility - Unique", "Requires a charged Energy Cell. Firing expends 1 of the cell's 5 charges, and no one in the Dale can refill it.")],
      gold=2000, weapon={"skill": "ranged", "range": "far", "d1": "d8", "d2": "d8", "type": "magical"})

relic("Laser Rifle", "Rifle",
      "Two-handed, absurdly precise, and utterly unrepairable this side of the stars.",
      [("Utility - Unique", "Requires a charged Energy Cell. Firing expends 1 of the cell's 5 charges.")],
      gold=3000, weapon={"skill": "ranged", "range": "far", "d1": "d10", "d2": "d10", "type": "magical"})

relic("Energy Cell", "Cell",
      "A flat crystalline wafer holding a charge that no Faerunian magic can replenish.",
      [("Utility - Unique", "Holds 5 charges. Nothing in Faerun can refill it - once spent, it is inert forever.")],
      consumable=True, gold=100, slots=0)

# ===========================================================================
# SPELL SCROLLS  (D&D spell -> nearest Vagabond spell)
# ===========================================================================
for nm, sp, fl in [
    ("Scroll of Beast", "Beast", "Tali's thanks for dealing with the thing in the lake."),
    ("Scroll of Guide", "Guide", "How Nass Lantomir knew what she knew."),
    ("Scroll of Erupt", "Erupt", "Confiscated from Dzaan, and offered back as a reward."),
    ("Scroll of Fade", "Fade", "Sealed in a chardalyn tube in the upside-down laboratory."),
    ("Scroll of Knock", "Knock", "Dropped down a waste chute, and none the worse for it."),
    ("Scroll of Cure", "Cure", "From an Icewind kobold shaman's tent."),
    ("Scroll of Mass Cure", "Cure", "Found on the crowned rooftop of Grimskalle."),
    ("Scroll of Portal", "Portal", "Scrivenscry's way into Ythryn, and possibly yours out."),
    ("Scroll of Dispel", "Dispel", "Bundled with an archer figurine in the Dark Duchess's hold."),
]:
    scroll(nm, sp, fl)

# ===========================================================================
# POTIONS  (alchemical convention)
# ===========================================================================
potion("Potion of Water Breathing",
       "A cloudy green potion with a single seaweed frond drifting in it.",
       "For 1 Hour, the consumer can breathe underwater. It does not grant a Swim speed.", gold=25)

potion("Potion of Resistance",
       "The liquid shifts colour depending on which element it was brewed against.",
       "For 1 Hour, the consumer gains Favor on Saves and damage reduction against one damage type, "
       "chosen when the potion is brewed.", gold=25)

potion("Potion of Warding",
       "Vagabond has no Radiant damage type, so Rime's <em>potion of radiant resistance</em> is "
       "brewed here as a warding draught against magical damage.",
       "For 1 Hour, the consumer gains Favor on Saves and damage reduction against magical damage.",
       gold=25)

potion("Potion of Vitality",
       "A clear red liquid that pulses gently, like something with a heartbeat.",
       "The consumer's Fatigue is removed, and they regain the full benefit of a Rest. For the next "
       "24 Hours they regain the maximum result on any healing die rolled for them.", gold=250)

potion("Potion of Longevity",
       "Amber, with a swirl of gold that never settles.",
       "The consumer's physical age is reduced by 1d6 + 6 years, to a minimum of 13. Each potion "
       "after the first carries a cumulative 10% chance of ageing them by the same amount instead.",
       gold=500)


if __name__ == "__main__":
    out = r"D:\claude projects\Icewind Dale Vagabond\items\new_items.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"{'name':40s} {'type':10s} {'gold':>8s}  lore")
    print("-" * 100)
    for i in items:
        s = i["system"]
        g = s["baseCost"]["gold"] + s["baseCost"].get("silver", 0) / 10
        print(f"{i['name']:40s} {i['type']:10s} {g:>8.0f}  {s.get('lore','(container)')}")
    print(f"\n{len(items)} items -> {out}")
