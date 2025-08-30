#!/usr/bin/env python3
import os

# Path to your dump
DUMP_DIR = "/home/adityas/Downloads/dump"

# Path to proprietary-files.txt
PROP_FILE = "proprietary-files.txt"

def clean_line(line: str) -> str:
    """Clean a line from proprietary-files.txt (remove comments, trailing parts)."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    # Handle entries like "src:dst"
    if ":" in line:
        line = line.split(":")[0]

    # Remove optional flags (e.g., ;PRESIGNED,;vNDK,;SHARED_LIBRARIES)
    if ";" in line:
        line = line.split(";")[0]

    return line.strip()

def main():
    missing = []
    existing = []

    with open(PROP_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for raw_line in lines:
        entry = clean_line(raw_line)
        if not entry:
            continue

        file_path = os.path.join(DUMP_DIR, entry)

        if os.path.exists(file_path):
            existing.append(entry)
        else:
            missing.append(entry)

    print("\n✅ Existing files:", len(existing))
    for f in existing:
        print("  ", f)

    print("\n❌ Missing files:", len(missing))
    for f in missing:
        print("  ", f)

    # Optionally write missing.txt for cleanup
    with open("missing-proprietary-files.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(missing))
    print("\nReport written to missing-proprietary-files.txt")

if __name__ == "__main__":
    main()

