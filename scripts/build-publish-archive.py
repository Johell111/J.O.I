"""Zip the clean publish folder with index.html at the archive root."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PUBLISH = ROOT / 'publish'
ARCHIVE = ROOT / 'J.O.I.-Portfolio-Publish.zip'
TEMP_ARCHIVE = ROOT / 'J.O.I.-Portfolio-Publish.tmp.zip'

if PUBLISH.is_symlink() or PUBLISH.resolve().parent != ROOT.resolve():
    raise RuntimeError('Publish directory must remain inside the project.')
if not (PUBLISH / 'index.html').is_file():
    raise RuntimeError('Run python scripts/prepare-publish.py first.')

files = sorted(path for path in PUBLISH.rglob('*') if path.is_file())
with ZipFile(TEMP_ARCHIVE, 'w', compression=ZIP_DEFLATED, compresslevel=9) as bundle:
    for path in files:
        if path.is_symlink() or not path.resolve().is_relative_to(PUBLISH.resolve()):
            raise RuntimeError(f'Unexpected publish path: {path}')
        bundle.write(path, path.relative_to(PUBLISH).as_posix())
TEMP_ARCHIVE.replace(ARCHIVE)
print(f'Created {ARCHIVE.name}: {len(files)} files, {ARCHIVE.stat().st_size:,} bytes; index.html at archive root.')
