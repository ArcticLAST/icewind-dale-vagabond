# -*- coding: utf-8 -*-
"""
Batch 6 - "full adventure audit" pass.

Everything here was identified by cross-referencing the complete IDRotF creature
roster (notes/creature-audit-full-crossref.md) against what already existed.
Creatures that had a genuine equivalent in the core `vagabond.bestiary` /
`vagabond.humanlike` compendiums are NOT here - those are copied straight across
in Foundry instead (see notes). This file holds only the ones that needed a real
hand conversion.

Same conventions as build_bestiary.py:
  - only steady / at-will attacks carry dpr=True; recharge & limited bursts don't
  - Combo is its own action; the member attacks carry mult=
  - Vagabond has no burrow speed, so burrowers note it in flavour/abilities
  - TL is validated against the Creature Forge formula, and sanity-checked
    against both the source CR and the closest core-compendium peer
"""
from build_bestiary import act, creature

creatures2 = []


def add(c):
    creatures2.append(c)
    return c


# =====================================================================
# A. COMMON RECURRING NPCs  (the Ten-Towns backbone)
# =====================================================================

add(creature(
    name="Tribal Warrior",
    size="Medium", type_="Humanlike", sub="",
    flav="A Reghed or Ten-Towns hunter who fights the way the tundra taught them: in a pack, and without ceremony.",
    hd=1, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=7, app="2d6", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Spear", tags="", n=1, d=6, mod=1),
        act("Ability", name="Pack Tactics", dpr=False,
            text="It has Favor on Attacks against a Being that has another of its allies adjacent to it."),
    ],
))

add(creature(
    name="Priest",
    size="Medium", type_="Humanlike", sub="",
    flav="A servant of Amaunator, Lathander, or whichever god still answers this far north. Ten-Towns keeps them busy.",
    hd=2, armType="Chain", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=25, spds={}, zone="Backline", morale=7, app="1d3", senses=[],
    oversize=0,
    acts=[
        act("Cast", name="Sacred Flame", tags="Remote", save="Reflex", n=2, d=6, mod=0),
        act("Melee Attack", name="Mace", n=1, d=6, mod=0, dpr=False),
        act("Cast", name="Cure Wounds", tags="Touch", n=2, d=6, mod=1, dpr=False,
            text="Restores the listed amount of HP to a Being it touches."),
        act("Ability", name="Divine Eminence", uses="2", per="Day", dpr=False,
            text="Its next melee Attack this Turn deals an extra 10 (3d6) damage."),
    ],
))

add(creature(
    name="Cult Fanatic",
    size="Medium", type_="Humanlike", sub="",
    flav="A true believer of Levistus, drunk on the promise that the Frostmaiden's night will spare the faithful.",
    hd=2, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=9, app="1d4", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Dagger"),
        act("Melee Attack", name="Dagger", n=1, d=4, mod=2, mult=2),
        act("Cast", name="Command", tags="Remote", save="Will", dpr=False,
            text="The target must obey a one-word command on its next Turn, so long as the order isn't directly self-destructive."),
        act("Ability", name="Dark Devotion", dpr=False,
            text="It has Favor on Saves against being Charmed or Frightened."),
    ],
))

add(creature(
    name="Druid",
    size="Medium", type_="Humanlike", sub="",
    flav="A keeper of the old green places, which in Icewind Dale means the few that are left.",
    hd=2, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=7, app="1d2", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Quarterstaff", n=1, d=8, mod=2),
        act("Cast", name="Entangle", tags="Near Sphere", save="Might", dpr=False,
            text="Targets are Restrained while the growth holds. A target can free itself by passing [Might] on its Turn."),
        act("Ability", name="Change Shape", dpr=False,
            text="It transforms into a beast of its size or smaller, and back. Its statistics are unchanged."),
    ],
))

add(creature(
    name="Bandit Captain",
    size="Medium", type_="Humanlike", sub="",
    flav="Whoever is holding the most knives when the last captain stopped breathing.",
    hd=2, armType="Leather", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=8, app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Scimitar"),
        act("Melee Attack", name="Scimitar", n=1, d=6, mod=1, mult=2),
        act("Ranged Attack", name="Dagger", n=1, d=4, mod=1, dpr=False),
        act("Action", name="Parry", dpr=False,
            text="Reaction. It adds 2 to its Armor against one melee Attack that would hit it. It must see the attacker and be wielding a weapon."),
    ],
))

add(creature(
    name="Frost Druid",
    size="Medium", type_="Humanlike", sub="",
    flav="A convert to Auril's winter, who has stopped asking the land for anything and started asking the cold instead.",
    hd=9, armType="Hide", armEnh=0, shield=False,
    weak=["Fire"], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=9, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Ice Sickle"),
        act("Melee Attack", name="Ice Sickle", n=2, d=6, mod=2, mult=2),
        act("Ability", name="Change Shape", dpr=False,
            text="It transforms into a fox, mountain goat, owl, or wolf, and back. Its statistics are unchanged, but it gains that beast's movement."),
        act("Ability", name="Cold Blooded", dpr=False,
            text="It ignores the effects of extreme cold and treats icy ground as normal footing."),
    ],
))

add(creature(
    name="Drow Elite Warrior",
    size="Medium", type_="Humanlike", sub="",
    flav="A blade of the Underdark, escorting an archmage's business up through the Caves of Hunger and deeply unhappy about the daylight.",
    hd=6, armType="Leather", armEnh=1, shield=True,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=9, app="1d4", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Shortsword"),
        act("Melee Attack", name="Shortsword", n=2, d=6, mod=2, mult=2),
        act("Ranged Attack", name="Hand Crossbow", n=1, d=6, mod=2, dpr=False,
            text="Target must pass [Endure] or be Unconscious (Cd6). The effect ends early if the target takes damage."),
        act("Ability", name="Sunlight Sensitivity", dpr=False,
            text="While in sunlight, it has Hinder on Attacks and on sight-based Checks."),
    ],
))

add(creature(
    name="Drow Mage",
    size="Medium", type_="Humanlike", sub="",
    flav="Patient, poisonous, and entirely certain that everyone in the room is a resource that hasn't been spent yet.",
    hd=10, armType="Leather", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Backline", morale=8, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Cast", name="Lightning Bolt", tags="Far Line", save="Reflex", n=4, d=6, mod=0),
        act("Cast", name="Darkfire Bolt", tags="Remote", n=3, d=6, mod=0),
        act("Melee Attack", name="Poison Staff", n=1, d=6, mod=0),
        act("Cast", name="Cloudkill", tags="Far Sphere", save="Endure", uses="1", per="Day", dpr=False,
            n=5, d=8, mod=0,
            text="The cloud lingers and moves away from the caster each Round. Beings inside it are Sickened."),
        act("Ability", name="Summon Demon", uses="1", per="Day", dpr=False,
            text="It calls a Shadow Demon to an empty space it can see. The demon acts as its ally and departs after 10 minutes."),
        act("Ability", name="Sunlight Sensitivity", dpr=False,
            text="While in sunlight, it has Hinder on Attacks and on sight-based Checks."),
    ],
))

