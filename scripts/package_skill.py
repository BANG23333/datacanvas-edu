"""Build a deterministic ZIP of the reusable Skill and its file manifest."""

from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def main():
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills/datacanvas-edu"
    version = "0.1.2"
    files = sorted(
        path for path in skill.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
        and path.name != ".DS_Store"
    )
    if not (skill / "SKILL.md").is_file():
        raise SystemExit("Missing Skill entry point")
    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    archive = dist / f"datacanvas-edu-v{version}.zip"
    fingerprints = {}
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as handle:
        for path in files:
            relative = path.relative_to(skill.parent).as_posix()
            data = path.read_bytes()
            info = ZipInfo(relative, date_time=(2026, 9, 8, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            handle.writestr(info, data)
            fingerprints[relative] = sha256(data).hexdigest()
    manifest = {
        "version": version,
        "zip": archive.name,
        "sha256": sha256(archive.read_bytes()).hexdigest(),
        "file_count": len(files),
        "files": fingerprints,
    }
    (dist / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {archive.name}: {len(files)} Skill files")


if __name__ == "__main__":
    main()
