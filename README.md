# Project Structure Generator

A command-line tool that converts AI-generated project architecture descriptions
(tree format or simple lists) into real files and folders on your system.

This tool is useful when working with AI tools (like ChatGPT) that describe
project structures but don’t actually create them.

---

## ✨ Features

- Supports **tree-style** structures (`├──`, `└──`)
- Supports **simple list** format
- Automatically creates folders and files
- Adds basic templates for:
  - `README.md`
  - `.gitignore`
- Detects project name from input
- Can open the project directly in **VS Code**
- Safe handling of existing directories (overwrite / merge / cancel)

---

## 📦 Example Input (Tree Format)

```text
MyApp/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── README.md
└── .gitignore
