# -*- coding: utf-8 -*-
"""
Builds dist/module.zip for manifest-based install (ForgeVTT, or Foundry's "Install from URL").

Why not PowerShell's Compress-Archive: on Windows PowerShell 5.1 it stores BACKSLASH path
separators inside the zip. The ZIP spec requires forward slashes, and Linux-hosted Foundry
(which is what ForgeVTT runs) then extracts the whole thing as flat files with literal
backslashes in their names. Python's zipfile writes correct POSIX paths.

The archive must contain exactly ONE top-level folder named after the module id.
"""
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "module"
DIST = ROOT / "dist"
SKIP = {"LOCK", "LOG", "LOG.old"}          # LevelDB runtime files; recreated on open

manifest = json.loads((SRC / "module.json").read_text(encoding="utf-8"))
MODULE_ID = manifest["id"]

DIST.mkdir(exist_ok=True)
zip_path = DIST / "module.zip"

count = 0
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(SRC.rglob("*")):
        if p.is_dir() or p.name in SKIP:
            continue
        z.write(p, f"{MODULE_ID}/{p.relative_to(SRC).as_posix()}")
        count += 1

# module.json is published alongside the zip so the manifest URL can be fetched on its own
(DIST / "module.json").write_bytes((SRC / "module.json").read_bytes())

# ---- verify ----
with zipfile.ZipFile(zip_path) as z:
    names = z.namelist()
    roots = {n.split("/")[0] for n in names}
    problems = []
    if any(chr(92) in n for n in names):
        problems.append("backslash separators present")
    if roots != {MODULE_ID}:
        problems.append(f"expected one root folder {MODULE_ID!r}, got {roots}")
    if f"{MODULE_ID}/module.json" not in names:
        problems.append("module.json not at the top of the module folder")
    bad = z.testzip()
    if bad:
        problems.append(f"corrupt entry: {bad}")

    print(f"dist/module.zip   {count} files, {zip_path.stat().st_size/1048576:.1f} MB")
    print(f"  root folder     {roots}")
    print(f"  pack files      {len([n for n in names if '/packs/' in n])}")
    print(f"  asset files     {len([n for n in names if '/assets/' in n])}")
    print(f"  version         {manifest['version']}")
    print(f"  manifest url    {manifest.get('manifest')}")
    print(f"  download url    {manifest.get('download')}")
    print("  status          " + ("OK" if not problems else "PROBLEMS: " + "; ".join(problems)))
