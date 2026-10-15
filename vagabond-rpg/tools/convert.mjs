/**
 * Convert the old Icewind Dale module (built for the community "vagabond" system) into compendium
 * sources for the "vagabond-rpg" system: src/packs/<pack>/*.json.
 *
 * Usage: node tools/convert.mjs <old-packs-json-dir>
 *   <old-packs-json-dir> holds the old module's packs extracted to JSON (see tools/extract-old.mjs).
 *   VAGABOND_SYSTEM points at a clone of github.com/ArcticLAST/vagabond-rpg (default ../../vagabond-rpg),
 *   whose module/rules.mjs reads Saves and damage types the same way the system's own Bestiary does.
 *
 * Keeps every document _id, so the Adventure, folders and any links survive the conversion.
 */
import fs from "node:fs";
import path from "node:path";

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(HERE, "..");
const SYSTEM = path.resolve(process.env.VAGABOND_SYSTEM ?? path.join(ROOT, "..", "..", "vagabond-rpg"));
const rules = await import(path.join(SYSTEM, "module", "rules.mjs"));
const IN = path.resolve(process.argv[2] ?? "");
const OUT = path.join(ROOT, "src", "packs");

const MODULE_ID = JSON.parse(fs.readFileSync(path.join(ROOT, "module.json"), "utf8")).id;
const OLD_ASSETS = "modules/icewind-dale-vagabond/assets/";
const NEW_ASSETS = `modules/${MODULE_ID}/assets/`;
const ICONS = "systems/vagabond-rpg/assets/icons/";
const SOURCE = "Icewind Dale: Rime of the Frostmaiden (Vagabond conversion)";

// Items the core system already ships: the module drops its copy rather than list the same thing twice.
const CORE_DUPLICATES = new Set([
  "Potion of Healing", "Potion of Superior Healing", "Potion of Invisibility", "Potion of Gaseous Form",
  "Potion of Cold Resistance", "Bag of Holding", "Helm of Telepathy"
]);

/* -------------------------------------------- */
/*  Helpers                                     */
/* -------------------------------------------- */

const read = dir => fs.readdirSync(path.join(IN, dir)).filter(f => f.endsWith(".json"))
  .map(f => JSON.parse(fs.readFileSync(path.join(IN, dir, f), "utf8")));
