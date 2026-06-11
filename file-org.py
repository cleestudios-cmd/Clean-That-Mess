import os
import shutil


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


SOURCE_FOLDER = get_source_folder()
DEST_FOLDER   = get_dest_folder()

# Photo extensions → go into PHOTOS/<ext>/
PHOTO_TYPES = {"jpg", "jpeg", "png", "heic", "webp", "gif", "bmp", "tiff", "raw"}

# Everything else → folder named after type (uppercase)
# Add or remove as needed
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


def organize():
    copied  = 0
    skipped = 0
    unknown = 0

    print(f"\n📂 Scanning: {SOURCE_FOLDER}\n")

    for filename in os.listdir(SOURCE_FOLDER):
        source_path = os.path.join(SOURCE_FOLDER, filename)

        # Skip subfolders
        if not os.path.isfile(source_path):
            continue

        # Get extension (lowercase, no dot)
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        # Determine destination subfolder
        if ext in PHOTO_TYPES:
            dest_subfolder = os.path.join(DEST_FOLDER, "PHOTOS", ext.upper())
        elif ext in OTHER_TYPES:
            dest_subfolder = os.path.join(DEST_FOLDER, OTHER_TYPES[ext])
        else:
            dest_subfolder = os.path.join(DEST_FOLDER, "OTHERS")
            unknown += 1

        # Create destination folder if it doesn't exist
        os.makedirs(dest_subfolder, exist_ok=True)

        dest_path = os.path.join(dest_subfolder, filename)

        # Skip if file already exists at destination
        if os.path.exists(dest_path):
            print(f"⏭️  Skipped (already exists): {filename}")
            skipped += 1
            continue

        # Copy file with metadata preserved
        shutil.copy2(source_path, dest_path)
        print(f"✅ Copied: {filename}  →  {dest_subfolder}")
        copied += 1

    print(f"\n─────────────────────────────")
    print(f"✅ Copied:   {copied} file(s)")
    print(f"⏭️  Skipped:  {skipped} file(s)")
    print(f"📦 Unknown:  {unknown} file(s) → OTHERS/")
    print(f"─────────────────────────────\n")


organize()
