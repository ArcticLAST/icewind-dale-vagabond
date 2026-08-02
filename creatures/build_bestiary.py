import json, math, random, string, datetime
from tl_calc import calc_tl

def rid():
    return "c" + "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

def act(kind, name="", tags="", save="", focus=False, uses="", per="Day", recharge="",
        n=1, d=6, mod=0, explode=False, text="", dpr=None, mult=1):
    if dpr is None:
        dpr = kind in ("Melee Attack", "Ranged Attack", "Cast")
    return {"id": rid(), "kind": kind, "name": name, "tags": tags, "save": save,
            "focus": focus, "uses": uses, "per": per, "recharge": recharge,
            "n": n, "d": d, "mod": mod, "explode": explode, "text": text,
            "dpr": dpr, "mult": mult}

def creature(name, size, type_, sub, flav, hd, armType, armEnh, shield, weak, imm, statusImm,
             speed, spds, zone, morale, app, senses, oversize, acts, boss=False, hp_override=None):
    ARMOR = {"Unarmored":0,"Leather":1,"Hide":1,"Wood":1,"Chain":2,"Scale":2,"Plate":3,"Splint":3}
    armor = max(0, ARMOR.get(armType,0) + armEnh + (1 if shield else 0))
    per_hp = 1 if size == "Small" else 4.5
    hp = hp_override if hp_override is not None else math.floor(max(0,hd) * per_hp) * (2 if boss else 1)
    return {
        "id": rid(), "name": name, "size": size, "type": type_, "sub": sub, "flav": flav,
        "hd": hd, "hp": hp, "hpAuto": hp_override is None, "boss": boss,
        "armType": armType, "armEnh": armEnh, "shield": shield, "armor": armor, "armAuto": True,
        "weak": weak, "imm": imm, "statusImm": statusImm,
        "speed": speed, "spds": spds, "zone": zone, "morale": morale, "app": app, "senses": senses,
        "oversize": oversize, "acts": acts,
        "dprMode": "exact", "dprMan": False, "dprVal": 0
    }

creatures = []

# ---------------------------------------------------------------
# 1. Xardorok Sunblight
# ---------------------------------------------------------------
xardorok = creature(
    name="Xardorok Sunblight",
    size="Medium", type_="Humanlike", sub="",
    flav="The self-styled Iron Tyrant of the duergar, a Sunblight fanatic who dreams of dragging Ten-Towns into the dark beneath a chardalyn wing.",
    hd=8, armType="Chain", armEnh=1, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed", "Confused"],
    speed=25, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Spiked Gauntlet"),
        act("Melee Attack", name="Spiked Gauntlet", tags="", n=1, d=6, mod=2, mult=2),
        act("Cast", name="Void Bolt", tags="Remote", save="Reflex", n=1, d=8, mod=1),
        act("Ability", name="Enlarge", recharge="Cd6", dpr=False,
            text="For the duration, Xardorok is Large, his Spiked Gauntlet dice explode, and he has Favor on Might Checks and Saves."),
        act("Ability", name="Vanish", recharge="Cd6", dpr=False,
            text="Xardorok is Invisible until he Attacks, Casts, uses Enlarge, or his Focus breaks."),
        act("Action", name="Spiteful Flame", uses="2", per="Day", dpr=False,
            text="Reaction. When damaged by a Being it senses, that Being takes 8 (3d4) Fire damage and is Burning (Cd4)."),
    ],
)
creatures.append(xardorok)

# ---------------------------------------------------------------
# 2. Chardalyn Dragon
# ---------------------------------------------------------------
chardalyn_dragon = creature(
    name="Chardalyn Dragon",
    size="Huge", type_="Artificial", sub="Wyrm",
    flav="A dragon-shaped engine of black chardalyn crystal, built by duergar hands and given a stolen dragon's fury. It has no mind of its own to reason with.",
    hd=22, armType="Plate", armEnh=3, shield=False,
    weak=[], imm=["Cold"], statusImm=["Charmed", "Confused", "Frightened", "Sickened"],
    speed=30, spds={"Fly": 90}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw and 1x Tail"),
        act("Melee Attack", name="Claw", n=1, d=8, mod=6, mult=2),
        act("Melee Attack", name="Tail", tags="10' reach", n=1, d=10, mod=6, mult=1,
            text="Target is shoved 15' and Prone."),
        act("Cast", name="Malevolent Presence", tags="Near Aura", save="Will", dpr=False, focus=True,
            n=0, d=0, mod=0,
            text="Targets are Charmed and fixate on a target of the dragon's choice, moving toward it and Attacking it on their Turn."),
        act("Cast", name="Chardalyn Breath", tags="Far Cone", save="Reflex", recharge="Cd6", dpr=False,
            n=7, d=6, mod=0,
            text="Bonus burst, not counted in steady DPR."),
    ],
)
creatures.append(chardalyn_dragon)

# ---------------------------------------------------------------
# 3. Arveiaturace (reflavored core Ancient Dragon)
# ---------------------------------------------------------------
arveiaturace = creature(
    name="Arveiaturace",
    size="Giant", type_="Cryptid", sub="Wyrm",
    flav="An ancient white wyrm who has ruled the Reghed Glacier since before Ten-Towns had a name. Duergar sky-priests court her with tribute; everyone else simply prays she stays asleep.",
    hd=30, armType="Plate", armEnh=4, shield=True,
    weak=[], imm=["Cold", "Physical from non-Relics"], statusImm=["Berserk", "Charmed", "Confused", "Frightened"],
    speed=40, spds={"Fly": 80}, zone="Frontline", morale="", app="1", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw and 1x Bite"),
        act("Melee Attack", name="Bite", n=2, d=12, mod=0, mult=1),
        act("Melee Attack", name="Claw", n=1, d=10, mod=1, mult=2),
        act("Melee Attack", name="Tail", tags="10' reach", n=1, d=12, mod=0, mult=1, dpr=False,
            text="Target is shoved 30' and Prone."),
        act("Cast", name="Glacial Breath", tags="Far Cone", save="Reflex", recharge="Cd4", dpr=False,
            n=6, d=6, mod=0,
            text="Cold damage. Targets are Dazed (Cd6, Speed reduced by 20') if failed. Bonus burst, not counted in steady DPR."),
        act("Ability", name="Immutable", dpr=False, text="It can't be transformed."),
        act("Ability", name="Magic Ward IV", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 4 Mana to affect it."),
        act("Ability", name="Terror of the Glacier", dpr=False,
            text="Enemies that see it for the first time, and at the start of their Turns thereafter, must pass [Will] or be Frightened (Cd6)."),
    ],
)
creatures.append(arveiaturace)

# ---------------------------------------------------------------
# 4. Chardalyn Berserker
# ---------------------------------------------------------------
berserker = creature(
    name="Chardalyn Berserker",
    size="Medium", type_="Humanlike", sub="",
    flav="A duergar or human warrior whose mind was hollowed out and refilled with something else the moment they picked up chardalyn weapons in Xardorok's forges.",
    hd=9, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="d4", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 3x Chardalyn Weapon"),
        act("Melee Attack", name="Chardalyn Flail", tags="Thrown", save="Endure", n=1, d=8, mod=1, mult=3,
            text="Target is Sickened until the end of its next Turn if it fails."),
        act("Ability", name="Chardalyn Madness", dpr=False,
            text="At the start of its Turn, roll a d6. On a 1, it does nothing but rave to a master that isn't there."),
        act("Ability", name="Reckless", dpr=False,
            text="At the start of its Turn, it can gain Favor on its melee Attacks this Turn, but Attacks against it have Favor until its next Turn."),
    ],
)
creatures.append(berserker)

