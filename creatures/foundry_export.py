# -*- coding: utf-8 -*-
import json, math, re, sys
sys.path.insert(0, ".")
from build_bestiary import creatures  # reuse the exact same source data
from build_bestiary_2 import creatures2  # batch 6 - full-adventure audit pass
from tl_calc import calc_tl

# Token grid footprint per size, matching the core compendium's own convention
# (confirmed against vagabond.bestiary: small/medium 1x1, large 2x2, huge 3x3,
# giant 4x4, colossal 5x5). Foundry does NOT derive this from system.size, so a
# creature omitting it silently renders as a 1x1 Medium regardless of its stat block.
TOKEN_SCALE = {"small": 1, "medium": 1, "large": 2, "huge": 3, "giant": 4, "colossal": 5}

BEING_TYPE_MAP = {
    "Artificial": "Artificials", "Beast": "Beasts", "Cryptid": "Cryptid",
    "Fae": "Fae", "Humanlike": "Humanlike", "Outer": "Outers",
    "Primordial": "Primordials", "Undead": "Undead",
}

# Foundry's live CONFIG.VAGABOND.damageTypes keys (confirmed against the running world, v5.4.1)
VALID_DMG_KEYS = {"-", "acid", "fire", "shock", "poison", "cold", "blunt", "piercing",
                   "slashing", "physical", "necrotic", "psychic", "magical", "healing",
                   "recover", "recharge"}

# Only elemental/exotic attacks get a typed damageType (matches official convention: Freeze->cold,
# Zap->shock in the Flying Spellbook precedent). Plain physical weapon hits stay "-" even for
# claws/bites/flails/greataxes - confirmed by Troll, Ancient White Dragon, and Archmage precedent.
DMG_TYPE_OVERRIDES = {
    ("Grandolpha Muzgardt", "Poison Spray"): "poison",
    ("Auril, the Frostmaiden (First Form)", "Talons"): "cold",
    ("Auril, the Frostmaiden (First Form)", "Touch of Frost"): "cold",
    ("Auril, the Frostmaiden (First Form)", "Frost Orb"): "cold",
    ("Auril, the Frostmaiden (Second Form)", "Ice Morningstar"): "cold",
    ("Auril, the Frostmaiden (Second Form)", "Cone of Cold"): "cold",
    ("Auril, the Frostmaiden (Third Form)", "Polar Ray"): "cold",
    ("Arveiaturace", "Glacial Breath"): "cold",
    ("Abominable Yeti", "Claw"): "cold",
    ("Abominable Yeti", "Cold Breath"): "cold",
    ("Winter Wolf", "Frost Breath"): "cold",
    ("Snow Golem", "Slam"): "cold",
    ("Snow Golem", "Snowball"): "cold",
    ("Coldlight Walker", "Slam"): "cold",
    ("Coldlight Walker", "Cold Ray"): "cold",
    ("Avarice", "Fire Bolt"): "fire",
    ("Avarice", "Cone of Cold"): "cold",
    ("Avarice", "Banishing Rebuke"): "cold",
    ("Dzaan's Simulacrum", "Shocking Grasp"): "shock",
    ("Dzaan's Simulacrum", "Acid Splash"): "acid",
    ("Dzaan's Simulacrum", "Magic Missile"): "magical",
    ("Duergar Mind Master", "Mind-Poison Dagger"): "psychic",
    ("Kobold Vampire Spawn", "Bite"): "necrotic",
    ("Frost Giant Skeleton", "Freezing Stare"): "cold",
    ("Galvan Magen", "Shocking Touch"): "shock",
    ("Galvan Magen", "Static Discharge"): "shock",
    ("Hypnos Magen", "Psychic Lash"): "psychic",
    ("Gnoll Vampire", "Bite"): "necrotic",
    ("Nass Lantomir's Ghost", "Withering Touch"): "necrotic",
    ("Yeti Tyke", "Claw"): "cold",
    ("Mind Flayer", "Tentacles"): "psychic",
    ("Mind Flayer", "Mind Blast"): "psychic",
    ("Myconid Sovereign", "Fist"): "poison",
    ("Barbed Devil", "Hurl Flame"): "fire",
    ("Ice Mephit", "Claws"): "cold",
    ("Ice Mephit", "Frost Breath"): "cold",
    ("Reghed Shaman", "Produce Flame"): "fire",
    # --- batch 6 ---
    ("Priest", "Sacred Flame"): "magical",
    ("Priest", "Cure Wounds"): "healing",
    ("Frost Druid", "Ice Sickle"): "cold",
    ("Drow Mage", "Lightning Bolt"): "shock",
    ("Drow Mage", "Darkfire Bolt"): "necrotic",
    ("Drow Mage", "Cloudkill"): "poison",
    ("Spellix Romwod", "Fire Bolt"): "fire",
    ("Spellix Romwod", "Shocking Grasp"): "shock",
    ("Sephek Kaltro", "Ice Longsword"): "cold",
    ("Sephek Kaltro", "Ice Dagger"): "cold",
    ("Quaggoth Thonot", "Mind Blast"): "psychic",
    ("Specter", "Life Drain"): "necrotic",
    ("Poltergeist", "Forceful Slam"): "magical",
    ("Poltergeist", "Telekinetic Thrust"): "magical",
    ("Flameskull", "Fire Ray"): "fire",
    ("Brain in a Jar", "Chill Touch"): "necrotic",
    ("Brain in a Jar", "Mind Blast"): "psychic",
    ("Demilich", "Life Drain"): "necrotic",
    ("Shadow Demon", "Claws"): "psychic",
    ("Arcanaloth", "Chain Lightning"): "shock",
    ("Arcanaloth", "Fire Bolt"): "fire",
    ("Green Slaad", "Hurl Flame"): "fire",
    ("Nothic", "Rotting Gaze"): "necrotic",
    ("Gnome Ceremorph", "Tentacles"): "psychic",
    ("Gnome Ceremorph", "Mind Blast"): "psychic",
    ("Gnome Ceremorph", "Laser Pistol"): "magical",
    ("Gnome Squidling", "Tentacles"): "psychic",
    ("Gnome Squidling", "Mind Tickle"): "psychic",
    ("Phase Spider", "Bite"): "poison",
    ("Spitting Mimic", "Spit Acid"): "acid",
    ("Ice Piercer", "Drop"): "cold",
    ("Living Bigby's Hand", "Force Fist"): "magical",
    ("Living Blade of Disaster", "Force Blade"): "magical",
    ("Flying Snake", "Bite"): "poison",
    ("Chimeric Baboon", "Bite"): "poison",
    ("Dragon, Hatchling - Silver", "Cold Breath"): "cold",
}
# Frigid Aura / Frost Nova / Cold Aura are in abilities[], not actions[] - handled separately below.

