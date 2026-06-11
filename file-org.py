import os
import shutil
import argparse
import sys

# Force UTF-8 encoding on standard streams to prevent Windows console emoji encoding errors
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stdin, 'reconfigure'):
    try:
        sys.stdin.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Photo extensions → go into PHOTOS/<ext>/
PHOTO_TYPES = {"jpg", "jpeg", "png", "heic", "webp", "gif", "bmp", "tiff", "raw"}

# Everything else → folder named after type (uppercase)
OTHER_TYPES = {
    "pdf":  "PDF",
    "doc":  "DOCS",
    "docx": "DOCS",
    "txt":  "TXT",
    "xlsx": "EXCEL",
    "xls":  "EXCEL",
    "csv":  "CSV",
    "pptx": "POWERPOINT",
    "ppt":  "POWERPOINT",
    "mp4":  "VIDEOS",
    "mov":  "VIDEOS",
    "avi":  "VIDEOS",
    "mkv":  "VIDEOS",
    "mp3":  "AUDIO",
    "wav":  "AUDIO",
    "zip":  "ARCHIVES",
    "rar":  "ARCHIVES",
    "7z":   "ARCHIVES",
    "exe":  "PROGRAMS",
    "msi":  "PROGRAMS",
    "py":   "CODE",
    "js":   "CODE",
    "html": "CODE",
    "css":  "CODE",
}


def iter_source_files(source_folder, dest_folder, recursive):
    """Yield (source_path, filename) for every file to organize.

    When recursive is True, subfolders are traversed with os.walk(); the
    destination folder is pruned so already-organized files are never
    re-scanned if it lives inside the source folder.
    """
    if not recursive:
        for filename in os.listdir(source_folder):
            source_path = os.path.join(source_folder, filename)
            if os.path.isfile(source_path):
                yield source_path, filename
        return

    dest_abs = os.path.abspath(dest_folder)
    for root, dirs, files in os.walk(source_folder):
        # Don't descend into the destination folder (avoids re-scanning copies)
        dirs[:] = [
            d for d in dirs
            if os.path.abspath(os.path.join(root, d)) != dest_abs
        ]
        for filename in files:
            yield os.path.join(root, filename), filename


def organize_files(source_folder, dest_folder, mode="copy", recursive=False, log_callback=print):
    copied  = 0
    moved   = 0
    skipped = 0
    unknown = 0

    scope = "recursively" if recursive else "top-level only"
    log_callback(f"📂 Scanning ({scope}): {source_folder}\n")

    try:
        files = list(iter_source_files(source_folder, dest_folder, recursive))
    except Exception as e:
        log_callback(f"❌ Error listing source folder: {e}")
        return

    for source_path, filename in files:
        # Get extension (lowercase, no dot)
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        # Determine destination subfolder
        if ext in PHOTO_TYPES:
            dest_subfolder = os.path.join(dest_folder, "PHOTOS", ext.upper())
        elif ext in OTHER_TYPES:
            dest_subfolder = os.path.join(dest_folder, OTHER_TYPES[ext])
        else:
            dest_subfolder = os.path.join(dest_folder, "OTHERS")
            unknown += 1

        # Create destination folder if it doesn't exist
        try:
            os.makedirs(dest_subfolder, exist_ok=True)
        except Exception as e:
            log_callback(f"❌ Error creating directory {dest_subfolder}: {e}")
            continue

        dest_path = os.path.join(dest_subfolder, filename)

        # Skip if file already exists at destination
        if os.path.exists(dest_path):
            log_callback(f"⏭️  Skipped (already exists): {filename}")
            skipped += 1
            continue

        # Copy/Move file with metadata preserved
        try:
            if mode == "move":
                shutil.move(source_path, dest_path)
                log_callback(f"🚚 Moved: {filename}  →  {dest_subfolder}")
                moved += 1
            else:
                shutil.copy2(source_path, dest_path)
                log_callback(f"✅ Copied: {filename}  →  {dest_subfolder}")
                copied += 1
        except Exception as e:
            log_callback(f"❌ Error processing {filename}: {e}")

    log_callback(f"\n─────────────────────────────")
    if mode == "move":
        log_callback(f"🚚 Moved:   {moved} file(s)")
    else:
        log_callback(f"✅ Copied:  {copied} file(s)")
    log_callback(f"⏭️  Skipped: {skipped} file(s)")
    log_callback(f"📦 Unknown: {unknown} file(s) → OTHERS/")
    log_callback(f"─────────────────────────────\n")


def get_source_folder():
    while True:
        path = input("📂 Enter source folder path: ").strip()
        if os.path.isdir(path):
            return path
        print("❌ Folder not found. Try again.\n")


def get_dest_folder():
    while True:
        choice = input("\nDestination — create new folder or use existing? (new/existing): ").strip().lower()

        if choice == "new":
            parent = input("📁 Enter path where new folder will be created: ").strip()
            if not os.path.isdir(parent):
                print("❌ That path doesn't exist. Try again.\n")
                continue
            name = input("📝 Enter new folder name: ").strip()
            full_path = os.path.join(parent, name)
            os.makedirs(full_path, exist_ok=True)
            print(f"✅ Created: {full_path}")
            return full_path

        elif choice == "existing":
            path = input("📁 Enter destination folder path: ").strip()
            if os.path.isdir(path):
                return path
            print("❌ Folder not found. Try again.\n")

        else:
            print("❌ Type 'new' or 'existing' only.\n")


def run_cli():
    try:
        source = get_source_folder()
        dest = get_dest_folder()
        
        while True:
            choice = input("\nSelect operation mode — copy or move? (copy/move) [default: copy]: ").strip().lower()
            if not choice:
                mode = "copy"
                break
            elif choice in ("copy", "move"):
                mode = choice
                break
            else:
                print("❌ Type 'copy' or 'move' or press Enter.")

        while True:
            choice = input("\nScan subfolders too? (yes/no) [default: no]: ").strip().lower()
            if not choice or choice in ("no", "n"):
                recursive = False
                break
            elif choice in ("yes", "y"):
                recursive = True
                break
            else:
                print("❌ Type 'yes' or 'no' or press Enter.")

        organize_files(source, dest, mode=mode, recursive=recursive)
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled.")
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean-That-Mess: Organize files into folders by type.")
    parser.add_argument("--cli", action="store_true", help="Run in command-line interface mode")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        try:
            from gui import run_gui
            run_gui(organize_files)
        except ImportError as e:
            print(f"⚠️ Could not load GUI module (gui.py). Running CLI mode instead...\nReason: {e}")
            run_cli()