# ---------------------------------------------------------------
# 5. Ice Troll
# ---------------------------------------------------------------
ice_troll = creature(
    name="Ice Troll",
    size="Large", type_="Cryptid", sub="",
    flav="A troll that has made its peace with the Everlasting Rime, growing a hide of rime-frost and a hatred of warmth to match its hatred of everything else.",
    hd=13, armType="Scale", armEnh=1, shield=False,
    weak=["Acid", "Fire"], imm=["Cold"], statusImm=[],
    speed=40, spds={}, zone="Frontline", morale="", app="d3", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw and 1x Bite"),
        act("Melee Attack", name="Claw", n=2, d=6, mod=3, mult=2,
            text="Target has Hinder on Attacks until the end of its next Turn if it takes this damage."),
        act("Melee Attack", name="Bite", n=1, d=6, mod=3, mult=1),
        act("Ability", name="Cold Aura", dpr=True, n=1, d=6, mod=0, mult=1,
            text="Any Being that starts its Turn within Close takes this damage."),
        act("Ability", name="Lesser Regenerate II", dpr=False,
            text="Regains 10 HP on each of its Turns unless it took damage it was Weak to in the last Round. It can't be reduced below 1 HP except by damage it is Weak to."),
    ],
)
creatures.append(ice_troll)

# ---------------------------------------------------------------
# 6. Goliath Werebear
# ---------------------------------------------------------------
werebear = creature(
    name="Goliath Werebear (Toji)",
    size="Large", type_="Humanlike", sub="Shapechanger",
    flav="A goliath cursed - or blessed - with the spirit of the great bear. Fiercely protective of Icewind Dale's few remaining innocents.",
    hd=16, armType="Chain", armEnh=0, shield=True,
    weak=["Silvered Weapons"], imm=["Physical from non-Relics"], statusImm=[],
    speed=30, spds={"Swim": 30}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Bite and 1x Claw"),
        act("Melee Attack", name="Bite", n=2, d=10, mod=4, mult=1,
            text="A Humanlike hit by this must pass [Endure] or be cursed with werebear lycanthropy."),
        act("Melee Attack", name="Claw", n=2, d=8, mod=4, mult=1),
        act("Melee Attack", name="Greataxe", tags="Humanoid form only", n=1, d=12, mod=3, mult=1, dpr=False),
        act("Action", name="Stone's Endurance", recharge="Cd6", dpr=False,
            text="Reaction. When damaged, reduce the damage taken by 8 (d12+2)."),
    ],
)
creatures.append(werebear)

# ---------------------------------------------------------------
# 7. Grandolpha Muzgardt
# ---------------------------------------------------------------
grandolpha = creature(
    name="Grandolpha Muzgardt",
    size="Medium", type_="Humanlike", sub="",
    flav="A duergar witch of dubious loyalty who trades secrets, poisons, and polymorphs for coin - or for a favor she'll collect on later.",
    hd=4, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed"],
    speed=25, spds={}, zone="Backline", morale="6", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Cast", name="Poison Spray", tags="Close", save="Endure", n=2, d=8, mod=0),
        act("Ability", name="Vanish", uses="3", per="Day", dpr=False, text="Grandolpha is Invisible until she Attacks or Casts a Spell that deals damage."),
        act("Ability", name="Hidebound", uses="3", per="Day", dpr=False, text="Grandolpha gains 3 Armor for the duration."),
        act("Cast", name="Sculpt Flesh", uses="3", per="Day", dpr=False, focus=True,
            n=0, d=0, mod=0,
            text="As the Polymorph Spell, Targeting only herself."),
    ],
)
creatures.append(grandolpha)

# ---------------------------------------------------------------
# 8-10. Auril, the Frostmaiden - three forms
# ---------------------------------------------------------------
auril_1 = creature(
    name="Auril, the Frostmaiden (First Form)",
    size="Medium", type_="Outer", sub="Divine",
    flav="The goddess of winter's cruelty, wearing a shape of frost-feathers and talons. She cannot truly die here - only be driven from one mask into the next.",
    hd=11, armType="Scale", armEnh=0, shield=False,
    weak=["Fire"], imm=["Cold", "Poison"],
    statusImm=["Berserk", "Charmed", "Confused", "Frightened", "Paralyzed", "Sickened"],
    speed=30, spds={"Fly": 60}, zone="Midline", morale="", app="1", senses=["Allsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Talons"),
        act("Melee Attack", name="Talons", n=1, d=8, mod=2, mult=2, text="Cold damage."),
        act("Cast", name="Touch of Frost", tags="Touch", save="Endure", focus=False, n=3, d=8, mod=0,
            text="Target can't take Reactions until the start of its next Turn."),
        act("Cast", name="Frost Orb", tags="Remote", save="Reflex", n=2, d=8, mod=0),
        act("Ability", name="Divine Rejuvenation", dpr=False,
            text="When reduced to 0 HP, Auril's body melts away and she reappears at full HP in her Second Form within Near."),
        act("Ability", name="Magic Ward IV", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 4 Mana to affect it."),
    ],
    boss=True,
)
creatures.append(auril_1)

auril_2 = creature(
    name="Auril, the Frostmaiden (Second Form)",
    size="Large", type_="Primordial", sub="",
    flav="Stripped of her first mask, Auril rises as a knight carved from glacier ice, morningstar in hand and murder in her unreadable face.",
    hd=15, armType="Plate", armEnh=1, shield=False,
    weak=["Fire"], imm=["Cold", "Poison"],
    statusImm=["Berserk", "Charmed", "Confused", "Frightened", "Paralyzed", "Sickened"],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Allsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Ice Morningstar"),
        act("Melee Attack", name="Ice Morningstar", n=1, d=8, mod=5, mult=2, text="Cold damage."),
        act("Ability", name="Frost Nova", dpr=True, n=2, d=6, mod=0, mult=1,
            text="Any Being within Close takes this Cold damage when Auril is struck in melee (no Action)."),
        act("Cast", name="Cone of Cold", tags="Far Cone", save="Endure", recharge="Cd6", dpr=False,
            n=8, d=8, mod=0, text="Bonus burst, not counted in steady DPR."),
        act("Ability", name="Ice Stasis", uses="1", per="Round", recharge="Cd6", dpr=False,
            text="Target must pass [Will] or become Restrained and Vulnerable in an ice crystal, taking 21 (6d6) Cold damage at the start of each of its Turns until it breaks free or the crystal (0 Armor, 9 HP, Immune except Fire) is destroyed."),
        act("Ability", name="Divine Rejuvenation", dpr=False,
            text="When reduced to 0 HP, Auril's body shatters and she reappears at full HP in her Third Form within Near."),
        act("Ability", name="Magic Ward IV", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 4 Mana to affect it."),
    ],
    boss=True,
)
creatures.append(auril_2)

