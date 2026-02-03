import os
import subprocess
import sys
import shutil
import re
from pathlib import Path


def get_project_name():
    """Prompt for project name."""
    print("\n" + "="*50)
    print("   ProjStruct - Universal Project Scaffolder")
    print("="*50 + "\n")
    
    while True:
        name = input("Project name: ").strip()
        if not name:
            print("ERROR: Project name cannot be empty.")
        elif os.path.exists(name):
            print(f"ERROR: Folder '{name}' already exists.")
        else:
            return name


def get_tree_input():
    """Get tree structure from user."""
    print("\nPaste your project structure (tree format).")
    print("Press Enter twice when done:\n")
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if not line.strip():
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break
    
    tree_text = '\n'.join(lines)
    
    # Validate that this looks like a tree structure, not code
    if tree_text.strip():
        code_indicators = [
            'def ', 'class ', 'import ', 'function ', 'const ', 'let ', 'var ',
            '#!/usr/bin', 'if __name__', 'public class', 'void main'
        ]
        
        if any(indicator in tree_text for indicator in code_indicators):
            print("\nERROR: This looks like code, not a project structure.")
            print("Please paste a tree structure like:")
            print("  lib/")
            print("    main.dart")
            print("  test/")
            print("    test.dart\n")
            return None
    
    return tree_text


def parse_tree_structure(tree_text):
    """
    Parse a tree structure into properly nested paths.
    No content added to files - just creates the structure.
    """
    lines = tree_text.strip().split('\n')
    paths = []
    dir_stack = []
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        
        # Measure indent by replacing tree chars with spaces
        line_normalized = line.replace('├──', '   ').replace('└──', '   ').replace('│', ' ').replace('─', ' ')
        indent = len(line_normalized) - len(line_normalized.lstrip())
        
        # Extract the name
        cleaned = re.sub(r'^[│├└─\s]+', '', line).strip()
        
        if not cleaned or cleaned.startswith('#'):
            continue
        
        # Remove comments (everything after # until double space or end)
        if '#' in cleaned:
            cleaned = cleaned.split('#')[0].strip()
        
        if not cleaned:
            continue
        
        # Check if directory (ends with /)
        is_dir = cleaned.endswith('/')
        name = cleaned.rstrip('/')
        
        # Skip project root (first line that's a single dir)
        if i == 0 and is_dir and '/' not in name:
            continue
        
        # Pop directories from stack that are at same or deeper level
        while dir_stack and dir_stack[-1][0] >= indent:
            dir_stack.pop()
        
        # Build full path from stack
        if dir_stack:
            path_parts = [d[1] for d in dir_stack] + [name]
            full_path = '/'.join(path_parts)
        else:
            full_path = name
        
        # Add to results
        if is_dir:
            paths.append(full_path + '/')
            dir_stack.append((indent, name))
        else:
            paths.append(full_path)
    
    return paths


def create_structure(project_name, paths):
    """Create folders and empty files from parsed paths."""
    print(f"\nCreating project structure...")
    
    created_files = []
    created_dirs = []
    
    for path in paths:
        full_path = os.path.join(project_name, path)
        
        # Check if it's a directory
        is_dir = path.endswith('/')
        
        if is_dir:
            # Create directory
            path_clean = path.rstrip('/')
            full_path = os.path.join(project_name, path_clean)
            os.makedirs(full_path, exist_ok=True)
            created_dirs.append(path_clean)
        else:
            # Create file (empty)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                pass  # Create empty file
            created_files.append(path)
    
    print(f"   Created {len(created_dirs)} directories")
    print(f"   Created {len(created_files)} files")
    
    return True


def open_in_vscode(project_name):
    """Open the project in VS Code."""
    try:
        subprocess.run(["code", project_name], check=True)
        print(f"\nOpened '{project_name}' in VS Code!")
        return True
    except FileNotFoundError:
        print("\nWARNING: VS Code ('code' command) not found.")
        return False
    except Exception:
        print("\nWARNING: Couldn't open VS Code automatically.")
        return False


def print_success(project_name, vscode_opened):
    """Print success message."""
    print("\n" + "="*50)
    print(f"Project '{project_name}' created successfully!")
    print("="*50)
    
    if not vscode_opened:
        print(f"\nNext steps:")
        print(f"   1. cd {project_name}")
        print(f"   2. Open in your editor (e.g., code .)")
        print(f"   3. Start adding your code!")
    
    print("\nAll files created empty - ready for your code!\n")


def main():
    """Main function."""
    try:
        # Get project details
        project_name = get_project_name()
        tree_text = get_tree_input()
        
        # Check if input validation failed
        if tree_text is None:
            print("Please try again with a valid project structure.")
            sys.exit(1)
        
        if not tree_text.strip():
            print("\nERROR: No structure provided. Exiting.")
            sys.exit(1)
        
        # Parse structure
        paths = parse_tree_structure(tree_text)
        
        if not paths:
            print("\nERROR: Could not parse project structure.")
            print("Make sure you're using a tree format with file/folder names.")
            sys.exit(1)
        
        print(f"   Found {len(paths)} items to create")
        
        # Ask about VS Code
        open_vscode = input("\nOpen in VS Code when done? (y/n): ").strip().lower() == 'y'
        
        # Create project
        os.makedirs(project_name, exist_ok=True)
        
        create_structure(project_name, paths)
        
        # Open in VS Code
        vscode_opened = False
        if open_vscode:
            vscode_opened = open_in_vscode(project_name)
        
        # Success message
        print_success(project_name, vscode_opened)
        
    except KeyboardInterrupt:
        print("\n\nERROR: Cancelled by user.")
        if 'project_name' in locals() and os.path.exists(project_name):
            shutil.rmtree(project_name)
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        if 'project_name' in locals() and os.path.exists(project_name):
            shutil.rmtree(project_name)
        sys.exit(1)


if __name__ == "__main__":
    main()
