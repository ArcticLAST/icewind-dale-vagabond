/**
 * Active Effect fix for the Vagabond system.
 * ------------------------------------------
 * Bundled into this module because the Icewind Dale content depends on it: every relic
 * Power in the Magic Items compendium is an ActiveEffect, and none of them apply without
 * this. See notes/vagabond-effect-bug.md for the full diagnosis.
 *
 * Every ActiveEffect shipped in the Vagabond system stores its changes under
 * `system.changes`:
 *
 *     changes: []                                              <- Foundry applies THIS
 *     system: { changes: [ { key, value, type, priority } ] }   <- the data actually lives here
 *
 * Foundry's `Actor#applyActiveEffects()` only iterates the native `changes` array, and
 * nothing in the system copies one into the other. The single reader of `system.changes`
 * is `getRollDataWithItemEffects()` in documents/actor.mjs, which handles only effects
 * flagged `applicationMode: "on-use"` - so every *permanent* and *when-equipped* effect
 * is inert.
 *
 * Measured against Vagabond 5.4.1: 61 of the system's 62 effects are affected - all 6
 * ancestry traits, all 7 class features, 7 perks, 2 gear, all 14 weapon properties, and
 * all 25 relic Powers.
 *
 * The fix mirrors `system.changes` onto `changes` during data preparation. It is
 * deliberately conservative:
 *   - it only fills a `changes` array that is already empty, so an effect authored
 *     correctly through the UI is never touched;
 *   - it therefore becomes a silent no-op if the system is ever fixed upstream;
 *   - it writes to the prepared document only, never to stored data;
 *   - it skips entries with no `key` (the system ships a couple of blank placeholders).
 */

const TAG = "icewind-dale-vagabond | effect-fix";
const MARKER = "__idrotfEffectShim";

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
  if (game.system.id !== "vagabond") return;          // harmless anywhere else

  const AE = CONFIG.ActiveEffect.documentClass;
  if (AE.prototype[MARKER]) return;                    // never double-patch
  // Stand down if the standalone vagabond-effect-fix module is also installed and active,
  // so the two can coexist during a migration without fighting.
  if (game.modules.get("vagabond-effect-fix")?.active) {
    console.log(`${TAG} | standalone vagabond-effect-fix is active; not patching`);
    return;
  }

  const original = AE.prototype.prepareBaseData;
  AE.prototype.prepareBaseData = function () {
    original?.call(this);

    const stranded = this.system?.changes;
    if (!Array.isArray(stranded) || stranded.length === 0) return;
    if (Array.isArray(this.changes) && this.changes.length > 0) return;

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

  AE.prototype[MARKER] = true;
  console.log(`${TAG} | mirroring system.changes -> changes on ActiveEffect prepare`);
});
