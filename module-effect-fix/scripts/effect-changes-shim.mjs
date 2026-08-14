/**
 * Vagabond - Active Effect Fix
 * ----------------------------
 * Every ActiveEffect shipped in the Vagabond system stores its changes under
 * `system.changes`:
 *
 *     changes: []                                              <- Foundry applies THIS
 *     system: { changes: [ { key, value, type, priority } ] }   <- the data actually lives here
 *
 * Foundry's `Actor#applyActiveEffects()` only ever iterates the native `changes`
 * array, and nothing in the system copies one into the other. The single reader of
 * `system.changes` is `getRollDataWithItemEffects()` in documents/actor.mjs, which
 * handles only effects flagged `applicationMode: "on-use"` - so every *permanent*
 * effect is inert.
 *
 * Measured against Vagabond 5.4.1: 61 of the system's 62 effects are affected -
 * all 6 ancestry traits, all 7 class features, 7 perks, 2 gear, all 14 weapon
 * properties, and all 25 relic Powers.
 *
 * The fix mirrors `system.changes` onto `changes` during data preparation.
 * It is deliberately conservative:
 *   - it only fills a `changes` array that is already empty, so a correctly
 *     authored effect is never touched;
 *   - it therefore becomes a no-op automatically if the system is ever fixed;
 *   - it writes to the prepared document only, never to stored data.
 */

const MODULE_ID = "vagabond-effect-fix";

/** Vagabond's `type` string -> Foundry's numeric ACTIVE_EFFECT_MODES. */
function modeFor(type) {
  const M = CONST.ACTIVE_EFFECT_MODES;
  switch (String(type ?? "add").toLowerCase()) {
    case "custom":    return M.CUSTOM;
    case "multiply":  return M.MULTIPLY;
    case "override":  return M.OVERRIDE;
    case "downgrade": return M.DOWNGRADE;
    case "upgrade":   return M.UPGRADE;
    case "add":
    default:          return M.ADD;
  }
}

Hooks.once("init", () => {
  const AE = CONFIG.ActiveEffect.documentClass;
  if (AE.prototype[`__${MODULE_ID}`]) return;

  const original = AE.prototype.prepareBaseData;
  AE.prototype.prepareBaseData = function () {
    original?.call(this);

    const stranded = this.system?.changes;
    if (!Array.isArray(stranded) || stranded.length === 0) return;
    if (Array.isArray(this.changes) && this.changes.length > 0) return;  // already authored correctly

    this.changes = stranded
      .filter(c => c?.key)
      .map(c => ({
        key: c.key,
        // AE change values are strings; formulas such as "@lvl" must survive verbatim
        value: c.value === null || c.value === undefined ? "" : String(c.value),
        mode: modeFor(c.type),
        priority: c.priority ?? null
      }));
  };

  AE.prototype[`__${MODULE_ID}`] = true;
  console.log(`${MODULE_ID} | mirroring system.changes -> changes on ActiveEffect prepare`);
});

Hooks.once("ready", () => {
  if (game.system.id !== "vagabond") {
    ui.notifications?.warn(`${MODULE_ID} is only meant for the Vagabond system.`);
    return;
  }
  // One-off count so it is obvious in the log whether the shim is doing anything.
  let repaired = 0;
  for (const actor of game.actors) {
    for (const effect of actor.allApplicableEffects?.() ?? []) {
      if ((effect._source.changes?.length ?? 0) === 0 && (effect.system?.changes?.length ?? 0) > 0) repaired++;
    }
  }
  console.log(`${MODULE_ID} | ready - ${repaired} stranded effect(s) repaired on ${game.actors.size} actor(s)`);
});