add(creature(
    name="Battlehammer Dwarf",
    size="Medium", type_="Humanlike", sub="",
    flav="Clan Battlehammer out of Kelvin's Cairn - short, armoured, and utterly unbothered by the walk.",
    hd=2, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=25, spds={}, zone="Frontline", morale=9, app="1d6", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Handaxe", n=1, d=6, mod=1),
        act("Ranged Attack", name="Light Crossbow", n=1, d=8, mod=1, dpr=False),
        act("Ability", name="Dwarven Resilience", dpr=False,
            text="It has Favor on Saves against Poison, and resists the effects of extreme cold."),
    ],
))

add(creature(
    name="Half-Ogre",
    size="Large", type_="Cryptid", sub="Giantkin",
    flav="An ogrillon: too clever to be an ogre, too large to be welcome anywhere else.",
    hd=4, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=8, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Battleaxe", n=1, d=8, mod=2),
        act("Ranged Attack", name="Javelin", n=2, d=6, mod=3, dpr=False),
    ],
))

add(creature(
    name="Goblin Boss",
    size="Medium", type_="Cryptid", sub="Goblinoid",
    flav="Izobai, or whoever knifed Izobai. Karkolohk's chain of command is short and frequently revised.",
    hd=2, armType="Chain", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=8, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Scimitar"),
        act("Melee Attack", name="Scimitar", n=1, d=6, mod=1, mult=2),
        act("Action", name="Redirect Attack", dpr=False,
            text="Reaction. When a Being it can see hits it with an Attack, it swaps places with an adjacent goblin ally, who is hit instead."),
        act("Ability", name="Nimble Escape", dpr=False,
            text="It can Disengage or Hide as a free action on its Turn."),
    ],
))

add(creature(
    name="Orc War Chief",
    size="Medium", type_="Cryptid", sub="Orcish",
    flav="Gruumsh's fury given a greataxe and a grudge. It leads from the very front, loudly.",
    hd=6, armType="Chain", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=10, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Greataxe"),
        act("Melee Attack", name="Greataxe", n=1, d=12, mod=2, mult=2),
        act("Ability", name="Gruumsh's Fury", dpr=False,
            text="Its weapon Attacks deal an extra 4 (1d8) damage. This is already included above."),
        act("Action", name="Battle Cry", uses="1", per="Day", dpr=False,
            text="Allies of its choice within Near that can hear it gain Favor on Attacks until the start of its next Turn. It may then Attack once as a free action."),
    ],
))

add(creature(
    name="Orc Eye of Gruumsh",
    size="Medium", type_="Cryptid", sub="Orcish",
    flav="An orc who put out one of their own eyes for their god, and has been rewarded for it.",
    hd=3, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=10, app="1d2", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Spear", n=1, d=8, mod=3),
        act("Cast", name="Bless", tags="Near", dpr=False, focus=True,
            text="Allies within the area add 1d4 to their Attacks and Saves while the Focus holds."),
        act("Ability", name="Gruumsh's Fury", dpr=False,
            text="Its weapon Attacks deal an extra 4 (1d8) damage. This is already included above."),
    ],
))

add(creature(
    name="Quaggoth Thonot",
    size="Medium", type_="Cryptid", sub="",
    flav="A quaggoth shaman whose grief curdled into something psionic. Krob is one of these, and he is not well.",
    hd=6, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Sickened"],
    speed=30, spds={"Climb": 30}, zone="Frontline", morale=10, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw"),
        act("Melee Attack", name="Claw", n=1, d=6, mod=3, mult=2),
        act("Cast", name="Mind Blast", tags="Near Cone", save="Will", recharge="Cd6", dpr=False,
            n=3, d=6, mod=0,
            text="Targets that fail are Dazed (Cd4)."),
        act("Ability", name="Wounded Fury", dpr=False,
            text="While at 10 HP or fewer, it has Favor on Attacks and its melee Attacks deal an extra 7 (2d6) damage."),
    ],
))

add(creature(
    name="Sephek Kaltro",
    size="Medium", type_="Undead", sub="",
    flav="Auril's chosen killer, walking the caravan roads to collect the toll she says the living owe her. Torrga Icevein thinks he works for her.",
    hd=6, armType="Leather", armEnh=0, shield=False,
    weak=["Fire"], imm=["Cold"], statusImm=["Charmed", "Frightened"],
    speed=30, spds={}, zone="Frontline", morale=12, app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Ice Longsword"),
        act("Melee Attack", name="Ice Longsword", n=1, d=8, mod=2, mult=2),
        act("Ranged Attack", name="Ice Dagger", n=1, d=4, mod=3, dpr=False),
        act("Ability", name="Cold Regeneration", dpr=False,
            text="While the surrounding air is freezing, he regains 5 HP at the start of his Turn. Fire damage suppresses this until the end of his next Turn."),
    ],
))

add(creature(
    name="Spellix Romwod",
    size="Medium", type_="Humanlike", sub="",
    flav="A gnome wizard who took shelter in the wrong pass and has been entombed in the ice ever since, still mid-argument with himself.",
    hd=3, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=25, spds={}, zone="Backline", morale=6, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Cast", name="Fire Bolt", tags="Remote", n=1, d=10, mod=0),
        act("Cast", name="Shocking Grasp", tags="Touch", n=1, d=8, mod=0, dpr=False,
            text="The target can't take Reactions until the start of its next Turn."),
        act("Ability", name="Gnome Cunning", dpr=False,
            text="It has Favor on Saves against Spells."),
    ],
))


# =====================================================================
# B. UNDEAD
# =====================================================================

add(creature(
    name="Specter",
    size="Medium", type_="Undead", sub="",
    flav="What's left when a soul is denied rest and given nothing to hold onto - not even a body.",
    hd=5, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=["Necrotic", "Poison"], statusImm=["Charmed", "Fatigued", "Grappling", "Paralyzed", "Prone", "Restrained", "Unconscious"],
    speed=0, spds={"Fly": 50}, zone="Frontline", morale=12, app="1d4", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Life Drain", n=2, d=6, mod=0,
            text="The target's maximum HP is reduced by the damage dealt until it Rests."),
        act("Ability", name="Incorporeal", dpr=False,
            text="It moves through Beings and solid objects as if they were difficult terrain, and takes 5 (1d10) damage if it ends its Turn inside one."),
        act("Ability", name="Sunlight Sensitivity", dpr=False,
            text="While in sunlight, it has Hinder on Attacks and on sight-based Checks."),
    ],
))

add(creature(
    name="Poltergeist",
    size="Medium", type_="Undead", sub="",
    flav="An invisible spite that expresses itself entirely through other people's furniture.",
    hd=5, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=["Necrotic", "Poison"], statusImm=["Charmed", "Fatigued", "Grappling", "Paralyzed", "Prone", "Restrained", "Unconscious"],
    speed=0, spds={"Fly": 50}, zone="Midline", morale=11, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Forceful Slam", n=3, d=6, mod=0),
        act("Cast", name="Telekinetic Thrust", tags="Near", save="Might", dpr=False,
            n=2, d=6, mod=0,
            text="It hurls a Being or loose object up to 30'. A thrown Being lands Prone and takes the listed damage."),
        act("Ability", name="Invisible", dpr=False, text="It is permanently Invisible."),
        act("Ability", name="Incorporeal", dpr=False,
            text="It moves through Beings and solid objects as if they were difficult terrain, and takes 5 (1d10) damage if it ends its Turn inside one."),
    ],
))

