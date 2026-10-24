"""Copy only the static site and referenced assets into the upload folder."""

from pathlib import Path, PurePosixPath
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "publish"
ROOT_RESOLVED = ROOT.resolve()

if OUTPUT.exists():
    if OUTPUT.is_symlink() or OUTPUT.resolve().parent != ROOT_RESOLVED:
        raise RuntimeError(f"Refusing to replace unexpected output path: {OUTPUT}")
    shutil.rmtree(OUTPUT.resolve())
OUTPUT.mkdir()

site_files = [
    *ROOT.glob("*.html"),
    ROOT / "styles.css",
    ROOT / "favicon.svg",
    ROOT / "robots.txt",
    ROOT / "sitemap.xml",
    *sorted((ROOT / "js").glob("*.js")),
]
site_files = [path for path in site_files if path.is_file()]
asset_references: set[str] = set()
asset_pattern = re.compile(r"assets/[A-Za-z0-9_./-]+")

for path in site_files:
    asset_references.update(asset_pattern.findall(path.read_text(encoding="utf-8")))

for relative in sorted(asset_references):
    source = (ROOT / PurePosixPath(relative)).resolve()
    if not source.is_relative_to(ROOT_RESOLVED):
        raise RuntimeError(f"Asset reference escapes the project folder: {relative}")
    if not source.is_file():
        raise FileNotFoundError(f"Referenced site asset does not exist: {relative}")
    site_files.append(source)

for source in site_files:
    relative = source.relative_to(ROOT_RESOLVED)
    destination = OUTPUT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

print(f"Prepared {len(site_files)} files in {OUTPUT}")
