#!/usr/bin/env python3
"""
Validate VS Code extension package.json for duplicate commands and menu entries.

This script checks the package.json file for:
- Duplicate command IDs in the commands array
- Duplicate command titles
- Duplicate commands in each menu section

Exit code 0 indicates success (no duplicates found).
Exit code 1 indicates failure (duplicates found).
"""

import json
import sys
import argparse
from collections import Counter
from pathlib import Path


def validate_package_json(package_json_path: Path) -> bool:
    """
    Validate package.json for duplicate commands.
    
    Returns True if valid (no duplicates), False otherwise.
    """
    with open(package_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    has_errors = False
    
    # Check for duplicate command IDs
    commands = data.get('contributes', {}).get('commands', [])
    command_ids = [c.get('command') for c in commands]
    duplicates = [item for item, count in Counter(command_ids).items() if count > 1]
    
    if duplicates:
        print(f'ERROR: Duplicate command IDs found: {duplicates}', file=sys.stderr)
        has_errors = True
    
    # Check for duplicate titles
    titles = [c.get('title') for c in commands]
    dup_titles = [item for item, count in Counter(titles).items() if count > 1]
    
    if dup_titles:
        print(f'ERROR: Duplicate command titles found: {dup_titles}', file=sys.stderr)
        has_errors = True
    
    # Check menu entries for duplicates
    menus = data.get('contributes', {}).get('menus', {})
    for menu_name, items in menus.items():
        menu_cmds = [i.get('command') for i in items if 'command' in i]
        dup_menu = [item for item, count in Counter(menu_cmds).items() if count > 1]
        if dup_menu:
            print(f'ERROR: Duplicate menu commands in {menu_name}: {dup_menu}', file=sys.stderr)
            has_errors = True
    
    if not has_errors:
        print(f'✓ Validated {len(commands)} commands with no duplicates')
    
    return not has_errors


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Validate VS Code extension package.json for duplicates'
    )
    parser.add_argument(
        '--package-json',
        type=str,
        default='xrcg_vscode/package.json',
        help='Path to package.json (default: xrcg_vscode/package.json)'
    )
    
    args = parser.parse_args()
    package_json_path = Path(args.package_json)
    
    if not package_json_path.exists():
        print(f'ERROR: Package.json not found at {package_json_path}', file=sys.stderr)
        return 1
    
    if validate_package_json(package_json_path):
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