add(creature(
    name="Ogre Zombie",
    size="Large", type_="Undead", sub="",
    flav="An ogre that died, and then kept the appointment anyway.",
    hd=8, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=["Poison"], statusImm=["Sickened"],
    speed=30, spds={}, zone="Frontline", morale=12, app="1d2", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Morningstar", n=2, d=8, mod=2),
        act("Ability", name="Undead Fortitude", dpr=False,
            text="When damage would drop it to 0 HP, it passes [Endure] to drop to 1 HP instead. Fire damage and Critical Hits bypass this."),
    ],
))

add(creature(
    name="Icewind Kobold Zombie",
    size="Medium", type_="Undead", sub="",
    flav="A Termalaine kobold that Xardorok's crystal got to first. It still wears its scraps of hide.",
    hd=2, armType="Hide", armEnh=-1, shield=False,
    weak=[], imm=["Poison"], statusImm=["Sickened"],
    speed=20, spds={}, zone="Frontline", morale=12, app="2d6", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Javelin", n=1, d=6, mod=-1),
        act("Ability", name="Undead Fortitude", dpr=False,
            text="When damage would drop it to 0 HP, it passes [Endure] to drop to 1 HP instead. Fire damage and Critical Hits bypass this."),
    ],
))

add(creature(
    name="Flameskull",
    # Medium for the same reason as the Demilich: Vagabond's "Small" tier derives only
    # 1 HP per HD, which would leave a CR 4 guardian on 9 HP. Medium gives it the 40 HP
    # its source stat block actually has.
    size="Medium", type_="Undead", sub="",
    flav="A wizard's skull kept burning as a watchdog. It remembers just enough to be dangerous and nothing at all to be reasoned with.",
    hd=9, armType="Unarmored", armEnh=2, shield=False,
    weak=[], imm=["Cold", "Fire", "Poison"], statusImm=["Charmed", "Frightened", "Paralyzed", "Prone", "Sickened"],
    speed=0, spds={"Fly": 40}, zone="Backline", morale=12, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Fire Ray"),
        act("Cast", name="Fire Ray", tags="Remote", n=2, d=6, mod=0, mult=2),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Rejuvenation", dpr=False,
            text="If destroyed, it reforms with all its HP in 1 hour unless holy water is poured on its remains or the magic on them is dispelled."),
        act("Ability", name="Illumination", dpr=False,
            text="It sheds bright light in a Near radius, and can dim this to a faint glow as a free action."),
    ],
))

add(creature(
    name="Brain in a Jar",
    size="Medium", type_="Undead", sub="",
    flav="Veneranda, once a Netherese wizard of Ythryn, now a preserved brain that has had far too long to think about it.",
    hd=8, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=["Poison"], statusImm=["Fatigued", "Paralyzed", "Prone", "Sickened"],
    speed=0, spds={"Fly": 10}, zone="Backline", morale=9, app="1", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Cast", name="Chill Touch", tags="Remote", n=3, d=8, mod=0,
            text="The target can't regain HP until the start of the brain's next Turn."),
        act("Cast", name="Mind Blast", tags="Far Cone", save="Will", recharge="Cd6", dpr=False,
            n=3, d=8, mod=4,
            text="Targets that fail are Dazed (Cd6)."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Detect Sentience", dpr=False,
            text="It senses the presence and location of any thinking Being within 300', through walls."),
    ],
))

add(creature(
    name="Demilich",
    # NB: a demilich is a floating skull, but Vagabond's "Small" tier is reserved for
    # rat/cat-scale creatures and derives only 1 HP per HD - which would leave the
    # campaign's final boss on 36 HP. Kept Medium so the HD->HP derivation is sane.
    size="Medium", type_="Undead", sub="",
    flav="Iriolarthas, Arch-Astronomer of Ythryn - a lich so old that only the skull kept up. The gems in its teeth are the souls it hasn't finished.",
    hd=18, armType="Plate", armEnh=4, shield=False,
    weak=[], imm=["Necrotic", "Poison", "Psychic", "Physical from non-Relics"],
    statusImm=["Charmed", "Fatigued", "Frightened", "Paralyzed", "Prone", "Sickened"],
    speed=0, spds={"Fly": 30}, zone="Backline", morale=12, app="1", senses=["Blindsight"],
    oversize=0, boss=True,
    acts=[
        act("Cast", name="Life Drain", tags="Near", save="Endure", n=6, d=6, mod=0, mult=2,
            text="Up to three Beings it can see are targeted. It regains HP equal to the total damage dealt."),
        act("Cast", name="Howl", tags="Near Aura", save="Endure", recharge="Cd6", dpr=False,
            n=0, d=0, mod=0,
            text="Every Being that hears it must pass [Endure] or drop to 0 HP. On a pass, the Being is Frightened until the end of its next Turn."),
        act("Cast", name="Vile Curse", tags="Near", save="Will", uses="1", per="Day", dpr=False,
            n=0, d=0, mod=0,
            text="The target has Hinder on Attacks and Saves, and the demilich has Favor on Attacks against it, until the curse is lifted."),
        act("Ability", name="Magic Ward IV", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 4 Mana to affect it."),
        act("Ability", name="Avoidance", dpr=False,
            text="When it passes a Save against an effect, it takes no damage from that effect at all."),
        act("Ability", name="Soul Gems", dpr=False,
            text="It cannot be permanently destroyed while any of its soul gems remain intact."),
    ],
))


# =====================================================================
# C. FIENDS, ABERRATIONS & OTHER OUTERS
# =====================================================================

add(creature(
    name="Bearded Devil",
    size="Medium", type_="Outer", sub="Hellspawn",
    flav="A barbazu, all glaive and writhing beard, sent up by Levistus to check on the investment.",
    hd=6, armType="Scale", armEnh=0, shield=False,
    weak=["Silvered Weapons"], imm=["Fire", "Poison"], statusImm=["Sickened", "Frightened"],
    speed=30, spds={}, zone="Frontline", morale=10, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Beard and 1x Glaive"),
        act("Melee Attack", name="Beard", n=1, d=8, mod=2, mult=1,
            text="Target must pass [Endure] or be unable to regain HP (Cd6)."),
        act("Melee Attack", name="Glaive", tags="10' reach", n=1, d=10, mod=1, mult=1,
            text="Target must pass [Endure] or take 5 (1d10) damage at the start of each of its Turns from an infernal wound until healed."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Steadfast", dpr=False,
            text="It can't be Frightened while it can see an ally within Near."),
    ],
))

add(creature(
    name="Shadow Demon",
    size="Medium", type_="Outer", sub="Demonic",
    flav="A demon that lost its body and found it didn't much need one.",
    hd=12, armType="Unarmored", armEnh=1, shield=False,
    weak=["Fire"], imm=["Cold", "Shock", "Poison"],
    statusImm=["Fatigued", "Grappling", "Paralyzed", "Prone", "Restrained", "Sickened"],
    speed=30, spds={"Fly": 30}, zone="Frontline", morale=10, app="1d2", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Claws", n=2, d=6, mod=3,
            text="If the demon had Favor on this Attack, it deals 17 (4d6+3) instead."),
        act("Ability", name="Incorporeal", dpr=False,
            text="It moves through Beings and solid objects as if they were difficult terrain, and takes 5 (1d10) damage if it ends its Turn inside one."),
        act("Ability", name="Shadow Stealth", dpr=False,
            text="In dim light or darkness it can Hide as a free action. In bright light it has Hinder on Attacks."),
    ],
))