auril_3 = creature(
    name="Auril, the Frostmaiden (Third Form)",
    size="Medium", type_="Primordial", sub="Beyonder",
    flav="A shard of pure winter, all that's left when the masks come off - and the most dangerous thing Auril has ever been.",
    hd=15, armType="Plate", armEnh=1, shield=True,
    weak=["Shock"], imm=["Cold", "Poison"],
    statusImm=["Berserk", "Charmed", "Confused", "Frightened", "Paralyzed", "Prone", "Sickened"],
    speed=0, spds={"Fly": 30}, zone="Backline", morale="", app="1", senses=["Allsight", "Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Polar Ray"),
        act("Cast", name="Polar Ray", tags="Remote", save="Reflex", n=3, d=6, mod=0, mult=2),
        act("Ability", name="Frigid Aura", dpr=True, n=3, d=6, mod=0, mult=1,
            text="Any Being that Ends its Turn within Close takes this Cold damage."),
        act("Ability", name="Blizzard Veil", dpr=False, focus=True,
            text="A 30' radius sphere centered on Auril is heavily obscured for the duration."),
        act("Ability", name="Divine Resurrection", dpr=False,
            text="When reduced to 0 HP, Auril's crystalline form shatters and she is gone - until the next winter solstice, when she reappears at full HP somewhere cold and remote."),
        act("Ability", name="Magic Ward IV", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 4 Mana to affect it."),
    ],
    boss=True,
)
creatures.append(auril_3)

# ---------------------------------------------------------------
# BATCH 2
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# 11. Frost Giant (custom - core only has Giant, Hill/Stone/Cyclops, none at CR8 tier)
# ---------------------------------------------------------------
frost_giant = creature(
    name="Frost Giant",
    size="Huge", type_="Cryptid", sub="",
    flav="A hulking raider of the Reghed Glacier, patchwork-armored and greataxe-armed, who measures worth in plunder and the size of what it can throw.",
    hd=15, armType="Scale", armEnh=1, shield=False,
    weak=[], imm=["Cold"], statusImm=[],
    speed=40, spds={}, zone="Frontline", morale=9, app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Greataxe"),
        act("Melee Attack", name="Greataxe", tags="10' reach", n=1, d=10, mod=5, mult=2),
        act("Ranged Attack", name="Rock", n=2, d=6, mod=3, mult=1),
    ],
)
creatures.append(frost_giant)

# ---------------------------------------------------------------
# 12. Abominable Yeti (custom - buffed beyond core Yeti's TL 3.5)
# ---------------------------------------------------------------
abominable_yeti = creature(
    name="Abominable Yeti",
    size="Huge", type_="Cryptid", sub="",
    flav="The largest and cruelest of its kind, driven from even the yeti packs of the high Spine for what it did to them.",
    hd=24, armType="Scale", armEnh=3, shield=False,
    weak=["Fire"], imm=["Cold"], statusImm=[],
    speed=40, spds={"Climb": 40}, zone="Frontline", morale=10, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw"),
        act("Melee Attack", name="Claw", n=1, d=10, mod=7, mult=2, text="Cold damage."),
        act("Ability", name="Chilling Gaze", uses="1", per="Round", dpr=False,
            text="Target within Near that can see it must pass [Endure] or take 21 (6d6) Cold damage and be Paralyzed for 1 Minute, repeating the Save at the end of each of its Turns. On a pass (or the Paralysis ending), it is immune to this Gaze for 1 Hour."),
        act("Cast", name="Cold Breath", tags="Near Cone", save="Endure", recharge="Cd6", dpr=False,
            n=10, d=8, mod=0, text="Cold damage."),
    ],
)
creatures.append(abominable_yeti)

# ---------------------------------------------------------------
# 13. Yeti (renamed/reflavored copy of the core entry)
# ---------------------------------------------------------------
yeti = creature(
    name="Yeti",
    size="Large", type_="Cryptid", sub="",
    flav="A shaggy, ape-like predator of the high passes above Icewind Dale, more territorial than truly evil.",
    hd=5, armType="Chain", armEnh=0, shield=False,
    weak=["Fire"], imm=["Cold"], statusImm=[],
    speed=40, spds={"Climb": 40}, zone="Frontline", morale=9, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw"),
        act("Melee Attack", name="Claw", n=1, d=6, mod=0, mult=2,
            text="plus 9 (2d8) if failed by 5 or more"),
        act("Cast", name="Terror Glare", tags="Sight", save="Will", uses="1", per="Day", dpr=False,
            n=0, d=0, mod=0, text="Frightened (Cd4, Paralyzed)."),
    ],
)
creatures.append(yeti)

# ---------------------------------------------------------------
# 14. Winter Wolf (renamed/reflavored copy of the core entry)
# ---------------------------------------------------------------
winter_wolf = creature(
    name="Winter Wolf",
    size="Large", type_="Beast", sub="",
    flav="Xardorok's hunting packs range the tundra on four frost-white legs, breath steaming with more than cold.",
    hd=6, armType="Leather", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=50, spds={}, zone="Frontline", morale=9, app="d4", senses=[],
    oversize=0,
    acts=[
        act("Cast", name="Frost Breath", tags="Close Aura", save="Endure", recharge="Cd4", dpr=False,
            n=6, d=4, mod=0, text="Cold damage."),
        act("Melee Attack", name="Bite", n=2, d=6, mod=0),
        act("Ability", name="Pack Hunter", dpr=False,
            text="Targets within 5' of one of this Being's Allies are Vulnerable to its attacks."),
        act("Ability", name="Pounce", dpr=False,
            text="If it moves at least 20' before an attack on the same Turn, the Target is also knocked Prone if it is Large or smaller."),
    ],
)
creatures.append(winter_wolf)

# ---------------------------------------------------------------
# 15. Vellynne Harpell
# ---------------------------------------------------------------
vellynne = creature(
    name="Vellynne Harpell",
    size="Medium", type_="Humanlike", sub="",
    flav="A pragmatic Arcane Brotherhood wizard chasing rumors of Netheril, more interested in what Icewind Dale can teach her than what it can give her.",
    hd=7, armType="Leather", armEnh=2, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={}, zone="Backline", morale=7, app="1", senses=[],
    oversize=0,
    acts=[
        act("Cast", name="Chill Touch", tags="Remote", save="Reflex", n=2, d=8, mod=1,
            text="Target can't regain HP until the start of Vellynne's next Turn."),
        act("Cast", name="Vampiric Touch", tags="Touch", save="Endure", uses="3", per="Day", dpr=False,
            n=3, d=6, mod=0, text="Vellynne regains HP equal to half the damage dealt."),
        act("Cast", name="Wand of Magic Missiles", tags="Remote", uses="7", per="Day", dpr=False,
            n=3, d=4, mod=3, text="Always hits."),
    ],
)
creatures.append(vellynne)

# ---------------------------------------------------------------
# 16. Duergar Hammerer (piloted construct exosuit)
# ---------------------------------------------------------------
duergar_hammerer = creature(
    name="Duergar Hammerer",
    size="Medium", type_="Artificial", sub="",
    flav="A duergar strapped into a hulking iron frame of pistons and grinding gears, more machine than dwarf until the frame breaks open.",
    hd=3, armType="Chain", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed", "Frightened"],
    speed=20, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Claw and 1x Hammer"),
        act("Melee Attack", name="Claw", n=1, d=4, mod=0),
        act("Melee Attack", name="Hammer", n=1, d=6, mod=1),
        act("Ability", name="Engine of Pain", dpr=False,
            text="Once per Turn, an Attacker can target the duergar trapped inside instead, at Hinder. On a hit, the hammerer takes an extra 5 (d10) damage and can Attack immediately as a Reaction."),
    ],
)
creatures.append(duergar_hammerer)

