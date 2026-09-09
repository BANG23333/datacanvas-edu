"""Synchronize the marketplace plugin with the canonical standalone Skill."""

import argparse
import json
from pathlib import Path
import shutil


def skill_files(directory):
    return {
        path.relative_to(directory): path.read_bytes()
        for path in directory.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
        and path.name != ".DS_Store"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify without writing files")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    marketplace = json.loads((root / ".agents/plugins/marketplace.json").read_text())
    entry = next(item for item in marketplace["plugins"] if item["name"] == "datacanvas-edu")
    plugin = (root / entry["source"]["path"]).resolve()
    if plugin != root / "plugins/datacanvas-edu":
        raise SystemExit("Marketplace must reference ./plugins/datacanvas-edu")
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    if manifest["name"] != plugin.name or manifest["skills"] != "./skills/":
        raise SystemExit("Plugin identity or Skill discovery path is inconsistent")

    source = root / "skills/datacanvas-edu"
    destination = plugin / "skills/datacanvas-edu"
    expected = skill_files(source)
    if Path("SKILL.md") not in expected:
        raise SystemExit("Missing canonical Skill entry point")
    actual = skill_files(destination)
    unexpected = actual.keys() - expected.keys()
    if unexpected:
        raise SystemExit("Review unexpected bundled files before rebuilding: " + ", ".join(map(str, sorted(unexpected))))
    if args.check:
        mismatches = [str(path) for path, data in expected.items() if actual.get(path) != data]
        if mismatches:
            raise SystemExit("Plugin bundle is stale or incomplete: " + ", ".join(mismatches))
    else:
        for path in expected:
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / path, target)
    print(f"Plugin bundle {'verified' if args.check else 'built'}: {len(expected)} Skill files")


if __name__ == "__main__":
    main()
