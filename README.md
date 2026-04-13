# Directory Sync Tool

## What this project does
A Python tool that compares two directories, identifies differences, and synchronizes them by copying updated files and optionally deleting extra files.

---

## Features implemented

- Recursively scans directories
- Collects file metadata:
  - Name
  - Extension(s)
  - Size (human-readable format)
  - SHA-256 hash
- Detects:
  - New files (only in source)
  - Modified files (based on size AND hash)
  - Missing files (only in destination)

---

## Synchronization Features

### Copy Operation
- Copies:
  - New files
  - Modified files
- Preserves file metadata (`shutil.copy2`)
- Automatically creates required directories

### Deletion Operation
- Deletes files in destination that do not exist in source
- Only deletes files (directories are not removed)

---

## How it works

1. User enters source directory
2. Metadata of source is displayed
3. User enters destination directory
4. Metadata of destination is displayed
5. Differences are shown:
   - New
   - Modified
   - Missing
6. User confirms synchronization (copy)
7. User confirms deletion of extra files

---

## Technical Details

- Uses `pathlib` for file handling
- Uses SHA-256 hashing for accurate comparison
- Reads files in chunks (memory efficient)
- Maintains relative directory structure during sync

---

## Limitations

- Directories are not deleted
- No dry-run mode (changes are applied after confirmation)
- Hashing may be slower for very large files

---

## Future Improvements

- Logging system for tracking changes
- CLI arguments instead of interactive input