# ---------------------------------------------------------------
# 17. Gunvald Halraggson (Reghed Tribe of the Bear king)
# ---------------------------------------------------------------
gunvald = creature(
    name="Gunvald Halraggson",
    size="Medium", type_="Humanlike", sub="",
    flav="King of the Tribe of the Bear, a mountain of a man who has never lost a duel and doesn't plan to start.",
    hd=8, armType="Hide", armEnh=0, shield=True,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 3x Battleaxe"),
        act("Melee Attack", name="Battleaxe", n=1, d=10, mod=1, mult=3),
        act("Ability", name="Menacing Blows", uses="1", per="Turn", dpr=False,
            text="Deals an extra 6 (d12) damage with a weapon Attack. Target must pass [Will] or be Frightened until the start of Gunvald's next Turn."),
        act("Ability", name="Second Wind", recharge="Cd6", dpr=False,
            text="Bonus Action. Gunvald regains 15 HP."),
        act("Ability", name="Indomitable", uses="3", per="Day", dpr=False,
            text="Gunvald can reroll a failed Save. He must use the new roll."),
    ],
)
creatures.append(gunvald)

# ---------------------------------------------------------------
# 18. Snow Golem
# ---------------------------------------------------------------
snow_golem = creature(
    name="Snow Golem",
    size="Medium", type_="Artificial", sub="",
    flav="A rough-hewn watchman of packed snow and ice, animated to guard a place or a person until it melts or is ordered otherwise.",
    hd=9, armType="Unarmored", armEnh=0, shield=False,
    weak=["Fire"], imm=["Cold", "Poison"], statusImm=["Charmed", "Frightened", "Paralyzed"],
    speed=10, spds={}, zone="Frontline", morale="", app="1", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 3x Slam"),
        act("Melee Attack", name="Slam", n=1, d=6, mod=0, mult=3, text="Cold damage."),
        act("Ranged Attack", name="Snowball", n=1, d=8, mod=0, text="Cold damage."),
        act("Ability", name="Cold Absorption", dpr=False,
            text="Whenever the golem is dealt Cold damage, it instead regains that much HP."),
    ],
)
creatures.append(snow_golem)

# ---------------------------------------------------------------
# 19. Coldlight Walker
# ---------------------------------------------------------------
coldlight_walker = creature(
    name="Coldlight Walker",
    size="Medium", type_="Undead", sub="",
    flav="A radiant, frozen corpse that glows with a false dawn - beautiful right up until it turns to look at you.",
    hd=11, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=["Cold"], statusImm=["Blinded", "Charmed", "Paralyzed"],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Slam and 1x Cold Ray"),
        act("Melee Attack", name="Slam", n=1, d=8, mod=2, text="Cold damage."),
        act("Ranged Attack", name="Cold Ray", n=2, d=10, mod=2, text="Cold damage."),
        act("Ability", name="Blinding Light", dpr=False,
            text="Bonus Action. Sheds bright light to Near and dim light beyond that. A Being in its bright light must pass [Endure] or be Blinded until the start of the walker's next Turn."),
        act("Ability", name="Icy Doom", dpr=False,
            text="A Being it kills freezes solid for 9 Days, during which it can't be thawed, harmed by Fire, animated, or raised from the dead."),
    ],
)
creatures.append(coldlight_walker)

# ---------------------------------------------------------------
# BATCH 3
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# 20. Avarice (Arcane Brotherhood wizard)
# ---------------------------------------------------------------
avarice = creature(
    name="Avarice",
    size="Medium", type_="Humanlike", sub="",
    flav="A tiefling wizard of the Arcane Brotherhood, chasing power in the ruins beneath the glacier and willing to freeze anyone who gets in her way.",
    hd=18, armType="Leather", armEnh=3, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Backline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Cast", name="Fire Bolt", tags="Remote", save="Reflex", n=3, d=10, mod=2),
        act("Cast", name="Cone of Cold", tags="Near Cone", save="Endure", uses="2", per="Day", dpr=False,
            n=8, d=8, mod=0, text="Cold damage."),
        act("Action", name="Banishing Rebuke", recharge="Cd8", dpr=False,
            text="Reaction. When damaged by a Being she senses, banish it for 1 Minute to a frigid prison: it is Incapacitated and takes 3 (d10) Cold damage at the start of each of its Turns, repeating a Will Save at the end of each of its Turns to escape early."),
    ],
)
creatures.append(avarice)

# ---------------------------------------------------------------
# 21. Dzaan's Simulacrum
# ---------------------------------------------------------------
dzaan_simulacrum = creature(
    name="Dzaan's Simulacrum",
    size="Medium", type_="Artificial", sub="",
    flav="A frost-pale duplicate of the missing wizard Dzaan, animated by the same magic he used to survive his own death - badly.",
    hd=4, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Backline", morale="6", app="1", senses=[],
    oversize=0,
    acts=[
        act("Cast", name="Shocking Grasp", tags="Touch", n=1, d=8, mod=0,
            text="Target can't take Reactions until the start of its next Turn."),
        act("Cast", name="Acid Splash", tags="Remote", save="Reflex", dpr=False,
            n=2, d=6, mod=0),
        act("Cast", name="Magic Missile", tags="Remote", uses="2", per="Day", dpr=False,
            n=1, d=4, mod=1, mult=3, text="Always hits."),
    ],
)
creatures.append(dzaan_simulacrum)

# ---------------------------------------------------------------
# 22. Duergar Mind Master
# ---------------------------------------------------------------
duergar_mind_master = creature(
    name="Duergar Mind Master",
    size="Medium", type_="Humanlike", sub="",
    flav="A duergar psion whose dagger hurts less than the thoughts it leaves behind.",
    hd=5, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed", "Confused"],
    speed=25, spds={}, zone="Midline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Mind-Poison Dagger"),
        act("Melee Attack", name="Mind-Poison Dagger", n=1, d=4, mod=1, mult=2,
            text="Psychic damage."),
        act("Ability", name="Mind Mastery", uses="1", per="Turn", dpr=False,
            text="Target within Far must pass [Will] or the duergar forces it to Attack another Being it can see, or Move up to 10' in a direction of the duergar's choice, on its Reaction."),
        act("Ability", name="Vanish", recharge="Cd6", dpr=False,
            text="The duergar is Invisible for up to 1 Hour, until it Attacks, Casts, or its Focus breaks."),
    ],
)
creatures.append(duergar_mind_master)

# ---------------------------------------------------------------
# 23. Icewind Kobold
# ---------------------------------------------------------------
icewind_kobold = creature(
    name="Icewind Kobold",
    size="Small", type_="Humanlike", sub="",
    flav="A shivering little opportunist that has learned to dig deep and strike from the dark - alone, it's nothing; in a pack, it's a problem.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={"Climb": 20}, zone="Midline", morale=6, app="d6", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Dagger", tags="Thrown", n=1, d=4, mod=0),
        act("Ability", name="Pack Tactics", dpr=False,
            text="It has Favor on Attacks against a Target that has one of its Allies within Close."),
    ],
)
creatures.append(icewind_kobold)

# ---------------------------------------------------------------
# 24. Kobold Vampire Spawn
# ---------------------------------------------------------------
kobold_vampire_spawn = creature(
    name="Kobold Vampire Spawn",
    size="Small", type_="Undead", sub="",
    flav="A kobold that crossed the wrong cave in Termalaine's mines and came back changed, hungry, and considerably harder to kill.",
    hd=9, armType="Leather", armEnh=1, shield=False,
    weak=[], imm=["Physical from non-Relics"], statusImm=[],
    speed=30, spds={"Climb": 20}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=6,
            text="Target's Max HP is reduced by the damage dealt until it finishes a Shift; the vampire spawn heals for the same amount."),
        act("Ability", name="Pack Tactics", dpr=False,
            text="It has Favor on Attacks against a Target that has one of its Allies within Close."),
        act("Ability", name="Lesser Regenerate II", dpr=False,
            text="Regains 10 HP on each of its Turns unless it took damage it was Weak to in the last Round. It can't be reduced below 1 HP except by damage it is Weak to."),
    ],
)
creatures.append(kobold_vampire_spawn)

