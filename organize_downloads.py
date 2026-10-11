import shutil
from pathlib import Path

VIDEO_EXTS = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v"}
AUDIO_EXTS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff", ".svg"}
DOCUMENT_EXTS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf",
    ".odt", ".ods", ".odp", ".csv", ".md", ".log"
}
ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"}
CODE_EXTS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".php", ".html", ".css", ".json", ".xml", ".sql", ".yaml", ".yml"}
SCRIPT_EXTS = {".bat", ".cmd", ".ps1", ".sh", ".exe", ".msi"}
TORRENT_EXTS = {".torrent"}

CATEGORY_ORDER = [
    "Videos",
    "Audio",
    "Images",
    "Documents",
    "Archives",
    "Code",
    "Scripts",
    "Torrents",
    "Other"
]

CATEGORY_MAP = {
    "Videos": VIDEO_EXTS,
    "Audio": AUDIO_EXTS,
    "Images": IMAGE_EXTS,
    "Documents": DOCUMENT_EXTS,
    "Archives": ARCHIVE_EXTS,
    "Code": CODE_EXTS,
    "Scripts": SCRIPT_EXTS,
    "Torrents": TORRENT_EXTS,
}


def get_category(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "Other"


def get_unique_path(folder: Path, file_name: str) -> Path:
    target = folder / file_name
    if not target.exists():
        return target

    stem = Path(file_name).stem
    suffix = Path(file_name).suffix
    counter = 1

    while True:
        new_name = f"{stem}_{counter}{suffix}"
        candidate = folder / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(folder: Path):
    if not folder.exists() or not folder.is_dir():
        print(f"Folder not found: {folder}")
        return

    for category in CATEGORY_ORDER:
        (folder / category).mkdir(exist_ok=True)

    moved = 0
    skipped = 0

    for item in list(folder.iterdir()):
        if item.is_dir():
            continue

        if item.name.lower() in {"organize_downloads.py", "organize_downloads.bat"}:
            skipped += 1
            continue

        category = get_category(item)
        dest_dir = folder / category
        dest_path = get_unique_path(dest_dir, item.name)

        try:
            shutil.move(str(item), str(dest_path))
            print(f"Moved: {item.name} -> {category}")
            moved += 1
        except Exception as e:
            print(f"Could not move {item.name}: {e}")
            skipped += 1

    print("\nFinished.")
    print(f"Files moved: {moved}")
    print(f"Files skipped: {skipped}")


if __name__ == "__main__":
    downloads_folder = Path(__file__).resolve().parent
    organize_folder(downloads_folder)
