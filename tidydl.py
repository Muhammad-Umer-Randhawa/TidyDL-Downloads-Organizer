from pathlib import Path
from datetime import datetime
from unicodedata import category
import shutil
import hashlib
import ctypes
import uuid
from ctypes import wintypes
CATEGORIES = {
    "Images": [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".heic", ".raw", ".ico", ".jfif"],
    "PDFs": [".pdf"],
    "Documents": [".docx", ".txt"],
    "Spreadsheets": [".xlsx", ".csv"],
    "Archives": [".zip", ".tar", ".gz"],
    "Executables": [".exe", ".bat", ".sh"],
    "Videos": [".mp4", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Presentations": [".pptx"],
    "Others": []
}

class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD), ("Data4", ctypes.c_ubyte * 8)]

    def __init__(self, guid_string):
        u = uuid.UUID(guid_string)
        super().__init__(u.time_low, u.time_mid, u.time_hi_version,
                         (ctypes.c_ubyte * 8).from_buffer_copy(u.bytes[8:]))

def get_downloads_folder():
    try:
        guid = GUID("{374DE290-123F-4565-9164-ACA4F1D4F2E7}")
        path_ptr = ctypes.c_wchar_p()
        result = ctypes.windll.shell32.SHGetKnownFolderPath(
            ctypes.byref(guid), 0, None, ctypes.byref(path_ptr))
        if result != 0:
            raise OSError("Windows could not find the Downloads folder")
        return Path(path_ptr.value)
    except Exception:
        return Path.home() / "Downloads"


def get_category(suffix):
    for category, extensions in CATEGORIES.items():
        if suffix.lower() in extensions:
            return category
    return "Others"

def get_file_hash(file_path):
    """Compute the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


# Step 1: Safely find the standard user "Downloads" folder across OS platforms
downloads_path = get_downloads_folder()

# Step 2: Verify the folder exists before proceeding
if downloads_path.exists() and downloads_path.is_dir():
    print(f"Looking inside: {downloads_path}\n")
    
    # Step 3: Loop through all items and display only the files
    moved_count = 0
    deleted_count = 0
    for item in downloads_path.iterdir():
        if item.is_file():
            if item.name.lower() == "desktop.ini":
                continue
            category = get_category(item.suffix)
            print(f"{item.name} -> {category}") 
            destination = downloads_path / category / item.name
            destination.parent.mkdir(exist_ok=True)
            if destination.exists():
                print(f"Name already taken: {item.name}")
                if get_file_hash(item) == get_file_hash(destination):
                    item.unlink()
                    deleted_count += 1
                    print(f"Duplicate deleted: {item.name}")
                else:
                    counter = 1
                    new_destination = destination.parent / f"{item.stem} ({counter}){item.suffix}"
                    is_duplicate = False

                    while new_destination.exists():
                        if get_file_hash(item) == get_file_hash(new_destination):
                            is_duplicate = True
                            break
                        counter += 1
                        new_destination = destination.parent / f"{item.stem} ({counter}){item.suffix}"

                    if is_duplicate:
                        item.unlink()
                        deleted_count += 1
                        print(f"Duplicate deleted: {item.name}")
                    else:
                        shutil.move(str(item), str(new_destination))
                        moved_count += 1
                        print(f"Moved as: {new_destination.name}")
            else:
                shutil.move(str(item), str(destination))
                moved_count += 1
    print(f"\nDone! Moved: {moved_count} | Duplicates deleted: {deleted_count}")
else:
    print("Could not find the Downloads folder at the standard location.")
