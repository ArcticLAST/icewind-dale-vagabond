/**
 * Extract the old module's LevelDB packs (../module/packs) to JSON for tools/convert.mjs.
 * Usage: node tools/extract-old.mjs <dest-dir>
 * LevelDB can't be opened in place on some network drives, so copy ../module/packs somewhere local first
 * and pass it as OLD_PACKS if needed.
 */
import { extractPack } from "@foundryvtt/foundryvtt-cli";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const src = process.env.OLD_PACKS ?? path.join(root, "..", "module", "packs");
const [dest] = process.argv.slice(2);
for ( const p of fs.readdirSync(src) ) {
  await extractPack(path.join(src, p), path.join(dest, p), { log: false, clean: true });
}
