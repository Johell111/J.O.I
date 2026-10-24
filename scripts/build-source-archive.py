"""Rebuild the editable source bundle without including the bundle itself."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "J.O.I.-Cinematic-Portfolio-Revision.zip"
TEMP_ARCHIVE = ROOT / "J.O.I.-Cinematic-Portfolio-Revision.tmp.zip"

if ARCHIVE.resolve().parent != ROOT.resolve():
    raise RuntimeError(f"Refusing to write outside the project folder: {ARCHIVE}")

files = []
with ZipFile(TEMP_ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as bundle:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] in {".git", "__pycache__", "preview"}:
            continue
        if path in {ARCHIVE, TEMP_ARCHIVE} or path.suffix.lower() in {".pyc", ".zip"}:
            continue
        bundle.write(path, relative.as_posix())
        files.append(relative.as_posix())

TEMP_ARCHIVE.replace(ARCHIVE)
print(f"Rebuilt {ARCHIVE.name}: {len(files)} files, {ARCHIVE.stat().st_size:,} bytes")