ATTACK_TYPE_OVERRIDES = {
    ("Xardorok Sunblight", "Void Bolt"): "castRanged",
    ("Chardalyn Dragon", "Chardalyn Breath"): "castRanged",
    ("Arveiaturace", "Glacial Breath"): "castRanged",
    ("Grandolpha Muzgardt", "Poison Spray"): "castClose",
    ("Auril, the Frostmaiden (First Form)", "Touch of Frost"): "castClose",
    ("Auril, the Frostmaiden (First Form)", "Frost Orb"): "castRanged",
    ("Auril, the Frostmaiden (Second Form)", "Cone of Cold"): "castRanged",
    ("Auril, the Frostmaiden (Third Form)", "Polar Ray"): "castRanged",
    ("Vellynne Harpell", "Chill Touch"): "castRanged",
    ("Vellynne Harpell", "Wand of Magic Missiles"): "castRanged",
    ("Yeti", "Terror Glare"): "castRanged",
    ("Avarice", "Fire Bolt"): "castRanged",
    ("Avarice", "Cone of Cold"): "castRanged",
    ("Dzaan's Simulacrum", "Acid Splash"): "castRanged",
    ("Dzaan's Simulacrum", "Magic Missile"): "castRanged",
    ("Galvan Magen", "Static Discharge"): "castRanged",
    ("Hypnos Magen", "Psychic Lash"): "castRanged",
    ("Hypnos Magen", "Suggestion"): "castRanged",
    ("Mind Flayer", "Mind Blast"): "castRanged",
    ("Barbed Devil", "Hurl Flame"): "castRanged",
    ("Reghed Shaman", "Produce Flame"): "castRanged",
    ("Reghed Shaman", "Entangle"): "castRanged",
    # --- batch 6 ---
    ("Priest", "Sacred Flame"): "castRanged",
    ("Priest", "Cure Wounds"): "castClose",
    ("Cult Fanatic", "Command"): "castRanged",
    ("Druid", "Entangle"): "castRanged",
    ("Drow Mage", "Lightning Bolt"): "castRanged",
    ("Drow Mage", "Darkfire Bolt"): "castRanged",
    ("Drow Mage", "Cloudkill"): "castRanged",
    ("Spellix Romwod", "Fire Bolt"): "castRanged",
    ("Spellix Romwod", "Shocking Grasp"): "castClose",
    ("Orc Eye of Gruumsh", "Bless"): "castClose",
    ("Quaggoth Thonot", "Mind Blast"): "castClose",
    ("Poltergeist", "Telekinetic Thrust"): "castRanged",
    ("Flameskull", "Fire Ray"): "castRanged",
    ("Brain in a Jar", "Chill Touch"): "castRanged",
    ("Brain in a Jar", "Mind Blast"): "castRanged",
    ("Demilich", "Life Drain"): "castClose",
    ("Demilich", "Howl"): "castClose",
    ("Demilich", "Vile Curse"): "castRanged",
    ("Arcanaloth", "Chain Lightning"): "castRanged",
    ("Arcanaloth", "Fire Bolt"): "castRanged",
    ("Green Slaad", "Hurl Flame"): "castRanged",
    ("Nothic", "Rotting Gaze"): "castRanged",
    ("Gnome Ceremorph", "Mind Blast"): "castRanged",
    ("Gnome Squidling", "Mind Tickle"): "castClose",
    ("Spitting Mimic", "Spit Acid"): "castRanged",
    ("Living Demiplane", "Extradimensional Chamber"): "castClose",
    ("Dryad", "Fey Charm"): "castRanged",
    ("Dragon, Hatchling - Silver", "Cold Breath"): "castRanged",
    ("Dragon, Hatchling - Silver", "Paralyzing Breath"): "castRanged",
}