# ---------------------------------------------------------------
# 25. Frost Giant Skeleton
# ---------------------------------------------------------------
frost_giant_skeleton = creature(
    name="Frost Giant Skeleton",
    size="Huge", type_="Undead", sub="",
    flav="A frost giant's bones, picked clean by wind and time, still swinging a greataxe for a master it can no longer name.",
    hd=13, armType="Scale", armEnh=0, shield=False,
    weak=["Blunt"], imm=["Cold", "Poison"], statusImm=[],
    speed=40, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Greataxe"),
        act("Melee Attack", name="Greataxe", tags="10' reach", n=1, d=10, mod=4, mult=2),
        act("Ability", name="Freezing Stare", uses="1", per="Round", dpr=False,
            text="Target within Far it senses must pass [Endure] or take 17 (5d6) Cold damage and be Paralyzed until the end of its next Turn."),
    ],
)
creatures.append(frost_giant_skeleton)

# ---------------------------------------------------------------
# 26. Chwinga
# ---------------------------------------------------------------
chwinga = creature(
    name="Chwinga",
    size="Small", type_="Fae", sub="",
    flav="A tiny nature spirit of Icewind Dale's dwindling wild places, shy, generous, and quick to hide in the nearest stone or stream.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Climb": 20, "Swim": 20}, zone="Backline", morale="", app="1", senses=["Blindsight"],
    oversize=0,
    hp_override=2,
    acts=[
        act("Ability", name="Magical Gift", uses="1", per="Day", dpr=False,
            text="Targets a willing Humanlike within Close, who gains a minor supernatural charm (GM's discretion)."),
        act("Ability", name="Natural Shelter", dpr=False,
            text="It can retreat into a rock, living plant, or natural fresh water in its space (no Action), where it can't be Targeted by anything. It can emerge with an Action."),
        act("Ability", name="Evasion", dpr=False,
            text="Checks or Saves it would take half damage on a pass instead take none, and it takes half on a fail."),
    ],
)
creatures.append(chwinga)

# ---------------------------------------------------------------
# 27. Jarund Elkhardt (Tribe of the Elk king)
# ---------------------------------------------------------------
jarund = creature(
    name="Jarund Elkhardt",
    size="Medium", type_="Humanlike", sub="",
    flav="King of the Tribe of the Elk, who fights with a warhammer in one hand and his shield as a second weapon in the other.",
    hd=10, armType="Hide", armEnh=0, shield=True,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Warhammer and 1x Shield Bash"),
        act("Melee Attack", name="Warhammer", n=1, d=10, mod=1, mult=2),
        act("Melee Attack", name="Shield Bash", n=1, d=6, mod=1,
            text="Target of Large or smaller is shoved 5' and Jarund can Move into the space."),
        act("Ability", name="Brute", dpr=False,
            text="Jarund's weapon Attacks deal an extra damage die (already included above)."),
    ],
)
creatures.append(jarund)

# ---------------------------------------------------------------
# 28. Bjornhild Solvigsdottir (Tribe of the Tiger queen)
# ---------------------------------------------------------------
bjornhild = creature(
    name="Bjornhild Solvigsdottir",
    size="Medium", type_="Humanlike", sub="",
    flav="Queen of the Tribe of the Tiger, who wears Auril's favor like a second edge on her greataxe.",
    hd=13, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Greataxe"),
        act("Melee Attack", name="Greataxe", n=1, d=12, mod=4, mult=2),
        act("Ability", name="Auril's Blessing", uses="3", per="Day", dpr=False,
            text="A weapon Attack that hits deals an extra 11 (2d10) Cold damage."),
    ],
)
creatures.append(bjornhild)

# ---------------------------------------------------------------
# 29. Isarr Kronenstrom (Tribe of the Wolf leader)
# ---------------------------------------------------------------
isarr = creature(
    name="Isarr Kronenstrom",
    size="Medium", type_="Humanlike", sub="",
    flav="Leader of the Tribe of the Wolf in name only - the tribe follows him because they're too afraid to stop.",
    hd=16, armType="Hide", armEnh=2, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 3x Sickle"),
        act("Melee Attack", name="Sickle", n=1, d=4, mod=6, mult=3,
            text="Deals an extra 13 (2d12) damage if the Target has no Allies within Close."),
        act("Ranged Attack", name="Heavy Crossbow", n=1, d=10, mod=4, dpr=False),
        act("Ability", name="Blood Frenzy", dpr=False,
            text="It has Favor on melee Attacks against a Target that isn't at full HP."),
        act("Ability", name="Indomitable", uses="3", per="Day", dpr=False,
            text="Isarr can reroll a failed Save. He must use the new roll."),
    ],
)
creatures.append(isarr)

# ---------------------------------------------------------------
# BATCH 4
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# 30. Demos Magen (soldier construct)
# ---------------------------------------------------------------
demos_magen = creature(
    name="Demos Magen",
    size="Medium", type_="Artificial", sub="",
    flav="A soldier-shaped construct from the ruins beneath the glacier, built to fight and little else.",
    hd=3, armType="Chain", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed", "Confused", "Frightened", "Paralyzed"],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Greatsword and 1x Crossbow"),
        act("Melee Attack", name="Greatsword", n=1, d=6, mod=1),
        act("Ranged Attack", name="Light Crossbow", n=1, d=8, mod=2, dpr=False),
        act("Ability", name="Fiery End", dpr=False,
            text="When it dies, its body disintegrates in a harmless burst of fire and smoke, leaving behind anything it carried."),
    ],
)
creatures.append(demos_magen)

# ---------------------------------------------------------------
# 31. Galvan Magen (lightning construct)
# ---------------------------------------------------------------
galvan_magen = creature(
    name="Galvan Magen",
    size="Medium", type_="Artificial", sub="",
    flav="A hovering construct that crackles faintly with stored lightning, built by the Netherese to guard what they couldn't carry.",
    hd=6, armType="Chain", armEnh=-1, shield=False,
    weak=[], imm=["Shock", "Poison"], statusImm=["Charmed", "Confused", "Frightened", "Paralyzed"],
    speed=30, spds={"Fly": 30}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Shocking Touch"),
        act("Melee Attack", name="Shocking Touch", n=1, d=6, mod=2, mult=2, text="Shock damage."),
        act("Cast", name="Static Discharge", tags="Far Line", save="Reflex", recharge="Cd6", dpr=False,
            n=4, d=10, mod=0, text="Shock damage."),
        act("Ability", name="Fiery End", dpr=False,
            text="When it dies, its body disintegrates in a harmless burst of fire and smoke, leaving behind anything it carried."),
    ],
)
creatures.append(galvan_magen)

