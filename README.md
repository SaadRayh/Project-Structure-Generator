# Project Structure Generator

Creates any project structure from a tree diagram. All files are created **empty** - no content added.

## Quick Start

```bash
python3 projstruct.py
```

1. Enter project name
2. Paste your tree structure
3. Press Enter twice
4. Done!

## Example

**Input:**
```
modern_lms/
├── lib/
│   ├── main.dart
│   ├── theme/
│   │   └── app_theme.dart
│   └── screens/
│       ├── splash_screen.dart
│       └── login_screen.dart
├── test/
│   └── widget_test.dart
└── pubspec.yaml
```

**Creates:**
```
my_project/
├── lib/
│   ├── main.dart              (empty file)
│   ├── theme/
│   │   └── app_theme.dart     (empty file)
│   └── screens/
│       ├── splash_screen.dart (empty file)
│       └── login_screen.dart  (empty file)
├── test/
│   └── widget_test.dart       (empty file)
└── pubspec.yaml               (empty file)
```

## Tree Format

- `/` at end = folder
- File has extension (like `.dart`, `.py`, `.js`)
- `├──` = more items below
- `└──` = last item
- `│` = continuation line
- `#` = comment (ignored)

## What You Get

- Empty folders
- Empty files
- Nothing else


## Features

- Works with any language
- All files created empty
- Opens in VS Code automatically
- Simple and fast

---

Save time creating folders and files. That's it.
