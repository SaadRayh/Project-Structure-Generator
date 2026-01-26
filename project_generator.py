#!/usr/bin/env python3
"""
Project Structure Generator
Converts AI-generated architecture descriptions into actual file/folder structures
"""

import os
import sys
from pathlib import Path
import re
import subprocess
import platform


class ProjectGenerator:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.created_items = {"folders": [], "files": []}
    
    def parse_tree_structure(self, tree_text, skip_root=True):
        """
        Parse tree-style architecture (like your example with ├── and └──)
        Returns a list of (path, is_file) tuples
        """
        lines = tree_text.strip().split('\n')
        items = []
        path_stack = []
        first_item = True
        
        for line in lines:
            # Remove tree characters and get the item name
            cleaned = re.sub(r'[│├└─\s]+', '', line)
            if not cleaned:
                continue
            
            # Count indentation level
            indent = len(line) - len(line.lstrip('│├└─ \t'))
            indent_level = indent // 4  # Approximate indentation level
            
            # Determine if it's a file or folder
            is_file = '.' in cleaned and not cleaned.endswith('/')
            item_name = cleaned.rstrip('/')
            
            # Skip the root folder (first line with the project name)
            if first_item and skip_root:
                first_item = False
                continue
            
            # Build the path based on indentation
            if indent_level == 0:
                current_path = item_name
                path_stack = [item_name]
            else:
                # Adjust for skipped root
                adjusted_level = indent_level - 1 if skip_root else indent_level
                path_stack = path_stack[:adjusted_level]
                path_stack.append(item_name)
                current_path = '/'.join(path_stack)
            
            items.append((current_path, is_file))
        
        return items
    
    def parse_simple_list(self, text, skip_root=True):
        """
        Parse simple list format like:
        folder1/
        folder1/file1.py
        folder2/subfolder/
        """
        items = []
        root_name = None
        
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Detect root folder (first line without /)
            if root_name is None and skip_root:
                root_name = line.rstrip('/')
                continue
            
            is_file = not line.endswith('/')
            path = line.rstrip('/')
            
            # Remove root prefix if present
            if skip_root and root_name and path.startswith(root_name + '/'):
                path = path[len(root_name) + 1:]
            elif skip_root and root_name and path == root_name:
                continue
            
            if path:  # Only add non-empty paths
                items.append((path, is_file))
        
        return items
    
    def create_structure(self, items):
        """Create the actual files and folders"""
        for path, is_file in items:
            full_path = self.base_path / path
            
            try:
                if is_file:
                    # Create parent directories if needed
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    # Create empty file
                    full_path.touch(exist_ok=True)
                    self.created_items["files"].append(str(full_path))
                    print(f"✓ Created file: {path}")
                else:
                    # Create directory
                    full_path.mkdir(parents=True, exist_ok=True)
                    self.created_items["folders"].append(str(full_path))
                    print(f"✓ Created folder: {path}/")
            except Exception as e:
                print(f"✗ Error creating {path}: {e}")
    
    def add_template_content(self, filepath, template_type):
        """Add basic template content to common file types"""
        templates = {
            'README.md': """# Project Name

## Description
Add your project description here.

## Installation
```bash
# Installation instructions
```

## Usage
```bash
# Usage instructions
```
""",
            '.gitignore': """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
""",
            'activate_env.sh': """#!/bin/bash
source venv/bin/activate
echo "Virtual environment activated"
""",
            'deactivate_env.sh': """#!/bin/bash
deactivate
echo "Virtual environment deactivated"
""",
        }
        
        filename = Path(filepath).name
        if filename in templates:
            with open(filepath, 'w') as f:
                f.write(templates[filename])
            print(f"  → Added template content to {filename}")
    
    def generate_report(self):
        """Print summary of created structure"""
        print("\n" + "="*50)
        print("PROJECT STRUCTURE CREATED")
        print("="*50)
        print(f"Folders created: {len(self.created_items['folders'])}")
        print(f"Files created: {len(self.created_items['files'])}")
        print("\nStructure:")
        self.print_tree(self.base_path)
    
    def print_tree(self, directory, prefix="", is_last=True):
        """Print directory tree structure"""
        items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
        
        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1
            current_prefix = "└── " if is_last_item else "├── "
            print(f"{prefix}{current_prefix}{item.name}{'/' if item.is_dir() else ''}")
            
            if item.is_dir() and list(item.iterdir()):
                extension = "    " if is_last_item else "│   "
                self.print_tree(item, prefix + extension, is_last_item)