add(creature(
    name="Night Hag",
    size="Medium", type_="Outer", sub="Hellspawn",
    flav="Auntie Pinch, Auntie Pillage, or Auntie Plunder. They are sisters, they are hospitable, and you should not eat anything they offer.",
    hd=10, armType="Scale", armEnh=0, shield=False,
    weak=["Silvered Weapons"], imm=[], statusImm=["Charmed"],
    speed=30, spds={}, zone="Midline", morale=10, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claws"),
        act("Melee Attack", name="Claws", n=2, d=8, mod=2, mult=2),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Change Shape", dpr=False,
            text="It takes the form of any Small or Medium humanlike woman, and back. Its statistics are unchanged."),
        act("Action", name="Etherealness", dpr=False,
            text="While holding its heartstone, it steps into or out of the Ethereal Plane."),
        act("Action", name="Nightmare Haunting", uses="1", per="Day", dpr=False,
            text="While Ethereal, it touches a sleeping Being. If the contact lasts an hour, the target gains no benefit from the Rest and its maximum HP drops by 5 (1d10) until the haunting ends."),
    ],
))

add(creature(
    name="Arcanaloth",
    size="Medium", type_="Outer", sub="Hellspawn",
    flav="Scrivenscry, a jackal-headed broker of contracts and secrets, who has read everything in Ythryn twice and is bored.",
    hd=16, armType="Plate", armEnh=2, shield=False,
    weak=[], imm=["Acid", "Poison"], statusImm=["Charmed", "Sickened"],
    speed=30, spds={"Fly": 30}, zone="Midline", morale=10, app="1", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claws"),
        act("Melee Attack", name="Claws", n=2, d=4, mod=3, mult=2,
            text="Target must pass [Endure] or take a further 10 (3d6) Poison damage."),
        act("Cast", name="Chain Lightning", tags="Far", save="Reflex", n=6, d=6, mod=0,
            text="Arcs to up to three additional Beings within Near of the first target."),
        act("Cast", name="Fire Bolt", tags="Remote", n=4, d=6, mod=0),
        act("Ability", name="Magic Ward IV", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 4 Mana to affect it."),
        act("Action", name="Teleport", dpr=False,
            text="It vanishes and reappears in an empty space it can see within Far."),
    ],
))

add(creature(
    name="Red Slaad",
    size="Large", type_="Outer", sub="Chaos",
    flav="A frog-thing out of Limbo, whose claws plant eggs in people. The Id Ascendant did not crash empty.",
    hd=11, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=10, app="1d2", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Bite and 2x Claw"),
        act("Melee Attack", name="Bite", n=2, d=4, mod=2, mult=1),
        act("Melee Attack", name="Claw", n=1, d=6, mod=2, mult=2,
            text="A humanlike target must pass [Endure] or be implanted with a slaad egg."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Regeneration", dpr=False,
            text="It regains 10 HP at the start of its Turn so long as it has at least 1 HP."),
    ],
))

add(creature(
    name="Blue Slaad",
    size="Large", type_="Outer", sub="Chaos",
    flav="Bone claws, and a disease called chaos phage that turns the victim into another one of these.",
    hd=13, armType="Scale", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=10, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Bite and 2x Claw"),
        act("Melee Attack", name="Bite", n=2, d=6, mod=3, mult=1),
        act("Melee Attack", name="Claw", n=2, d=6, mod=2, mult=2,
            text="A humanlike target must pass [Endure] or contract chaos phage."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Regeneration", dpr=False,
            text="It regains 10 HP at the start of its Turn so long as it has at least 1 HP."),
    ],
))

add(creature(
    name="Green Slaad",
    size="Large", type_="Outer", sub="Chaos",
    flav="A slaad that learned to wear a person. It is working very hard on becoming a grey one.",
    hd=15, armType="Scale", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=10, app="1", senses=["Blindsight", "Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Bite and 2x Claw"),
        act("Melee Attack", name="Bite", n=2, d=6, mod=4, mult=1),
        act("Melee Attack", name="Claw", n=1, d=6, mod=4, mult=2),
        act("Cast", name="Hurl Flame", tags="Remote", n=3, d=6, mod=0, dpr=False),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Shapechanger", dpr=False,
            text="It takes the form of any Small or Medium humanlike, and back. Only its size changes."),
        act("Ability", name="Regeneration", dpr=False,
            text="It regains 10 HP at the start of its Turn so long as it has at least 1 HP."),
    ],
))

add(creature(
    name="Nothic",
    size="Medium", type_="Outer", sub="",
    flav="A wizard who looked too long at something they shouldn't have, and got one enormous eye out of the bargain.",
    hd=4, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=8, app="1d2", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw"),
        act("Melee Attack", name="Claw", n=1, d=6, mod=2, mult=2),
        act("Cast", name="Rotting Gaze", tags="Near", save="Endure", n=3, d=6, mod=0, dpr=False),
        act("Ability", name="Weird Insight", dpr=False,
            text="It can magically wrest one secret from a Being it can see within Near, unless that Being resists with [Will]."),
    ],
))

add(creature(
    name="Grell",
    size="Medium", type_="Outer", sub="",
    flav="A floating brain with a beak and ten paralysing tentacles. Termalaine's mine has one, and the miners have stopped going deep.",
    hd=8, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=["Shock"], statusImm=["Blinded", "Prone"],
    speed=10, spds={"Fly": 30}, zone="Frontline", morale=8, app="1d2", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Tentacles and 1x Beak"),
        act("Melee Attack", name="Tentacles", tags="10' reach", n=1, d=10, mod=2, mult=1,
            text="Target must pass [Endure] or be Paralyzed (Cd6). It is also Grappling."),
        act("Melee Attack", name="Beak", n=2, d=4, mod=1, mult=1),
    ],
))

add(creature(
    name="Gnome Ceremorph",
    size="Medium", type_="Outer", sub="",
    flav="A svirfneblin whose head a mind flayer tadpole rewrote badly. Vorryn Q'uuol and Dredavex Sinfiz co-captain the Id Ascendant like this.",
    hd=13, armType="Plate", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=25, spds={}, zone="Midline", morale=9, app="1d2", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Tentacles", n=2, d=10, mod=4,
            text="A Medium or smaller target is Grappling, and must pass [Will] or be Dazed while the grapple holds."),
        act("Ranged Attack", name="Laser Pistol", n=3, d=6, mod=2, dpr=False),
        act("Cast", name="Mind Blast", tags="Far Cone", save="Will", recharge="Cd6", dpr=False,
            n=4, d=8, mod=4,
            text="Targets that fail are Dazed (Cd6)."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
    ],
))