# ---------------------------------------------------------------
# 32. Hypnos Magen (control construct)
# ---------------------------------------------------------------
hypnos_magen = creature(
    name="Hypnos Magen",
    size="Medium", type_="Artificial", sub="",
    flav="A construct with silver-glowing eyes, built to talk enemies into laying down their arms - or into far worse ideas.",
    hd=4, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed", "Confused", "Frightened", "Paralyzed"],
    speed=30, spds={}, zone="Backline", morale="", app="1", senses=["Telepathy"],
    oversize=0,
    acts=[
        act("Cast", name="Psychic Lash", tags="Remote", save="Will", n=1, d=8, mod=0),
        act("Cast", name="Suggestion", tags="Remote", save="Will", dpr=False,
            n=0, d=0, mod=0, text="Charms the Target into following a reasonable suggestion for the duration. Only works on a Being it can speak to telepathically."),
        act("Ability", name="Fiery End", dpr=False,
            text="When it dies, its body disintegrates in a harmless burst of fire and smoke, leaving behind anything it carried."),
    ],
)
creatures.append(hypnos_magen)

# ---------------------------------------------------------------
# 33. Verbeeg Longstrider
# ---------------------------------------------------------------
verbeeg_longstrider = creature(
    name="Verbeeg Longstrider",
    size="Large", type_="Cryptid", sub="",
    flav="A lean, watchful verbeeg who ranges far ahead of its kin, spear in hand and half a dozen quiet spells up its sleeve.",
    hd=8, armType="Hide", armEnh=2, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=50, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Spear"),
        act("Melee Attack", name="Spear", n=1, d=8, mod=2, mult=2),
        act("Ranged Attack", name="Sling", tags="", save="Endure", dpr=False,
            n=3, d=4, mod=2, text="Target is Dazed until the end of its next Turn if it fails."),
        act("Ability", name="Simple Weapon Wielder", dpr=False,
            text="Its weapon Attacks deal an extra damage die (already included above)."),
    ],
)
creatures.append(verbeeg_longstrider)

# ---------------------------------------------------------------
# 34. Verbeeg Marauder
# ---------------------------------------------------------------
verbeeg_marauder = creature(
    name="Verbeeg Marauder",
    size="Large", type_="Cryptid", sub="",
    flav="A verbeeg raider who has traded patience for plunder, and isn't shy about which one it enjoys more.",
    hd=5, armType="Hide", armEnh=0, shield=True,
    weak=[], imm=[], statusImm=[],
    speed=40, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Spear"),
        act("Melee Attack", name="Spear", n=2, d=6, mod=0, mult=2),
        act("Ability", name="Simple Weapon Wielder", dpr=False,
            text="Its weapon Attacks deal an extra damage die (already included above)."),
    ],
)
creatures.append(verbeeg_marauder)

# ---------------------------------------------------------------
# 35. Gnoll Vampire
# ---------------------------------------------------------------
gnoll_vampire = creature(
    name="Gnoll Vampire",
    size="Medium", type_="Undead", sub="Shapechanger",
    flav="A gnoll raider who fed on the wrong corpse in the wrong crypt and rose again craving more.",
    hd=15, armType="Scale", armEnh=2, shield=False,
    weak=[], imm=["Physical from non-Relics"], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Bite and 1x Claws"),
        act("Melee Attack", name="Bite", n=2, d=6, mod=7,
            text="Target's Max HP is reduced by the damage dealt until it finishes a Shift; the vampire heals for the same amount."),
        act("Melee Attack", name="Claws", n=2, d=4, mod=7),
        act("Ability", name="Frightful Cackle", uses="1", per="Day", dpr=False,
            text="Beings of its choice within Far that can hear it must pass [Will] or be Frightened (Cd6)."),
        act("Ability", name="Lesser Regenerate II", dpr=False,
            text="Regains 10 HP on each of its Turns unless it took damage it was Weak to in the last Round. It can't be reduced below 1 HP except by damage it is Weak to."),
    ],
)
creatures.append(gnoll_vampire)

# ---------------------------------------------------------------
# 36. Goliath Warrior
# ---------------------------------------------------------------
goliath_warrior = creature(
    name="Goliath Warrior",
    size="Medium", type_="Humanlike", sub="",
    flav="A goliath fighter of the Spine of the World, at home on any cliff face and unbothered by the cold.",
    hd=4, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Greataxe"),
        act("Melee Attack", name="Greataxe", n=1, d=12, mod=1, mult=2),
        act("Ability", name="Stone's Endurance", recharge="Cd6", dpr=False,
            text="Reaction. When damaged, reduce the damage taken by 9 (d12+3)."),
    ],
)
creatures.append(goliath_warrior)

# ---------------------------------------------------------------
# 37. Yeti Tyke
# ---------------------------------------------------------------
yeti_tyke = creature(
    name="Yeti Tyke",
    size="Small", type_="Cryptid", sub="",
    flav="A yeti cub, more curious than dangerous - unless its parents are close, in which case it's not the problem.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=["Cold"], statusImm=[],
    speed=20, spds={"Climb": 20}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Claw", n=1, d=4, mod=0, text="Cold damage."),
    ],
)
creatures.append(yeti_tyke)

# ---------------------------------------------------------------
# 38. Nass Lantomir's Ghost
# ---------------------------------------------------------------
nass_ghost = creature(
    name="Nass Lantomir's Ghost",
    size="Medium", type_="Undead", sub="",
    flav="A Netherese wizard's spirit, still furious about the theft that killed him and still cleverer than most things that will ever threaten you.",
    hd=10, armType="Unarmored", armEnh=2, shield=False,
    weak=[], imm=["Cold", "Physical from non-Relics"], statusImm=["Charmed", "Frightened", "Paralyzed"],
    speed=0, spds={"Fly": 40}, zone="Midline", morale="", app="1", senses=["Darksight", "Allsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Withering Touch", n=5, d=6, mod=4),
        act("Ability", name="Horrifying Visage", dpr=False,
            text="Beings within Far that can see it must pass [Will] or be Frightened (1 Minute); if failed by 5 or more, also aged 1d4x10 years."),
        act("Ability", name="Possession", recharge="Cd6", dpr=False,
            text="A Humanlike within Close must pass [Will] or be possessed: it is Incapacitated and the ghost controls its body (using the target's Stats) until the body drops to 0 HP, the ghost ends the possession (no Action), or the ghost is forced out by a Spell like Dispel."),
    ],
)
creatures.append(nass_ghost)

# ---------------------------------------------------------------
# 39. Hengar Aesnvaard
# ---------------------------------------------------------------
hengar = creature(
    name="Hengar Aesnvaard",
    size="Medium", type_="Humanlike", sub="",
    flav="A militia captain of Bryn Shander, steady in a shield wall and stubborn everywhere else.",
    hd=8, armType="Chain", armEnh=0, shield=True,
    weak=[], imm=[], statusImm=["Frightened"],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 3x Spear"),
        act("Melee Attack", name="Spear", n=1, d=8, mod=1, mult=3),
        act("Melee Attack", name="Shield Bash", n=1, d=4, mod=4, dpr=False,
            text="Target of Medium or smaller must pass [Might] or be knocked Prone."),
        act("Action", name="Parry", recharge="Cd4", dpr=False,
            text="Reaction. Hengar gains +3 Armor against one melee Attack that would hit him, if he can see the Attacker and is wielding a melee weapon."),
    ],
)
creatures.append(hengar)