def open_in_vscode(project_path):
    """Try to open the project in VS Code"""
    try:
        # Try to open with 'code' command
        subprocess.run(['code', str(project_path)], check=True)
        print(f"\nOpened project in VS Code!")
        return True
    except subprocess.CalledProcessError:
        print(f"\nVS Code command failed")
        return False
    except FileNotFoundError:
        print(f"\nVS Code 'code' command not found in PATH")
        print("You can open the project manually in VS Code")
        return False


def show_example():
    """Display example formats for user"""
    print("\n" + "="*60)
    print("EXAMPLE INPUT FORMATS")
    print("="*60)
    print("\nFormat 1: Tree Format (recommended)")
    print("-" * 60)
    print("""MyCoolApp/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_basic.py
├── docs/
├── venv/
├── README.md
├── .gitignore
└── requirements.txt""")
    
    print("\nFormat 2: Simple List Format")
    print("-" * 60)
    print("""MyCoolApp/
src/
src/main.py
src/utils.py
tests/
tests/test_basic.py
docs/
venv/
README.md
.gitignore
requirements.txt""")
    print("="*60 + "\n")


def main():
    print("Project Structure Generator")
    print("="*60)
    
    # Show examples
    show_example()
    
    print("Paste your project architecture below (including project name as root folder).")
    print("Press Ctrl+D (Unix/Mac) or Ctrl+Z then Enter (Windows) when done:\n")
    
    # Read multi-line input
    architecture = sys.stdin.read().strip()
    
    if not architecture:
        print("Error: No architecture provided.")
        sys.exit(1)
    
    # Extract project name from first line
    first_line = architecture.split('\n')[0].strip()
    # Remove tree characters and trailing slash
    project_name = re.sub(r'[│├└─\s/]+', '', first_line).strip('/')
    
    if not project_name:
        project_name = "MyCoolApp"
    
    # Check if project already exists
    project_path = Path.cwd() / project_name
    
    if project_path.exists():
        print(f"\nWARNING: Directory '{project_name}' already exists!")
        print(f"Location: {project_path.absolute()}")
        choice = input("\nWhat would you like to do?\n"
                     "  1. Choose a different name\n"
                     "  2. Overwrite existing directory (CAUTION!)\n"
                     "  3. Merge with existing directory\n"
                     "  4. Cancel\n"
                     "Enter choice (1-4): ").strip()
        choice = input("\nWhat would you like to do?\n"
                     "  1. Choose a different name\n"
                     "  2. Overwrite existing directory (CAUTION!)\n"
                     "  3. Merge with existing directory\n"
                     "  4. Cancel\n"
                     "Enter choice (1-4): ").strip()
        
        if choice == '1':
            new_name = input("Enter new project name: ").strip()
            if new_name:
                project_name = new_name
                project_path = Path.cwd() / project_name
                # Check again if new name exists
                if project_path.exists():
                    print(f"Directory '{project_name}' also exists. Please try again.")
                    sys.exit(1)
        elif choice == '2':
            confirm = input(f"Are you SURE you want to delete '{project_name}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                import shutil
                shutil.rmtree(project_path)
                print(f"Deleted existing directory")
            else:
                print("Overwrite cancelled.")
                sys.exit(0)
        elif choice == '3':
            print(f"Will merge with existing directory")
        elif choice == '4':
            print("Operation cancelled.")
            sys.exit(0)
        else:
            print("Invalid choice. Operation cancelled.")
            sys.exit(1)
    
    print(f"\nProject name detected: {project_name}")
    print(f"Creating project structure...\n")
    
    # Create generator
    generator = ProjectGenerator(project_name)
    
    # Auto-detect format and parse
    if '├──' in architecture or '└──' in architecture:
        print("\nDetected tree format...")
        items = generator.parse_tree_structure(architecture)
    else:
        print("\nDetected simple list format...")
        items = generator.parse_simple_list(architecture)
    
    # Create structure
    print(f"\nCreating project structure in: {project_name}/\n")
    generator.create_structure(items)
    
    # Add template content to common files
    for filepath, is_file in items:
        if is_file:
            full_path = generator.base_path / filepath
            generator.add_template_content(full_path, Path(filepath).name)
    
    # Generate report
    generator.generate_report()
    
    # Show full path
    print("\n" + "="*60)
    print("PROJECT LOCATION")
    print("="*60)
    print(f"Full path: {project_path.absolute()}")
    print("="*60)
    
    # Ask if user wants to open in VS Code
    print(f"\nProject '{project_name}' created successfully!")
    open_choice = input("\nDo you want to open this project in VS Code? (y/n): ").strip().lower()
    
    if open_choice in ['y', 'yes']:
        open_in_vscode(project_path.absolute())


if __name__ == "__main__":
    main()