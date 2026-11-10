# TidyDL

A small Windows tool that keeps your Downloads folder tidy.

## What it does
- Sorts files into folders by type (Images, PDFs, Documents, Archives, and more)
- Deletes exact duplicates (same name and same content)
- Keeps both files when the name matches but the content differs, numbering the new one: `report (1).pdf`
- Finds your real Downloads folder, even if it was moved
- Prints a short summary of what it did

## How to use
1. Download `tidydl.exe` from the Releases page.
2. Double-click it, and your Downloads folder gets sorted.
3. To run it automatically, put a shortcut to it in the Startup folder (Windows key + R, type `shell:startup`).

## Run from source
Requires Python 3.

    python tidydl.py

## Build the .exe
    pip install pyinstaller
    pyinstaller --onefile --noconsole tidydl.