add(creature(
    name="Gnome Squidling",
    size="Medium", type_="Outer", sub="",
    flav="A ceremorphosis that stalled halfway. Rin, Rix, and Zglarrd are pitiable, and still hungry.",
    hd=3, armType="Unarmored", armEnh=-1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=15, spds={}, zone="Frontline", morale=6, app="1d4", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Tentacles", n=2, d=4, mod=0,
            text="A Medium or smaller target is Grappling, and must pass [Will] or be Dazed while the grapple holds."),
        act("Cast", name="Mind Tickle", tags="Near Cone", save="Will", recharge="Cd6", dpr=False,
            n=1, d=4, mod=0,
            text="Targets that fail are Dazed until the end of their next Turn."),
    ],
))


# =====================================================================
# D. CRYPTIDS / MONSTROSITIES
# =====================================================================

add(creature(
    name="Remorhaz",
    size="Huge", type_="Cryptid", sub="",
    flav="The polar worm. It tunnels under the ice and comes up beneath you, and its back glows hot enough to cook whatever it swallows.",
    hd=17, armType="Plate", armEnh=1, shield=False,
    weak=[], imm=["Cold", "Fire"], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=11, app="1", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", tags="10' reach", n=6, d=10, mod=7,
            text="The target is Grappling and Restrained, and the remorhaz can't bite another target until the grapple ends."),
        act("Action", name="Swallow", dpr=False,
            text="It bites a Medium or smaller Being it is Grappling. On a hit, the target is swallowed, is Blinded and Restrained, and takes 21 (6d6) Acid damage at the start of each of the remorhaz's Turns."),
        act("Ability", name="Heated Body", dpr=False,
            text="A Being that touches it or hits it with a melee Attack takes 10 (3d6) Fire damage."),
        act("Ability", name="Ice Tunneler", dpr=False,
            text="It burrows through ice and packed snow at 20', leaving a tunnel behind it."),
    ],
))

add(creature(
    name="Young Remorhaz",
    size="Large", type_="Cryptid", sub="",
    flav="Only twenty feet of it so far. Give it time.",
    hd=11, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=["Cold", "Fire"], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=10, app="1d2", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=3, d=10, mod=4),
        act("Ability", name="Heated Body", dpr=False,
            text="A Being that touches it or hits it with a melee Attack takes 7 (2d6) Fire damage."),
        act("Ability", name="Ice Tunneler", dpr=False,
            text="It burrows through ice and packed snow at 30', leaving a tunnel behind it."),
    ],
))

add(creature(
    name="Phase Spider",
    size="Large", type_="Cryptid", sub="",
    flav="It is not in the room. It will be in the room, briefly, while it bites you.",
    hd=5, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={"Climb": 30}, zone="Midline", morale=8, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=10, mod=2,
            text="Target must pass [Endure] or take a further 18 (4d8) Poison damage and be Paralyzed (Cd6)."),
        act("Ability", name="Ethereal Jaunt", dpr=False,
            text="As a free action on its Turn it shifts to or from the Ethereal Plane."),
        act("Ability", name="Web Walker", dpr=False, text="Webbing never slows it."),
    ],
))

add(creature(
    name="Spitting Mimic",
    size="Large", type_="Cryptid", sub="",
    flav="A mimic that grew big enough to stop waiting. Ythryn is full of furniture that isn't.",
    hd=10, armType="Scale", armEnh=0, shield=False,
    weak=[], imm=["Acid"], statusImm=["Prone"],
    speed=20, spds={}, zone="Frontline", morale=9, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Pseudopod and 1x Bite"),
        act("Melee Attack", name="Pseudopod", tags="10' reach", n=1, d=10, mod=2, mult=2,
            text="In object form, the target also sticks fast and is Grappling."),
        act("Melee Attack", name="Bite", n=1, d=10, mod=2, mult=1),
        act("Cast", name="Spit Acid", tags="Near", save="Reflex", recharge="Cd6", dpr=False,
            n=9, d=6, mod=1),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="False Appearance", dpr=False,
            text="While it stays still in object form it is indistinguishable from ordinary furniture."),
    ],
))

add(creature(
    name="Gnoll Fang of Yeenoghu",
    size="Medium", type_="Outer", sub="Demonic",
    flav="Chyzka, and others like her - a gnoll that ate the right corpse and got promoted by a demon lord.",
    hd=8, armType="Hide", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Frontline", morale=11, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Bite and 2x Claw"),
        act("Melee Attack", name="Bite", n=1, d=6, mod=2, mult=1,
            text="Target must pass [Endure] or take a further 7 (2d6) Poison damage."),
        act("Melee Attack", name="Claw", n=1, d=8, mod=1, mult=2),
        act("Ability", name="Rampage", dpr=False,
            text="When it drops a Being to 0 HP with a melee Attack, it may immediately move up to half its Speed and Bite again."),
    ],
))

add(creature(
    name="Ice Piercer",
    size="Medium", type_="Cryptid", sub="",
    flav="An icicle with an appetite. You will not notice the difference until it is already falling.",
    hd=3, armType="Plate", armEnh=0, shield=False,
    weak=["Fire"], imm=["Cold"], statusImm=[],
    speed=5, spds={"Cling": 10}, zone="Frontline", morale=8, app="2d6", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Drop", n=3, d=6, mod=0,
            text="It falls on a Being directly beneath it, dealing an extra 10 (3d6) Cold damage. On a miss it takes half the falling damage itself."),
        act("Ability", name="False Appearance", dpr=False,
            text="While it hangs motionless it is indistinguishable from an ordinary icicle."),
    ],
))


# =====================================================================
# E. ARTIFICIALS  (the Ythryn constructs)
# =====================================================================

add(creature(
    name="Tomb Tapper",
    size="Huge", type_="Artificial", sub="",
    flav="A blind Netherese construct built to hunt magic and break it. It has been tapping through the ice under Ythryn for two thousand years.",
    hd=18, armType="Plate", armEnh=1, shield=False,
    weak=["Shock"], imm=["Cold", "Fire"], statusImm=["Charmed", "Frightened"],
    speed=30, spds={}, zone="Frontline", morale=12, app="1", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw"),
        act("Melee Attack", name="Claw", tags="10' reach", n=3, d=6, mod=6, mult=2,
            text="If both Claws hit the same Being, it is dragged adjacent to the tapper's mouth and Bitten."),
        act("Melee Attack", name="Bite", n=3, d=10, mod=6, dpr=False),
        act("Ranged Attack", name="Sledgehammer", n=6, d=6, mod=6, dpr=False,
            text="Thrown, it returns to the tomb tapper's feet at the end of its Turn."),
        act("Ability", name="Sense Magic", dpr=False,
            text="It senses magic within Near and can pinpoint any magical Being, object, or area in that range through solid rock."),
        act("Ability", name="Petrified Death", dpr=False,
            text="At 0 HP it becomes a lifeless stone statue. Anything it carried is left behind."),
    ],
))

add(creature(
    name="Helmed Horror",
    size="Medium", type_="Artificial", sub="",
    flav="Empty armour with a purpose bolted into it. It will guard the door until the door is gone.",
    hd=8, armType="Plate", armEnh=0, shield=False,
    weak=[], imm=["Necrotic", "Poison", "Physical from non-Relics"],
    statusImm=["Blinded", "Charmed", "Frightened", "Paralyzed", "Sickened"],
    speed=30, spds={"Fly": 30}, zone="Frontline", morale=12, app="1d3", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Longsword"),
        act("Melee Attack", name="Longsword", n=1, d=10, mod=2, mult=2),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Spell Immunity", dpr=False,
            text="Its creator chose three Spells it cannot be affected by at all."),
    ],
))