# ---------------------------------------------------------------
# BATCH 5 - creatures with no core Vagabond equivalent
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# 40. Mind Flayer
# ---------------------------------------------------------------
mind_flayer = creature(
    name="Mind Flayer",
    size="Medium", type_="Outer", sub="Beyonder",
    flav="An alien intellect wrapped in a squid-headed humanoid shape, patient, cruel, and always hungry for something a body can't hold.",
    hd=13, armType="Chain", armEnh=2, shield=False,
    weak=[], imm=[], statusImm=["Charmed", "Frightened"],
    speed=30, spds={}, zone="Midline", morale="", app="1", senses=["Telepathy", "Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Tentacles", n=4, d=8, mod=2,
            text="Psychic damage. Target of Medium or smaller is Restrained until it escapes."),
        act("Cast", name="Mind Blast", tags="Near Cone", save="Will", recharge="Cd6", dpr=False,
            n=4, d=8, mod=2, text="Psychic damage. Targets are Dazed (1 Minute) if failed."),
        act("Ability", name="Extract Brain", dpr=False,
            text="Melee Attack against an Incapacitated Target it has Restrained: 30 (10d6) damage, killing instantly by devouring the brain if this reduces it to 0 HP."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
    ],
)
creatures.append(mind_flayer)

# ---------------------------------------------------------------
# 41. Umber Hulk
# ---------------------------------------------------------------
umber_hulk = creature(
    name="Umber Hulk",
    size="Large", type_="Cryptid", sub="",
    flav="A burrowing horror of chitin and claw, its mandibles alone worse than most things Underdark tunnels produce.",
    hd=8, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw and 1x Mandibles"),
        act("Melee Attack", name="Claw", n=1, d=8, mod=1, mult=2),
        act("Melee Attack", name="Mandibles", n=2, d=8, mod=1, mult=1),
        act("Ability", name="Confusing Gaze", dpr=False,
            text="A Being that starts its Turn within Near and can see its eyes must pass [Will] or be Confused until the start of its next Turn. A Being can avert its eyes to avoid the Save, but then can't see it until its own next Turn."),
    ],
)
creatures.append(umber_hulk)

# ---------------------------------------------------------------
# 42. Myconid Sovereign
# ---------------------------------------------------------------
myconid_sovereign = creature(
    name="Myconid Sovereign",
    size="Large", type_="Primordial", sub="",
    flav="The eldest fungus of its circle, crowned in spore-dust, ruling a patch of glowing mushrooms deep under the Reghed Glacier.",
    hd=6, armType="Hide", armEnh=0, shield=False,
    weak=["Fire"], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Fist", n=3, d=4, mod=0, text="Poison damage."),
        act("Ability", name="Pacifying Spores", dpr=False,
            text="A Being within Close must pass [Endure] or be Incapacitated (1 Minute), repeating the Save at the end of each of its Turns."),
        act("Ability", name="Hallucination Spores", dpr=False,
            text="A Being within Close must pass [Endure] or be Confused (1 Minute), repeating the Save at the end of each of its Turns."),
        act("Ability", name="Sun Sickness", dpr=False,
            text="While in sunlight, its Checks and Saves have Hinder, and it dies after 1 Hour in direct sunlight."),
    ],
)
creatures.append(myconid_sovereign)

# ---------------------------------------------------------------
# 43. Quaggoth
# ---------------------------------------------------------------
quaggoth = creature(
    name="Quaggoth",
    size="Medium", type_="Cryptid", sub="",
    flav="A shaggy, feral humanoid of the Underdark, more animal instinct than mind, and most dangerous when it's already hurt.",
    hd=4, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=[],
    speed=30, spds={"Climb": 30}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw"),
        act("Melee Attack", name="Claw", n=1, d=6, mod=1, mult=2),
        act("Ability", name="Wounded Fury", dpr=False,
            text="While it has 10 HP or fewer, it has Favor on Attacks and deals an extra 7 (2d6) damage with melee Attacks."),
    ],
)
creatures.append(quaggoth)

# ---------------------------------------------------------------
# 44. Barbed Devil
# ---------------------------------------------------------------
barbed_devil = creature(
    name="Barbed Devil",
    size="Medium", type_="Outer", sub="Hellspawn",
    flav="A devil bristling with iron-hard spines, sent up from the Nine Hells whenever Xardorok's ambitions need a longer reach.",
    hd=9, armType="Scale", armEnh=0, shield=False,
    weak=["Silvered Weapons"], imm=["Fire", "Poison", "Physical from non-Relics"], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw and 1x Tail"),
        act("Melee Attack", name="Claw", n=1, d=6, mod=1, mult=2),
        act("Melee Attack", name="Tail", n=2, d=6, mod=1, mult=1),
        act("Cast", name="Hurl Flame", tags="Remote", dpr=False, n=3, d=6, mod=0),
        act("Ability", name="Barbed Hide", dpr=False,
            text="At the start of its Turn, any Being Grappling it takes 3 (d10) damage."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
    ],
)
creatures.append(barbed_devil)

# ---------------------------------------------------------------
# 45. Shield Guardian
# ---------------------------------------------------------------
shield_guardian = creature(
    name="Shield Guardian",
    size="Large", type_="Artificial", sub="",
    flav="A hulking construct bound to a wearer's amulet, absorbing half of what would otherwise kill them - and hitting back twice as hard.",
    hd=18, armType="Scale", armEnh=1, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed", "Confused", "Frightened", "Paralyzed"],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight", "Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Fist"),
        act("Melee Attack", name="Fist", n=2, d=6, mod=3, mult=2),
        act("Ability", name="Regeneration", dpr=False,
            text="Regains 10 HP on each of its Turns if it has at least 1 HP."),
        act("Ability", name="Bound", dpr=False,
            text="While within Close of its amulet's wearer, half of any damage the wearer takes (rounded up) is transferred to the guardian instead."),
    ],
)
creatures.append(shield_guardian)

# ---------------------------------------------------------------
# 46. Spectator
# ---------------------------------------------------------------
spectator = creature(
    name="Spectator",
    size="Medium", type_="Outer", sub="Beyonder",
    flav="A small, floating eye-beast summoned to guard a place and never told when to stop.",
    hd=6, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=["Prone"],
    speed=0, spds={"Fly": 30}, zone="Backline", morale="", app="1", senses=["Darksight", "Allsight"],
    oversize=0,
    acts=[
        act("Ranged Attack", name="Eye Rays", tags="Far", save="Will", dpr=True, n=1, d=8, mod=0, mult=2,
            text="Choose per ray: Confused, Paralyzed, Frightened, or 14 (4d6) damage, each (1 Minute) if failed."),
        act("Melee Attack", name="Bite", n=1, d=6, mod=0, dpr=False),
        act("Ability", name="Spell Reflection", dpr=False,
            text="Reaction. If it passes a Save against a Spell, or a Spell Attack misses it, it can redirect the Spell to another Being it senses within Near instead."),
    ],
)
creatures.append(spectator)

# ---------------------------------------------------------------
# 47. Slaad Tadpole
# ---------------------------------------------------------------
slaad_tadpole = creature(
    name="Slaad Tadpole",
    size="Small", type_="Outer", sub="",
    flav="A wriggling seed of chaos, implanted in some unlucky Being and counting down to a very bad day.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=0),
    ],
)
creatures.append(slaad_tadpole)

# ---------------------------------------------------------------
# 48. Gnoll
# ---------------------------------------------------------------
gnoll = creature(
    name="Gnoll",
    size="Medium", type_="Cryptid", sub="",
    flav="A hyena-headed raider driven by a demon's hunger, following whoever promises the next meal.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=6, app="d6", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Spear", n=1, d=4, mod=0),
        act("Ability", name="Rampage", dpr=False,
            text="When it reduces a Being to 0 HP with a melee Attack on its Turn, it can Move up to half its Speed and make a Bite Attack, as a Reaction."),
    ],
)
creatures.append(gnoll)