# Breath/AoE-style Cast actions that read as "Attack, <delivery> | <save> | Half damage on a pass"
# in the official note-field convention (see Dragon, Ancient - White's Breath Attack), rather than
# a plain "Cast, ..." note.
BREATH_STYLE = {
    ("Chardalyn Dragon", "Chardalyn Breath"),
    ("Arveiaturace", "Glacial Breath"),
    ("Auril, the Frostmaiden (Second Form)", "Cone of Cold"),
    ("Dragon, Hatchling - Silver", "Cold Breath"),
    ("Dragon, Hatchling - Silver", "Paralyzing Breath"),
}

# Immunity/weakness free-text -> valid lowercase keys (matching official compendium convention,
# e.g. Dragon Ancient uses "physical" for "Physical from non-Relics", Zombie Dragon uses "silver"
# for "Silvered Weapons")
IMM_WEAK_MAP = {
    "Poison": "poison", "Cold": "cold", "Fire": "fire", "Shock": "shock", "Acid": "acid",
    "Physical from non-Relics": "physical", "Silvered Weapons": "silver",
}


def dice_str(n, d, mod):
    if not d:
        return ""
    s = (str(n) if n and n > 1 else "") + "d" + str(d)
    if mod > 0:
        s += "+" + str(mod)
    elif mod < 0:
        s += str(mod)
    return s


def flat_str(n, d, mod):
    if not d:
        return ""
    return str(math.floor(n * (d + 1) / 2 + mod))


def map_imm_weak(vals):
    out = []
    for v in vals:
        out.append(IMM_WEAK_MAP.get(v, v.lower()))
    return out