add(creature(
    name="Living Bigby's Hand",
    size="Large", type_="Artificial", sub="Living Spell",
    flav="A spell that outlived its caster and never stopped casting. It is a fist the size of a cart, and it is still following its last order.",
    hd=5, armType="Plate", armEnh=0, shield=False,
    weak=[], imm=["Poison"],
    statusImm=["Blinded", "Charmed", "Fatigued", "Frightened", "Paralyzed", "Sickened", "Unconscious"],
    speed=0, spds={"Fly": 60}, zone="Frontline", morale=12, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Force Fist", n=3, d=8, mod=4,
            text="A Large or smaller target is shoved up to 5', and the hand moves with it."),
        act("Action", name="Grasping Hand", dpr=False,
            text="A Huge or smaller Being within reach must pass [Reflex] or be Grappling, taking 15 (2d6+8) damage at the start of each of its Turns. It can't use Force Fist while grappling."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
    ],
))

add(creature(
    name="Living Blade of Disaster",
    size="Medium", type_="Artificial", sub="Living Spell",
    flav="A rip in the world shaped roughly like a sword. It does not so much cut as delete.",
    hd=9, armType="Scale", armEnh=2, shield=False,
    weak=[], imm=["Poison", "Physical from non-Relics"],
    statusImm=["Blinded", "Fatigued", "Grappling", "Paralyzed", "Restrained", "Sickened", "Unconscious"],
    speed=0, spds={"Fly": 30}, zone="Frontline", morale=12, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Force Blade", n=4, d=12, mod=0,
            text="It Crits far more readily than a normal weapon; on a Crit it deals 78 (12d12) instead."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Unfettered", dpr=False,
            text="It passes through any barrier, including a wall of force."),
    ],
))

add(creature(
    name="Living Demiplane",
    size="Medium", type_="Artificial", sub="Living Spell",
    flav="A door to nowhere that drifts along the walls of Ythryn looking for someone to be a room for.",
    hd=7, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=["Poison"],
    statusImm=["Blinded", "Charmed", "Fatigued", "Frightened", "Grappling", "Paralyzed", "Prone", "Restrained", "Sickened", "Unconscious"],
    speed=30, spds={"Climb": 30}, zone="Midline", morale=12, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Cast", name="Extradimensional Chamber", tags="Touch", save="Reflex", dpr=False,
            n=0, d=0, mod=0,
            text="The first time it enters a Being's space on a Turn, that Being must pass [Reflex] or be pulled into a bare stone room 30' on a side with no exit."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Dimensional Form", dpr=False,
            text="It shares space with other Beings freely and can squeeze through a one-inch gap, but it must stay attached to a solid surface."),
        act("Ability", name="Planar Destruction", dpr=False,
            text="When it is destroyed, everything inside its chamber is expelled into the space it occupied."),
    ],
))


# =====================================================================
# F. PRIMORDIALS & PLANTS
# =====================================================================

add(creature(
    name="Needle Blight",
    size="Medium", type_="Primordial", sub="Plant",
    flav="A shrub that walks, and fires its own pine needles at anything warm.",
    hd=2, armType="Leather", armEnh=0, shield=False,
    weak=["Fire"], imm=[], statusImm=["Blinded"],
    speed=30, spds={}, zone="Frontline", morale=10, app="2d6", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Claws", n=2, d=4, mod=1),
        act("Ranged Attack", name="Needles", n=2, d=6, mod=1, dpr=False),
    ],
))

add(creature(
    name="Awakened Shrub",
    size="Medium", type_="Primordial", sub="Plant",
    flav="A bush that someone taught to talk. It has opinions and almost no way to enforce them.",
    hd=3, armType="Unarmored", armEnh=0, shield=False,
    weak=["Fire"], imm=[], statusImm=[],
    speed=20, spds={}, zone="Frontline", morale=5, app="1d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Rake", n=1, d=4, mod=-1),
        act("Ability", name="False Appearance", dpr=False,
            text="While it stays still it is indistinguishable from an ordinary shrub."),
    ],
))

add(creature(
    name="Quaggoth Spore Servant",
    size="Medium", type_="Primordial", sub="Plant",
    flav="A quaggoth corpse being walked around by the fungus that ate it.",
    hd=4, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=["Poison"],
    statusImm=["Blinded", "Charmed", "Frightened", "Paralyzed", "Sickened"],
    speed=20, spds={"Climb": 20}, zone="Frontline", morale=12, app="1d4", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 2x Claw"),
        act("Melee Attack", name="Claw", n=1, d=6, mod=1, mult=2),
    ],
))

add(creature(
    name="Tribal Warrior Spore Servant",
    size="Medium", type_="Primordial", sub="Plant",
    flav="One of Caer-Konig's missing hunters, still holding the spear, no longer holding anything else.",
    hd=2, armType="Hide", armEnh=0, shield=False,
    weak=[], imm=["Poison"],
    statusImm=["Blinded", "Charmed", "Frightened", "Paralyzed", "Sickened"],
    speed=20, spds={}, zone="Frontline", morale=12, app="1d6", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Spear", n=1, d=6, mod=1),
    ],
))

add(creature(
    name="Water Weird",
    size="Large", type_="Primordial", sub="Elemental",
    flav="An invisible serpent of animate water, bound to a fountain or a pool and extremely literal about guarding it.",
    hd=9, armType="Unarmored", armEnh=1, shield=False,
    weak=["Cold"], imm=["Poison"],
    statusImm=["Fatigued", "Grappling", "Paralyzed", "Prone", "Restrained", "Sickened", "Unconscious"],
    speed=0, spds={"Swim": 60}, zone="Frontline", morale=12, app="1", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Constrict", tags="10' reach", n=3, d=6, mod=3,
            text="A Medium or smaller target is pulled 5' toward the weird, is Grappling and Restrained, and is being drowned."),
        act("Ability", name="Invisible in Water", dpr=False,
            text="It is Invisible while fully immersed."),
        act("Ability", name="Water Bound", dpr=False,
            text="It dies if it leaves the water it is bound to, or if that water is destroyed."),
    ],
))

add(creature(
    name="Dryad",
    size="Medium", type_="Fae", sub="",
    flav="Hathowyn, bound to a tree that should not be able to grow this far north, and quietly furious about the cold.",
    hd=5, armType="Leather", armEnh=0, shield=False,
    weak=["Fire"], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=6, app="1", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Shillelagh Club", n=1, d=8, mod=4),
        act("Cast", name="Fey Charm", tags="Near", save="Will", dpr=False,
            text="The target treats the dryad as a trusted friend until it is harmed by her, or a day passes."),
        act("Ability", name="Magic Ward II", dpr=False,
            text="The first time it is unwillingly affected by a Spell each Round, the Caster must spend an extra 2 Mana to affect it."),
        act("Ability", name="Tree Stride", dpr=False,
            text="Once on her Turn she may step into one living tree within reach and step out of another within Far."),
    ],
))


