#!/usr/bin/env python3
"""
Generate commands.json from template directories and _templateinfo.json files.

This script scans the xregistry/templates directory structure and generates
a commands.json file that can be used by the CLI and VS Code extension.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


# Language group mappings
LANGUAGE_GROUPS = {
    'py': 'python',
    'ts': 'typescript',
    'cs': 'csharp',
    'java': 'java',
    'asyncapi': 'asyncapi',
    'openapi': 'openapi',
    'asaql': 'azure-stream-analytics'
}

# Standard arguments for generate commands
STANDARD_ARGS = [
    {"name": "input", "type": "str", "help": "Input file path"},
    {"name": "--output", "type": "str", "help": "Output directory"}
]

# File extensions
STANDARD_EXTENSIONS = [".xreg.json"]


def find_template_styles(templates_dir: Path) -> List[Dict[str, Any]]:
    """
    Scan the templates directory and find all language/style combinations.
    
    Returns a list of dicts with language, style, and templateinfo data.
    """
    template_styles = []
    
    # Iterate through language directories
    for language_dir in templates_dir.iterdir():
        if not language_dir.is_dir():
            continue
        
        language_name = language_dir.name
        
        # Skip special directories
        if language_name.startswith('_'):
            continue
        
        # Read language-level templateinfo if it exists
        language_info_path = language_dir / '_templateinfo.json'
        language_info = {}
        if language_info_path.exists():
            with open(language_info_path, 'r', encoding='utf-8') as f:
                language_info = json.load(f)
        
        # Iterate through style directories
        for style_dir in language_dir.iterdir():
            if not style_dir.is_dir():
                continue
            
            style_name = style_dir.name
            
            # Skip special directories
            if style_name.startswith('_'):
                continue
            
            # Read style-level templateinfo
            style_info_path = style_dir / '_templateinfo.json'
            style_info = {}
            if style_info_path.exists():
                with open(style_info_path, 'r', encoding='utf-8') as f:
                    style_info = json.load(f)
            
            # Combine language and style info
            template_styles.append({
                'language': language_name,
                'style': style_name,
                'language_info': language_info,
                'style_info': style_info
            })
    
    return template_styles


def generate_command_entry(template_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a command entry for commands.json from template data.
    """
    language = template_data['language']
    style = template_data['style']
    style_info = template_data['style_info']
    
    # Get description from style_info or construct from language/style
    description = style_info.get('description', f"Generate {language.upper()} {style}")
    
    # Construct command name
    command_name = f"generate-{language}-{style}"
    
    # Get group name
    group = LANGUAGE_GROUPS.get(language, language)
    
    # Get priority (default to 100)
    priority = style_info.get('priority', 100)
    
    # Construct suggested output path
    suggested_output = f"{{input_file_name}}-{language}-{style}"
    
    return {
        "command": command_name,
        "description": description,
        "extensions": STANDARD_EXTENSIONS.copy(),
        "group": group,
        "language": language,
        "style": style,
        "priority": priority,
        "args": STANDARD_ARGS.copy(),
        "prompts": [],
        "suggested_output_file_path": suggested_output
    }


def main():
    """Main function to generate commands.json"""
    # Determine paths
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    templates_dir = root_dir / 'xregistry' / 'templates'
    output_file = root_dir / 'xregistry' / 'commands.json'
    
    if not templates_dir.exists():
        print(f"Error: Templates directory not found at {templates_dir}")
        return 1
    
    print(f"Scanning templates in: {templates_dir}")
    
    # Find all template styles
    template_styles = find_template_styles(templates_dir)
    
    print(f"Found {len(template_styles)} template styles")
    
    # Generate command entries
    commands = []
    for template_data in template_styles:
        command_entry = generate_command_entry(template_data)
        commands.append(command_entry)
        print(f"  - {command_entry['command']}: {command_entry['description']}")
    
    # Sort commands by priority (ascending), then by command name
    commands.sort(key=lambda x: (x['priority'], x['command']))
    
    # Write commands.json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(commands, f, indent=2)
    
    print(f"\nGenerated {len(commands)} commands")
    print(f"Output written to: {output_file}")
    
    return 0


if __name__ == '__main__':
    exit(main())