def build_note(creature_name, a):
    """Mirrors the rulebook's bracket notation: 'Kind[, extra tag] | Save | Focus'
    (e.g. "Cast, 20-foot Sphere | Endure | Focus", "Melee Attack 10'", "Attack, Far Cone | Reflex").
    Does NOT notate save-reduction ("half damage on a pass") - Vagabond's universal Defending
    rules (a passed Save vs. an attack ignores its highest rolled damage die) already handle
    this, and the Foundry sheet has its own damage-reduction mechanics, so restating it on the
    action is redundant and shouldn't be included."""
    key = (creature_name, a["name"])
    kind = a["kind"]

    if key in BREATH_STYLE:
        head = "Attack"
    elif kind == "Melee Attack":
        head = "Melee Attack"
    elif kind == "Ranged Attack":
        head = "Ranged Attack"
    else:
        head = "Cast"

    tags = a.get("tags", "")
    if tags == "10' reach":
        head += " 10'"
        extra_tag = ""
    else:
        extra_tag = tags

    pipe_segs = []
    if a.get("save"):
        pipe_segs.append(a["save"])
    if a.get("focus"):
        pipe_segs.append("Focus")

    note = head
    if extra_tag:
        note += ", " + extra_tag
    if pipe_segs:
        note += " | " + " | ".join(pipe_segs)
    return note


def combo_extra_info(combo_name):
    # "Combo: 2x Claw and 1x Bite" -> "2xClaw and 1xBite"
    text = combo_name.split(":", 1)[1].strip() if ":" in combo_name else combo_name
    return text.replace(" x", "x").replace("x ", "x")


def blank_action():
    return {
        "weaponId": "", "weaponPrevName": "", "weaponPrevFlatDamage": "", "weaponPrevRollDamage": "",
        "causedStatuses": [], "critCausedStatuses": [],
        "macro": {"enabled": False, "uuid": "", "command": "", "label": "", "runAsGM": False},
        "hitMacro": {"enabled": False, "uuid": "", "command": "", "label": "", "runAsGM": False},
    }