# =====================================================================
# G. BEASTS
# =====================================================================

add(creature(
    name="Fox",
    size="Small", type_="Beast", sub="",
    flav="An arctic fox. Ravisin keeps company with them, and they are cannier than they look.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=4, app="1d4", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=-1),
        act("Ability", name="Keen Hearing", dpr=False,
            text="It has Favor on Checks that rely on hearing."),
    ],
))

add(creature(
    name="Goat",
    size="Medium", type_="Beast", sub="",
    flav="Livestock, and in Ten-Towns, occasionally a wall-climbing menace.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=40, spds={}, zone="Frontline", morale=4, app="2d6", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Ram", n=1, d=4, mod=1),
        act("Ability", name="Charge", dpr=False,
            text="If it moves at least 20' straight at a target before Ramming it, the Attack deals an extra 2 (1d4) damage and the target must pass [Might] or fall Prone."),
    ],
))

add(creature(
    name="Giant Goat",
    size="Large", type_="Beast", sub="",
    flav="A goat that could headbutt a sledge apart, and will if provoked.",
    hd=3, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=40, spds={}, zone="Frontline", morale=6, app="1d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Ram", n=2, d=4, mod=1),
        act("Ability", name="Charge", dpr=False,
            text="If it moves at least 20' straight at a target before Ramming it, the Attack deals an extra 5 (2d4) damage and the target must pass [Might] or fall Prone."),
    ],
))

add(creature(
    name="Mountain Goat",
    size="Medium", type_="Beast", sub="",
    flav="Kelvin's Cairn is full of them, standing on ledges that have no business holding anything.",
    hd=2, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=40, spds={"Climb": 30}, zone="Frontline", morale=5, app="2d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Ram", n=1, d=6, mod=1),
        act("Ability", name="Sure-Footed", dpr=False,
            text="It has Favor on Saves against being knocked Prone, and icy ground never slows it."),
    ],
))

add(creature(
    name="Raven",
    size="Small", type_="Beast", sub="",
    flav="Skelm, Avarice's familiar, is one of these. So is every other bird watching you from the eaves.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=10, spds={"Fly": 50}, zone="Midline", morale=3, app="1d6", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Beak", n=1, d=4, mod=-1),
        act("Ability", name="Mimicry", dpr=False,
            text="It can imitate simple sounds it has heard. A listener who passes [Will] can tell the sound is an imitation."),
    ],
))

add(creature(
    name="Swarm of Ravens",
    size="Medium", type_="Beast", sub="Swarm",
    flav="A black cloud of beaks that has decided you are carrion slightly ahead of schedule.",
    hd=5, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[],
    statusImm=["Charmed", "Frightened", "Grappling", "Paralyzed", "Prone", "Restrained"],
    speed=10, spds={"Fly": 50}, zone="Frontline", morale=8, app="1d3", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Beaks", n=2, d=6, mod=0,
            text="Only 3 (1d6) once the swarm is at half HP or fewer."),
        act("Ability", name="Swarm", dpr=False,
            text="It shares space with other Beings, squeezes through any gap a raven could, and can't regain HP."),
    ],
))

add(creature(
    name="Flying Snake",
    size="Small", type_="Beast", sub="",
    flav="A winged serpent kept as a curiosity in Easthaven and Targos. It bites far above its weight.",
    hd=2, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={"Fly": 60, "Swim": 30}, zone="Midline", morale=6, app="1d3", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=2, d=4, mod=0),
        act("Ability", name="Flyby", dpr=False,
            text="It doesn't provoke Attacks when it flies out of reach."),
    ],
))

add(creature(
    name="Giant Vulture",
    size="Large", type_="Beast", sub="",
    flav="Patient, ugly, and clever enough to help a fight along when it's going the right way.",
    hd=3, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=10, spds={"Fly": 60}, zone="Midline", morale=6, app="1d4", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Beak and 1x Talons"),
        act("Melee Attack", name="Beak", n=1, d=4, mod=2, mult=1),
        act("Melee Attack", name="Talons", n=1, d=6, mod=2, mult=1),
        act("Ability", name="Pack Tactics", dpr=False,
            text="It has Favor on Attacks against a Being that has another of its allies adjacent to it."),
    ],
))

add(creature(
    name="Plesiosaurus",
    size="Large", type_="Beast", sub="",
    flav="Something very old still living in Maer Dualdon, which the Bremen fishers would rather you didn't confirm.",
    hd=6, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Swim": 40}, zone="Frontline", morale=8, app="1", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", tags="10' reach", n=2, d=6, mod=2),
        act("Ability", name="Hold Breath", dpr=False, text="It can hold its breath for an hour."),
    ],
))

add(creature(
    name="Weasel",
    size="Small", type_="Beast", sub="",
    flav="Zelennor, Nass Lantomir's arctic familiar, and every other small thing in the snow with teeth.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=3, app="1d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=-1),
        act("Ability", name="Keen Hearing and Smell", dpr=False,
            text="It has Favor on Checks that rely on hearing or smell."),
    ],
))

add(creature(
    name="Seal",
    size="Medium", type_="Beast", sub="",
    flav="Food, company, or an obstacle, depending on who is looking at it.",
    hd=2, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Swim": 40}, zone="Midline", morale=4, app="2d6", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=-1),
        act("Ability", name="Hold Breath", dpr=False, text="It can hold its breath for 15 minutes."),
    ],
))

add(creature(
    name="Walrus",
    size="Large", type_="Beast", sub="",
    flav="Two thousand pounds of blubber and tusk that would prefer you left the ice floe.",
    hd=3, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Swim": 40}, zone="Frontline", morale=6, app="2d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Tusks", n=2, d=4, mod=2),
        act("Ability", name="Hold Breath", dpr=False, text="It can hold its breath for 10 minutes."),
    ],
))

add(creature(
    name="Giant Walrus",
    size="Huge", type_="Beast", sub="",
    flav="Ukuma is one of these, and he can talk. The others cannot, and are no less dangerous for it.",
    hd=9, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Swim": 40}, zone="Frontline", morale=8, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Body Flop and 1x Tusks"),
        act("Melee Attack", name="Body Flop", n=2, d=8, mod=2, mult=1),
        act("Melee Attack", name="Tusks", n=2, d=6, mod=2, mult=1),
        act("Ability", name="Hold Breath", dpr=False, text="It can hold its breath for 30 minutes."),
    ],
))

add(creature(
    name="Hare",
    size="Small", type_="Beast", sub="",
    flav="An arctic hare. Almost entirely a way for something else to get a meal.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={}, zone="Midline", morale=2, app="2d6", senses=[],
    oversize=0,
    acts=[
        act("Ability", name="Escape", dpr=False,
            text="It can Dash, Disengage, or Hide as a free action on its Turn."),
    ],
))

add(creature(
    name="Knucklehead Trout",
    size="Small", type_="Beast", sub="",
    flav="The fish Ten-Towns is built on. The bony skull carves beautifully, and Ol' Bitey is the biggest ever landed.",
    hd=2, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=0, spds={"Swim": 30}, zone="Midline", morale=2, app="4d6", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=0),
        act("Ability", name="Water Breathing", dpr=False, text="It can breathe only underwater."),
    ],
))