# ---------------------------------------------------------------
# 49. Ice Mephit
# ---------------------------------------------------------------
ice_mephit = creature(
    name="Ice Mephit",
    size="Small", type_="Primordial", sub="",
    flav="A cackling shard of animated ice, more nuisance than threat until it pops.",
    hd=4, armType="Unarmored", armEnh=0, shield=False,
    weak=["Blunt", "Fire"], imm=["Cold", "Poison"], statusImm=[],
    speed=30, spds={"Fly": 30}, zone="Frontline", morale=6, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Claws", n=1, d=4, mod=1, text="Cold damage."),
        act("Cast", name="Frost Breath", tags="Close Cone", save="Reflex", recharge="Cd6", dpr=False,
            n=2, d=4, mod=0, text="Cold damage."),
        act("Ability", name="Death Burst", dpr=False,
            text="When it dies, Beings within Close must pass [Reflex] or take 4 (d8) damage, half on a pass."),
    ],
)
creatures.append(ice_mephit)

# ---------------------------------------------------------------
# 50. Merrow
# ---------------------------------------------------------------
merrow = creature(
    name="Merrow",
    size="Large", type_="Cryptid", sub="",
    flav="An ogre-kin of the deep water, harpoon in hand and a taste for anything that swims too close.",
    hd=3, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=10, spds={"Swim": 40}, zone="Frontline", morale="", app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Bite and 1x Harpoon"),
        act("Melee Attack", name="Bite", n=1, d=8, mod=1),
        act("Melee Attack", name="Harpoon", tags="Thrown", n=1, d=6, mod=1,
            text="Target of Huge or smaller is pulled 20' toward it if it fails an [Might] Save."),
    ],
)
creatures.append(merrow)

# ---------------------------------------------------------------
# 51. Duergar
# ---------------------------------------------------------------
duergar = creature(
    name="Duergar",
    size="Medium", type_="Humanlike", sub="",
    flav="A grim, gray-skinned dwarf of Xardorok's rank and file, unhappy to be here and twice as unhappy to see you.",
    hd=2, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Charmed", "Confused"],
    speed=25, spds={}, zone="Frontline", morale=7, app="d4", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="War Pick", n=1, d=8, mod=0),
        act("Ability", name="Enlarge", recharge="Cd6", dpr=False,
            text="For the duration, it is Large, and its War Pick dice explode."),
        act("Ability", name="Vanish", recharge="Cd6", dpr=False,
            text="It is Invisible for up to 1 Hour, until it Attacks, Casts, or its Focus breaks."),
    ],
)
creatures.append(duergar)

# ---------------------------------------------------------------
# 52. Reghed Warrior
# ---------------------------------------------------------------
reghed_warrior = creature(
    name="Reghed Warrior",
    size="Medium", type_="Humanlike", sub="",
    flav="A tundra tribesfolk armed with a spear and a lifetime of practice not freezing to death.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=6, app="d8", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Spear", tags="Thrown", n=1, d=4, mod=0),
        act("Ability", name="Pack Tactics", dpr=False,
            text="It has Favor on Attacks against a Target that has one of its Allies within Close."),
    ],
)
creatures.append(reghed_warrior)

# ---------------------------------------------------------------
# 53. Reghed Shaman
# ---------------------------------------------------------------
reghed_shaman = creature(
    name="Reghed Shaman",
    size="Medium", type_="Humanlike", sub="",
    flav="A tribal healer and weather-reader who calls on old spirits when spears aren't enough.",
    hd=5, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Backline", morale=6, app="1", senses=[],
    oversize=0,
    acts=[
        act("Cast", name="Produce Flame", tags="Remote", n=2, d=8, mod=1),
        act("Cast", name="Entangle", tags="Near Cube", save="Might", dpr=False,
            n=0, d=0, mod=0, text="Targets are Restrained for the duration."),
        act("Ability", name="Barkskin", uses="1", per="Day", dpr=False,
            text="Grants itself or an Ally it touches +2 Armor for the duration."),
    ],
)
creatures.append(reghed_shaman)

# ---------------------------------------------------------------
# 54. Reghed Chieftain (mechanically identical to Hengar Aesnvaard)
# ---------------------------------------------------------------
reghed_chieftain = creature(
    name="Reghed Chieftain",
    size="Medium", type_="Humanlike", sub="",
    flav="A tribal leader who earned the spear-right the old way, and defends it the same.",
    hd=8, armType="Chain", armEnh=0, shield=True,
    weak=[], imm=[], statusImm=["Frightened"],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 3x Spear"),
        act("Melee Attack", name="Spear", n=1, d=8, mod=1, mult=3),
        act("Melee Attack", name="Shield Bash", n=1, d=4, mod=4, dpr=False,
            text="Target of Medium or smaller must pass [Might] or be knocked Prone."),
        act("Action", name="Parry", recharge="Cd4", dpr=False,
            text="Reaction. Gains +3 Armor against one melee Attack that would hit it, if it can see the Attacker and is wielding a melee weapon."),
    ],
)
creatures.append(reghed_chieftain)

# ---------------------------------------------------------------
# 55. Reghed Great Warrior (mechanically identical to Hengar Aesnvaard)
# ---------------------------------------------------------------
reghed_great_warrior = creature(
    name="Reghed Great Warrior",
    size="Medium", type_="Humanlike", sub="",
    flav="A tribe's finest fighter, kept close to its leader's side for exactly the reasons you'd expect.",
    hd=8, armType="Chain", armEnh=0, shield=True,
    weak=[], imm=[], statusImm=["Frightened"],
    speed=30, spds={}, zone="Frontline", morale="", app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 3x Spear"),
        act("Melee Attack", name="Spear", n=1, d=8, mod=1, mult=3),
        act("Melee Attack", name="Shield Bash", n=1, d=4, mod=4, dpr=False,
            text="Target of Medium or smaller must pass [Might] or be knocked Prone."),
        act("Action", name="Parry", recharge="Cd4", dpr=False,
            text="Reaction. Gains +3 Armor against one melee Attack that would hit it, if it can see the Attacker and is wielding a melee weapon."),
    ],
)
creatures.append(reghed_great_warrior)

# ---------------------------------------------------------------
# 56. Aarakocra
# ---------------------------------------------------------------
aarakocra = creature(
    name="Aarakocra",
    size="Medium", type_="Cryptid", sub="",
    flav="A bird-folk scout of the high peaks, javelin in talon, most dangerous in a dive.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Fly": 50}, zone="Frontline", morale=6, app="d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Talon", n=1, d=4, mod=0),
        act("Ranged Attack", name="Javelin", n=1, d=6, mod=1, dpr=False),
        act("Ability", name="Dive Attack", dpr=False,
            text="If it Flies at least 30' straight toward a Target before hitting it with a melee Attack, that Attack deals an extra damage die."),
    ],
)
creatures.append(aarakocra)

# ---------------------------------------------------------------
# Report + write bundle
# ---------------------------------------------------------------
for c in creatures:
    r = calc_tl(c)
    print(f"{c['name']:42s} TL={r['tl']:<6} armor={c['armor']:<2} hp={c['hp']:<4} dpr={r['dpr']:.2f}")

bundle = {
    "format": "vagabond-bestiary",
    "version": 1,
    "exported": datetime.datetime.utcnow().isoformat() + "Z",
    "count": len(creatures),
    "creatures": creatures,
}

out_path = r"D:\claude projects\Icewind Dale Vagabond\creatures\bestiary.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(bundle, f, indent=2)
print("\nWrote", out_path)