const isFolder = d => d._key?.startsWith("!folders!");
const cap = s => String(s ?? "").replace(/(^|[\s,(-])([a-z])/g, (m, a, b) => a + b.toUpperCase());
const plain = html => String(html ?? "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
const repath = s => typeof s === "string" ? s.replaceAll(OLD_ASSETS, NEW_ASSETS) : s;
const deepRepath = v => JSON.parse(JSON.stringify(v).replaceAll(OLD_ASSETS, NEW_ASSETS));

/** Strip what only made sense in the old world (owner ids, the old system's stats). */
function clean(doc) {
  delete doc._stats;
  doc.ownership = { default: 0 };
  return doc;
}

function write(pack, doc) {
  const dir = path.join(OUT, pack);
  fs.mkdirSync(dir, { recursive: true });
  const slug = doc.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  fs.writeFileSync(path.join(dir, `${isFolder(doc) ? "_folder-" : ""}${slug}-${doc._id}.json`), `${JSON.stringify(doc, null, 2)}\n`);
}

function folder(doc) {
  const out = clean({ ...doc });
  delete out.ownership;
  return out;
}

/** Spell names in <em>…</em> become links to the system's Spells compendium. */
const SPELLS = Object.fromEntries(fs.readdirSync(path.join(SYSTEM, "src", "packs", "spells")).map(f => {
  const d = JSON.parse(fs.readFileSync(path.join(SYSTEM, "src", "packs", "spells", f), "utf8"));
  return [d.name.toLowerCase(), d._id];
}));
const linkSpells = html => String(html ?? "").replace(/<em>([A-Za-z' ]+)<\/em>/g, (m, name) => {
  const id = SPELLS[name.trim().toLowerCase()];
  return id ? `@UUID[Compendium.vagabond-rpg.spells.Item.${id}]{${name.trim()}}` : m;
});

/* -------------------------------------------- */
/*  Creatures and NPCs                          */
/* -------------------------------------------- */

const BEING_TYPES = {
  artificials: "artificial", beasts: "beast", cryptid: "cryptid", fae: "fae", humanlike: "humanlike",
  outers: "outer", primordials: "primordial", undead: "undead"
};
// Vagabond has no Necrotic, Psychic or Force damage: the old system's extras are Magic.
const DAMAGE_TYPES = { magical: "magic", necrotic: "magic", psychic: "magic", piercing: "pierce", slashing: "slash" };
const STATUS_NAMES = { grappling: "Grappled" };

/** "physical" in the old system means mundane damage, which Vagabond writes "Physical from non-Relics". */
// Necrotic and Psychic stay as written on Immune lines: they name no Vagabond damage type, so they're notes for the GM.
const TRAIT_WORDS = { piercing: "Pierce", slashing: "Slash", coldIron: "Cold Iron" };
const traitWord = t => TRAIT_WORDS[t] ?? cap(t);
function immuneText(list) {
  const text = list.filter(t => t !== "physical").map(traitWord).join(", ");
  return list.includes("physical") ? [text, "Physical from non-Relics"].filter(Boolean).join("; ") : text;
}

function speedTypes(list) {
  return list.map(s => {
    const [kind, ft] = s.split(/\s+/);
    return ft ? `${cap(kind)} ${ft}'` : cap(kind);
  }).join(", ");
}

function itemId(actorId, n) {
  // Deterministic 16-character ids for embedded Actions, derived from the Actor's id.
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let h = 2166136261;
  for ( const c of `${actorId}:${n}` ) h = Math.imul(h ^ c.charCodeAt(0), 16777619) >>> 0;
  let out = "";
  for ( let i = 0; i < 16; i++ ) {
    h = Math.imul(h ^ (h >>> 13), 2654435761) >>> 0;
    out += chars[h % chars.length];
  }
  return out;
}

function action(actor, a, sort) {
  const isCombo = a.name === "Combo" || /^\s*\d+\s*x\s*\w/i.test(a.extraInfo ?? "") && !a.rollDamage;
  const actionType = isCombo ? "combo"
    : a.attackType?.startsWith("cast") ? "cast"
    : a.attackType === "ranged" ? "ranged"
    : /^\s*Cast\b/i.test(a.note) ? "cast" : "melee";
  let tags = (a.note ?? "").trim();
  if ( !tags && actionType === "melee" ) tags = "Melee Attack";
  if ( !tags && actionType === "ranged" ) tags = "Ranged Attack";
  if ( isCombo ) tags = "";
  const extra = (a.extraInfo ?? "").trim();
  let text;
  if ( isCombo ) text = extra.replace(/(\d+)\s*x\s*/gi, "$1×").replace(/,\s*/g, " and ");
  else if ( a.rollDamage ) text = [a.flatDamage ? `${a.flatDamage} (${a.rollDamage})` : `(${a.rollDamage})`, extra].filter(Boolean).join(" ");
  else text = extra;
  const healing = a.damageType === "healing";
  const saves = rules.actionSaves({ actionType, tags, text });
  let damageType = "";
  if ( a.rollDamage && !healing && !isCombo ) {
    damageType = (a.damageType && a.damageType !== "-") ? (DAMAGE_TYPES[a.damageType] ?? a.damageType)
      : rules.inferActionDamage(a.name, actionType).type;
  }
  const recharge = /^Cd\d+/.test(a.recharge) ? `Recharge ${a.recharge}` : (a.recharge ?? "");
  return {
    _id: itemId(actor._id, sort),
    name: a.name,
    type: "action",
    img: `${ICONS}sword-clash.svg`,
    system: {
      description: text ? `<p>${text}</p>` : "",
      source: "",
      actionType,
      tags,
      damage: isCombo ? "" : (a.rollDamage ?? ""),
      average: (!isCombo && a.flatDamage !== "" && Number.isFinite(Number(a.flatDamage))) ? Number(a.flatDamage) : null,
      damageType,
      save: saves.save,
      recharge,
      sort,
      relic: 0,
      effectSaves: Object.fromEntries(["endure", "reflex", "will"].map(s => [s, saves.effect.includes(s)])),
      healing
    },
    effects: [], folder: null, sort: sort * 100, ownership: { default: 0 }, flags: {}
  };
}

function ability(actor, ab, sort) {
  const text = ab.description ?? "";
  const saves = rules.actionSaves({ actionType: "ability", tags: "", text });
  return {
    _id: itemId(actor._id, sort),
    name: ab.name,
    type: "action",
    img: `${ICONS}sword-clash.svg`,
    system: {
      description: text.startsWith("<") ? text : `<p>${text}</p>`,
      source: "", actionType: "ability", tags: "", damage: "", average: null, damageType: "",
      save: saves.save, recharge: "", sort, relic: 0,
      effectSaves: Object.fromEntries(["endure", "reflex", "will"].map(s => [s, saves.effect.includes(s)])),
      healing: false
    },
    effects: [], folder: null, sort: sort * 100, ownership: { default: 0 }, flags: {}
  };
}

function actor(old) {
  const s = old.system;
  const iwd = old.flags?.icewindDale ?? {};
  const items = [];
  (s.actions ?? []).forEach(a => items.push(action(old, a, items.length)));
  (s.abilities ?? []).forEach(a => items.push(ability(old, a, items.length)));
  for ( const i of items ) i._key = `!actors.items!${old._id}.${i._id}`;

  let description = s.biography || (s.description ? `<p>${s.description}</p>` : "");
  if ( iwd.statBlock ) description += `<p><strong>Stat block:</strong> ${iwd.statBlock}</p>`;
  const token = deepRepath(old.prototypeToken ?? {});
  token.bar1 = { attribute: "attributes.hp" };
  token.bar2 = { attribute: null };

  return {
    _id: old._id,
    _key: `!actors!${old._id}`,
    name: old.name,
    type: "npc",
    img: repath(old.img),
    system: {
      hd: Math.max(0, Math.round(s.hd ?? 1)),
      tl: Number(s.threatLevel ?? 1),
      attributes: {
        hp: { value: s.health?.max ?? s.health?.value ?? 4, max: s.health?.max ?? 4 },
        armor: Math.max(0, s.armor ?? 0),
        armorTag: s.armorDescription ?? "",
        morale: s.morale == null ? null : Math.min(12, Math.max(2, s.morale)),
        speed: { value: s.speed ?? 30, types: speedTypes(s.speedTypes ?? []) },
        travel: 0
      },
      cargo: { max: 0 },
      details: {
        size: s.size ?? "medium",
        beingType: BEING_TYPES[String(s.beingType ?? "").toLowerCase()] ?? "humanlike",
        subtype: "",
        zone: s.zone ?? "frontline",
        appearing: s.appearing ?? "",
        senses: s.senses ?? "",
        immune: immuneText(s.immunities ?? []),
        weak: (s.weaknesses ?? []).map(traitWord).join(", "),
        statusImmunities: (s.statusImmunities ?? []).map(x => STATUS_NAMES[x] ?? cap(x)).join(", "),
        source: iwd.chapter ? `${SOURCE}, ${iwd.chapter}` : SOURCE,
        description
      }
    },
    items,
    effects: [],
    folder: old.folder ?? null,
    sort: old.sort ?? 0,
    ownership: { default: 0 },
    flags: iwd && Object.keys(iwd).length ? { [MODULE_ID]: iwd } : {},
    prototypeToken: token
  };
}

/* -------------------------------------------- */
/*  Magic Items                                 */
/* -------------------------------------------- */

const WEAPON_BASES = {
  "Berserker Axe": "battleaxe", "Trident +2": "spear", "Laser Pistol": "handgun", "Laser Rifle": "rifle",
  "Wand of Orcus": "mace"
};
const ARMOR_BASES = { "Mithral Armor": "armor-medium" };
// Armor bonuses the item grants while equipped, as Active Effects (like the core Loyalty Shield).
const ARMOR_EFFECTS = { "Berserker Axe": 1, "Cloak of Protection": 1, "Staff of Power": 2 };
// Relics whose Power is a plain damage roll get the same roll button as Alchemical Items.
const ROLLS = {
  "Necklace of Fireballs": { formula: "3d6", type: "damage", save: "reflex", damageType: "fire" },
  "Horn of Blasting": { formula: "5d6", type: "damage", save: "endure", damageType: "physical" }
};

const coreItem = (pack, slug) => {
  const dir = path.join(SYSTEM, "src", "packs", pack);
  const f = fs.readdirSync(dir).find(n => n.startsWith(`${slug}-`) && n.length === slug.length + 22);
  return JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
};

function value(cost = {}) {
  return ((cost.gold ?? 0) * 100) + ((cost.silver ?? 0) * 10) + (cost.copper ?? 0);
}

function powerBonus(desc, kind) {
  const m = plain(desc).match(new RegExp(`\\(\\+(\\d)\\) ${kind}:`));
  return m ? Number(m[1]) : 0;
}

function uses(desc) {
  const t = plain(desc);
  const m = t.match(/Holds (\d+) charges/i) ?? t.match(/(\d+) charges, all of which/i);
  if ( m ) return Number(m[1]);
  const words = { two: 2, three: 3, four: 4, five: 5, six: 6 };
  const w = t.match(/\b(two|three|four|five|six) (?:uses|beads)\b/i);
  return w ? words[w[1].toLowerCase()] : 0;
}

function armorEffect(item, bonus) {
  return {
    _id: itemId(item._id, 99), _key: `!items.effects!${item._id}.${itemId(item._id, 99)}`,
    name: `(+${bonus}) Armor`, img: `${ICONS}crystal-ball.svg`, transfer: true, disabled: false,
    changes: [{ key: "system.bonuses.armor", mode: 2, value: String(bonus), priority: null }],
    description: "", origin: null, tint: "#ffffff", statuses: [], flags: {},
    duration: { startTime: null, seconds: null, combat: null, rounds: null, turns: null, startRound: null, startTurn: null },
    system: {}, type: "base", sort: 0
  };
}

function item(old) {
  const s = old.system;
  const lore = s.lore && s.lore !== "None" ? s.lore : "Relic";
  const isPotion = s.equipmentType === "alchemical";
  const cost = value(s.baseCost);
  let desc = linkSpells(s.description ?? "");
  if ( !isPotion ) {
    desc = `<p><em>Lore: ${lore}</em></p>${desc}<p>Value: ${s.baseCost?.gold ?? 0}g</p>`;
  }
  const base = {
    _id: old._id, _key: `!items!${old._id}`, name: old.name, folder: old.folder ?? null, sort: old.sort ?? 0,
    ownership: { default: 0 }, flags: {}, effects: []
  };
  const common = { description: desc, source: SOURCE, quantity: 1, value: cost, equipped: false };

  if ( WEAPON_BASES[old.name] ) {
    const core = coreItem("weapons-armor", WEAPON_BASES[old.name]);
    const bonus = powerBonus(desc, "Weapon");
    Object.assign(base, {
      type: "weapon", img: `${ICONS}broadsword.svg`,
      system: { ...core.system, ...common, slots: core.system.slots, bonus, relic: true }
    });
  } else if ( ARMOR_BASES[old.name] ) {
    const core = coreItem("weapons-armor", ARMOR_BASES[old.name]);
    Object.assign(base, {
      type: "armor", img: `${ICONS}breastplate.svg`,
      system: { ...core.system, ...common, might: 0, metal: "mythral", bonus: powerBonus(desc, "Armor") }
    });
  } else {
    const n = uses(desc);
    const holding = plain(desc).match(/can hold (\d+) Slots/i);
    Object.assign(base, {
      type: "gear", img: `${ICONS}${isPotion ? "knapsack" : "crystal-ball"}.svg`,
      system: {
        ...common,
        slots: old.type === "container" ? (s.slots ?? 1) : (s.baseSlots ?? 1),
        category: isPotion ? "alchemical" : "relic",
        alchemicalType: isPotion ? "potion" : "",
        consumable: isPotion || /Consumable/i.test(lore),
        slotsBonus: holding ? Number(holding[1]) : 0,
        uses: { value: n, max: n },
        roll: ROLLS[old.name] ?? { formula: "", type: "", save: "", damageType: "" },
        contents: [], wealth: 0
      }
    });
  }
  if ( ARMOR_EFFECTS[old.name] ) base.effects.push(armorEffect(old, ARMOR_EFFECTS[old.name]));
  return base;
}

/** Keep the conversion notes true to this module. */
function journalText(html) {
  return html
    .replace("<strong>Magic Items</strong> — 74, in six folders,",
      `<strong>Magic Items</strong> — ${out.items.length}, in six folders (${dropped.join(", ")} are left out: use the core Relics and Alchemical Items compendiums),`)
    .replace("<li><strong>No burrow speed.</strong>",
      "<li><strong>No Necrotic or Psychic damage.</strong> Attacks that dealt them deal Magic damage; Immune lines still name them as a note for the GM.</li><li><strong>No burrow speed.</strong>");
}

/* -------------------------------------------- */
/*  Run                                         */
/* -------------------------------------------- */

fs.rmSync(OUT, { recursive: true, force: true });
const out = { monsters: [], npcs: [], items: [], scenes: [], journals: [], tables: [], folders: [] };

for ( const [oldPack, pack] of [["idrotf-monsters", "monsters"], ["idrotf-npcs", "npcs"]] ) {
  for ( const d of read(oldPack) ) {
    if ( isFolder(d) ) { write(pack, folder(d)); out.folders.push(folder(d)); continue; }
    const a = actor(d);
    write(pack, a);
    out[pack].push(a);
  }
}

const dropped = [];
for ( const d of read("idrotf-items") ) {
  if ( isFolder(d) ) { write("items", folder(d)); out.folders.push(folder(d)); continue; }
  if ( CORE_DUPLICATES.has(d.name) ) { dropped.push(d.name); continue; }
  const i = item(d);
  write("items", i);
  out.items.push(i);
}

for ( const [oldPack, pack, key] of [["idrotf-scenes", "scenes", "scenes"], ["idrotf-journals", "journals", "journals"],
  ["idrotf-tables", "tables", "tables"]] ) {
  for ( const d of read(oldPack) ) {
    const doc = clean(deepRepath(d));
    for ( const page of doc.pages ?? [] ) if ( page.text?.content ) page.text.content = journalText(page.text.content);
    if ( isFolder(d) ) { delete doc.ownership; out.folders.push(doc); write(pack, doc); continue; }
    write(pack, doc);
    out[key].push(doc);
  }
}

// One Adventure that imports everything with the old folder tree.
const [oldAdventure] = read("idrotf-adventure");
// Adventure documents keep the Adventure's own folder ids, which differ from the compendium folders.
const advFolder = new Map(["actors", "items", "journal", "tables", "scenes"]
  .flatMap(k => (oldAdventure[k] ?? []).map(d => [d._id, d.folder ?? null])));
const strip = ({ _key, ...d }) => {
  const r = JSON.parse(JSON.stringify(d));
  r.folder = advFolder.get(r._id) ?? null;
  for ( const i of r.items ?? [] ) delete i._key;
  for ( const e of r.effects ?? [] ) delete e._key;
  return r;
};
const adventure = clean(deepRepath({
  ...oldAdventure,
  description: oldAdventure.description,
  folders: oldAdventure.folders.map(f => { const c = { ...f }; delete c._stats; return c; }),
  actors: [...out.monsters, ...out.npcs].map(strip),
  items: out.items.map(strip),
  journal: out.journals.map(strip),
  tables: out.tables.map(strip),
  scenes: out.scenes.map(strip)
}));
write("adventure", adventure);

console.log(`Monsters ${out.monsters.length}, NPCs ${out.npcs.length}, Items ${out.items.length} (dropped core duplicates: ${dropped.join(", ")}), `
  + `Scenes ${out.scenes.length}, Journals ${out.journals.length}, Tables ${out.tables.length}`);