def to_foundry_actor(c):
    tl = calc_tl(c)["tl"]
    being_type = BEING_TYPE_MAP.get(c["type"], "Humanlike")

    # Foundry's official compendium encodes movement as combined strings in speedTypes
    # (e.g. ["fly 80"]), leaving speedValues at its 0 defaults - matched here for consistency.
    speed_types = [f"{k.lower()} {v}" for k, v in c.get("spds", {}).items()]
    speed_values = {"climb": 0, "cling": 0, "fly": 0, "phase": 0, "swim": 0}

    armor_desc = "as "
    if c.get("armEnh"):
        armor_desc += f"({'+' if c['armEnh'] > 0 else ''}{c['armEnh']}) "
    armor_desc += c.get("armType", "Unarmored")
    if c.get("shield"):
        armor_desc += " and Shield"

    actions = []
    abilities = []
    for a in c.get("acts", []):
        kind = a["kind"]
        if kind == "Combo":
            actions.append({
                "name": "Combo", "note": "", "recharge": "", "rechargeCountdownId": None,
                "flatDamage": "", "rollDamage": "", "damageType": "-", "attackType": "melee",
                "extraInfo": combo_extra_info(a["name"]),
                **blank_action(),
            })
            continue

        if kind in ("Melee Attack", "Ranged Attack", "Cast"):
            key = (c["name"], a["name"])
            if key in ATTACK_TYPE_OVERRIDES:
                attack_type = ATTACK_TYPE_OVERRIDES[key]
            elif kind == "Melee Attack":
                attack_type = "melee"
            elif kind == "Ranged Attack":
                attack_type = "ranged"
            else:
                attack_type = "castClose"

            recharge = a.get("recharge", "")
            if not recharge and a.get("uses"):
                recharge = f"{a['uses']}/{a.get('per', 'Day')}"

            extra_info = a.get("text", "")
            if key in BREATH_STYLE:
                # Vagabond's universal Defending rules already reduce damage on a passed Save
                # (the highest rolled die is ignored) - don't restate "half damage on a pass" on
                # the action itself. Also strips the internal Creature-Forge authoring note
                # ("Bonus burst, not counted in steady DPR"), which isn't meant for live play text.
                extra_info = re.sub(r"^(cold damage,\s*)?half damage on a pass\.?\s*", "", extra_info, flags=re.I)
                extra_info = re.sub(r"\s*bonus burst, not counted in steady dpr\.?", "", extra_info, flags=re.I)
                extra_info = extra_info.strip()

            actions.append({
                "name": a["name"],
                "note": build_note(c["name"], a),
                "recharge": recharge,
                "rechargeCountdownId": None,
                "flatDamage": flat_str(a["n"], a["d"], a["mod"]),
                "rollDamage": dice_str(a["n"], a["d"], a["mod"]),
                "damageType": DMG_TYPE_OVERRIDES.get(key, "-"),
                "attackType": attack_type,
                "extraInfo": extra_info,
                **blank_action(),
            })
        else:  # Ability / Action / Use -> abilities[]
            desc = a.get("text", "")
            bits = []
            if a.get("recharge"):
                bits.append(f"(Recharge {a['recharge']})")
            if a.get("uses"):
                bits.append(f"({a['uses']}/{a.get('per', 'Day')})")
            if bits:
                desc = " ".join(bits) + " " + desc
            if a.get("dpr") and a.get("d"):
                desc = f"Deals {flat_str(a['n'], a['d'], a['mod'])} ({dice_str(a['n'], a['d'], a['mod'])}) damage. " + desc
            abilities.append({"name": a["name"], "description": desc.strip()})

    # --- HP/HD: Foundry has no "boss" HP-doubling field (unlike Creature Forge / the printed
    # rulebook's "double a boss's HP" guidance). health.max is derived from hd (hd*4.5, floored)
    # by the system itself, so a boss creature's *effective* hd is doubled here to reach the
    # intended HP through the system's own derivation, rather than setting health.max directly
    # (which the sheet was silently overriding, causing "current HP exceeds max").
    effective_hd = c["hd"] * (2 if c.get("boss") else 1)
    per_hp = 1 if c["size"] == "Small" else 4.5
    hp = math.floor(effective_hd * per_hp)

    size_key = c["size"].lower()
    grid = TOKEN_SCALE[size_key]  # KeyError here is intentional: an unmapped size is a bug

    return {
        "name": c["name"],
        "type": "npc",
        "prototypeToken": {
            "name": c["name"],
            "width": grid,
            "height": grid,
        },
        "system": {
            "threatLevel": tl,
            "size": c["size"].lower(),
            "beingType": being_type,
            "speedTypes": speed_types,
            "hd": effective_hd,
            "morale": int(c["morale"]) if str(c.get("morale", "")).strip().isdigit() else None,
            "appearing": str(c.get("app", "")),
            "speed": c["speed"],
            "speedValues": speed_values,
            "senses": ", ".join(c.get("senses", [])),
            "armor": c["armor"],
            "armorDescription": armor_desc,
            "locked": False,
            "immunities": map_imm_weak(c.get("imm", [])),
            "weaknesses": map_imm_weak(c.get("weak", [])),
            "statusImmunities": [s.lower() for s in c.get("statusImm", [])],
            "zone": c["zone"].lower() if c.get("zone") else None,
            "description": c.get("flav", ""),
            "actions": actions,
            "abilities": abilities,
            "health": {"value": hp, "max": hp, "bonus": []},
            "fatigue": 0,
            "fatigueBonus": [],
            "biography": f"<p>{c.get('flav', '')}</p>",
        },
    }


actors = [to_foundry_actor(c) for c in creatures]
with open("foundry_actors.json", "w", encoding="utf-8") as f:
    json.dump(actors, f, indent=2, ensure_ascii=False)

# batch 6 goes to its own file so it can be pushed independently of the
# already-live original 56
actors2 = [to_foundry_actor(c) for c in creatures2]
with open("foundry_actors_batch6.json", "w", encoding="utf-8") as f:
    json.dump(actors2, f, indent=2, ensure_ascii=False)

for a in actors2:
    print(f"{a['name']:38s} TL={a['system']['threatLevel']:<5} hd={a['system']['hd']:<3} "
          f"hp={a['system']['health']['max']:<4} act={len(a['system']['actions'])} "
          f"abil={len(a['system']['abilities'])} zone={a['system']['zone']}")
print(f"\nWrote foundry_actors.json ({len(actors)}) and foundry_actors_batch6.json ({len(actors2)})")