add(creature(
    name="Octopus",
    size="Small", type_="Beast", sub="",
    flav="A small cold-water octopus, mostly interested in not being seen.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=5, spds={"Swim": 30}, zone="Midline", morale=3, app="1d3", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Tentacles", n=1, d=4, mod=-1,
            text="The target is Grappling."),
        act("Ability", name="Ink Cloud", recharge="Cd6", dpr=False,
            text="Underwater, it fills its space and everything adjacent with ink, Blinding those inside, then Dashes as a free action."),
    ],
))

add(creature(
    name="Awakened White Moose",
    size="Large", type_="Beast", sub="",
    flav="Ravisin's guardian, white as the tundra and considerably smarter than a moose ought to be.",
    hd=6, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=40, spds={}, zone="Frontline", morale=9, app="1", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Antlers and 1x Hooves"),
        act("Melee Attack", name="Antlers", n=2, d=8, mod=1, mult=1),
        act("Melee Attack", name="Hooves", n=2, d=4, mod=1, mult=1),
        act("Ability", name="Charge", dpr=False,
            text="If it moves at least 20' straight at a target before hitting it with Antlers, the Attack deals an extra 9 (2d8) damage and the target must pass [Might] or fall Prone."),
    ],
))

add(creature(
    name="Young Griffon (Tiny)",
    size="Small", type_="Cryptid", sub="",
    flav="A griffon chick. It is fluff, it is loud, and its mother is nearby.",
    hd=1, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={"Fly": 40}, zone="Midline", morale=4, app="1d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Beak", n=1, d=4, mod=-1),
    ],
))

add(creature(
    name="Young Griffon (Small)",
    size="Medium", type_="Cryptid", sub="",
    flav="Half-grown, entirely convinced it is full-grown.",
    hd=2, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={"Fly": 60}, zone="Midline", morale=5, app="1d3", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Beak and 1x Claws"),
        act("Melee Attack", name="Beak", n=1, d=4, mod=0, mult=1),
        act("Melee Attack", name="Claws", n=1, d=4, mod=0, mult=1),
    ],
))

add(creature(
    name="Young Griffon (Medium)",
    size="Medium", type_="Cryptid", sub="",
    flav="Nearly a griffon, and already able to carry off a goat.",
    hd=4, armType="Leather", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={"Fly": 80}, zone="Midline", morale=6, app="1d2", senses=[],
    oversize=0,
    acts=[
        act("Combo", name="Combo: 1x Beak and 1x Claws"),
        act("Melee Attack", name="Beak", n=1, d=6, mod=0, mult=1),
        act("Melee Attack", name="Claws", n=1, d=6, mod=1, mult=1),
    ],
))

# --- Iriolarthas's chimeric menagerie (Ch7) ------------------------------
add(creature(
    name="Chimeric Baboon",
    size="Small", type_="Beast", sub="Chimeric",
    flav="One of the Arch-Astronomer's experiments. Its bite has been made venomous, for no reason anyone can now ask about.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={"Climb": 30}, zone="Midline", morale=5, app="2d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=6, mod=0,
            text="Includes an extra 3 (1d6) Poison damage from its altered glands."),
        act("Ability", name="Pack Tactics", dpr=False,
            text="It has Favor on Attacks against a Being that has another of its allies adjacent to it."),
    ],
))

add(creature(
    name="Chimeric Cat",
    size="Small", type_="Beast", sub="Chimeric",
    flav="A cat that was given eyeless sight. It navigates a dark room better than you navigate a lit one.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=40, spds={"Climb": 30}, zone="Midline", morale=3, app="1d4", senses=["Blindsight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Claws", n=1, d=4, mod=-1),
        act("Ability", name="Tremorsense", dpr=False,
            text="It senses everything touching the ground within Near, even through walls."),
    ],
))

add(creature(
    name="Chimeric Fox",
    size="Small", type_="Beast", sub="Chimeric",
    flav="Its fur shifts colour to match whatever is behind it.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=4, app="1d4", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=-1),
        act("Ability", name="Chimeric Creation", dpr=False,
            text="Its fur shifts to match its surroundings, giving it Favor on Checks to hide."),
    ],
))

add(creature(
    name="Chimeric Hare",
    size="Small", type_="Beast", sub="Chimeric",
    flav="Someone gave a hare wings. It has not stopped being a hare about it.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Fly": 30}, zone="Midline", morale=2, app="2d4", senses=[],
    oversize=0,
    acts=[
        act("Ability", name="Escape", dpr=False,
            text="It can Dash, Disengage, or Hide as a free action on its Turn."),
    ],
))

add(creature(
    name="Chimeric Rat",
    size="Small", type_="Beast", sub="Chimeric",
    flav="Gills, iridescent scales, and the ability to breathe both air and water. Still a rat.",
    hd=1, armType="Unarmored", armEnh=0, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=20, spds={"Swim": 20}, zone="Midline", morale=3, app="2d6", senses=["Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=-1),
        act("Ability", name="Chimeric Creation", dpr=False,
            text="It breathes air and water equally well."),
    ],
))

add(creature(
    name="Chimeric Weasel",
    size="Small", type_="Beast", sub="Chimeric",
    flav="Its eyes throw off bright light. It cannot turn them off, and it is not happy about that.",
    hd=1, armType="Unarmored", armEnh=1, shield=False,
    weak=[], imm=[], statusImm=[],
    speed=30, spds={}, zone="Midline", morale=3, app="1d4", senses=[],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=4, mod=-1),
        act("Ability", name="Chimeric Creation", dpr=False,
            text="Its eyes shed bright light in a Near radius and dim light for a Near radius beyond that."),
    ],
))


# =====================================================================
# H. DRAGONS
# =====================================================================

add(creature(
    name="Dragon, Hatchling - Silver",
    size="Medium", type_="Cryptid", sub="Wyrm",
    flav="A silver wyrmling, curious about people in a way its white cousins never are.",
    hd=6, armType="Plate", armEnh=0, shield=False,
    weak=[], imm=["Cold"], statusImm=[],
    speed=30, spds={"Fly": 60}, zone="Frontline", morale=8, app="1", senses=["Blindsight", "Darksight"],
    oversize=0,
    acts=[
        act("Melee Attack", name="Bite", n=1, d=10, mod=2),
        act("Cast", name="Cold Breath", tags="Near Cone", save="Reflex", recharge="Cd6", dpr=False,
            n=3, d=8, mod=0),
        act("Cast", name="Paralyzing Breath", tags="Near Cone", save="Endure", recharge="Cd6", dpr=False,
            n=0, d=0, mod=0,
            text="Targets that fail are Paralyzed (Cd6)."),
    ],
))


if __name__ == "__main__":
    from tl_calc import calc_tl
    print(f"{'name':38s} {'TL':>5}  {'armor':>5} {'hp':>4} {'dpr':>6}")
    print("-" * 68)
    for c in creatures2:
        r = calc_tl(c)
        print(f"{c['name']:38s} {r['tl']:>5}  {c['armor']:>5} {c['hp']:>4} {r['dpr']:>6.2f}")
    print(f"\n{len(creatures2)} creatures")
