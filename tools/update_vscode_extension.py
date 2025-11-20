#!/usr/bin/env python3
"""
Update VS Code extension project based on commands.json.

This script reads xregistry/commands.json and generates:
1. The commands section in xregistry_vscode/package.json
2. The menus/submenus sections in xregistry_vscode/package.json
3. Optionally updates src/extension.ts with command handlers

Based on tools/editvscodeext.py from clemensv/avrotize
"""

import json
import os
import subprocess
import argparse
from typing import List, Dict
from pathlib import Path

INDENT = '    '


def get_latest_git_tag() -> str:
    """Get the latest git tag for versioning."""
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            check=True
        )
        tag = result.stdout.strip()
        # Remove 'v' prefix if present
        if tag.startswith('v'):
            tag = tag[1:]
        return tag
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0.13.0"  # fallback version


def clip_command_description(command_description: str) -> str:
    """
    Clip 'Generate' prefix from command description for menu display.
    """
    if command_description.startswith('Generate '):
        command_description = command_description[9:]  # Remove 'Generate '
    return command_description


def update_package_json(package_json_path: Path, commands: List[Dict]) -> None:
    """
    Update package.json with commands and menus from commands.json.
    """
    with open(package_json_path, 'r', encoding='utf-8') as file:
        package_json = json.load(file)
    
    # Update version
    latest_version = get_latest_git_tag()
    package_json['version'] = latest_version
    print(f"Setting version to: {latest_version}")
    
    # Group commands by language/group
    groups = {}
    all_extensions = set()
    
    for command in commands:
        group = command['group']
        all_extensions.update(command.get('extensions', ['.xreg.json']))
        
        if group not in groups:
            groups[group] = []
        
        groups[group].append(command)
    
    # Generate commands section
    package_json['contributes']['commands'] = []
    for command in commands:
        cmd_id = f"xrcg.{command['command']}"
        title = clip_command_description(command['description'])
        
        package_json['contributes']['commands'].append({
            "category": "XRegistry",
            "command": cmd_id,
            "title": title
        })
    
    # Generate submenus for each group
    submenus = []
    menu_entries = {}
    
    # Define group display names and order
    group_names = {
        'python': {'label': 'Python', 'id': 'xrcg.py'},
        'typescript': {'label': 'TypeScript', 'id': 'xrcg.ts'},
        'csharp': {'label': 'C#', 'id': 'xrcg.cs'},
        'java': {'label': 'Java', 'id': 'xrcg.java'},
        'asyncapi': {'label': 'AsyncAPI', 'id': 'xrcg.asyncapi'},
        'openapi': {'label': 'OpenAPI', 'id': 'xrcg.openapi'},
        'azure-stream-analytics': {'label': 'Azure Stream Analytics', 'id': 'xrcg.asaql'}
    }
    
    # Create submenu entries for each group
    for group_key, group_data in group_names.items():
        if group_key in groups:
            submenu_id = group_data['id']
            
            # Add to submenus list
            submenus.append({
                "id": submenu_id,
                "label": group_data['label']
            })
            
            # Create menu entries for this submenu
            menu_entries[submenu_id] = []
            
            for command in sorted(groups[group_key], key=lambda x: x['description']):
                cmd_id = f"xrcg.{command['command']}"
                title = clip_command_description(command['description'])
                ext_conditions = " || ".join([f"resourceExtname == {ext}" for ext in command.get('extensions', ['.xreg.json'])])
                
                menu_entries[submenu_id].append({
                    "title": title,
                    "command": cmd_id,
                    "when": f"resourceExtname == .json"
                })
    
    # Update package.json menus section
    package_json['contributes']['menus'] = {}
    
    # Add main submenu to explorer context
    ext_condition = " || ".join([f"resourceExtname == {ext}" for ext in all_extensions])
    package_json['contributes']['menus']['explorer/context'] = [
        {
            "submenu": "xrcgSubmenu",
            "group": "8_transformation",
            "title": "Generate Code",
            "when": "resourceExtname == .json"
        }
    ]
    
    # Add submenu entries to xrcgSubmenu
    package_json['contributes']['menus']['xrcgSubmenu'] = []
    for submenu_id, submenu_data in [(gd['id'], gd['label']) for gd in [group_names[g] for g in group_names if g in groups]]:
        package_json['contributes']['menus']['xrcgSubmenu'].append({
            "submenu": submenu_id,
            "title": submenu_data,
            "when": "resourceExtname == .json"
        })
    
    # Add command entries to each language submenu
    for submenu_id, entries in menu_entries.items():
        package_json['contributes']['menus'][submenu_id] = entries
    
    # Update submenus section
    package_json['contributes']['submenus'] = [
        {"id": "xrcgSubmenu", "label": "Generate Code"}
    ]
    package_json['contributes']['submenus'].extend(submenus)
    
    # Write updated package.json
    with open(package_json_path, 'w', encoding='utf-8') as file:
        json.dump(package_json, file, indent=2)
    
    print(f"Updated package.json with {len(commands)} commands in {len(groups)} groups")


def generate_extension_ts(extension_ts_path: Path, commands: List[Dict]) -> None:
    """
    Generate src/extension.ts with command handlers.
    """
    extension_ts_content = []
    
    # Header
    extension_ts_content.extend([
        "import * as vscode from 'vscode';",
        "import { exec } from 'child_process';",
        "import * as path from 'path';",
        "import * as fs from 'fs';",
        "",
        "const currentVersionMajor = 0;",
        "const currentVersionMinor = 13;",
        "const currentVersionPatch = 0;",
        "",
        "async function checkXRegistryTool(context: vscode.ExtensionContext, outputChannel: vscode.OutputChannel): Promise<boolean> {",
        f"{INDENT}// Check if xregistry CLI is available",
        f"{INDENT}try {{",
        f"{INDENT*2}return await execShellCommand('xrcg --version', outputChannel)",
        f"{INDENT*3}.then((stdout) => {{",
        f"{INDENT*4}const versionMatch = stdout.match(/(\\d+)\\.(\\d+)\\.(\\d+)/);",
        f"{INDENT*4}if (!versionMatch) {{",
        f"{INDENT*5}return false;",
        f"{INDENT*4}}}",
        f"{INDENT*4}const major = parseInt(versionMatch[1]);",
        f"{INDENT*4}const minor = parseInt(versionMatch[2]);",
        f"{INDENT*4}const patch = parseInt(versionMatch[3]);",
        f"{INDENT*4}if (major < currentVersionMajor) {{",
        f"{INDENT*5}vscode.window.showWarningMessage('xregistry tool version is outdated. Please update.');",
        f"{INDENT*5}return false;",
        f"{INDENT*4}}}",
        f"{INDENT*4}return true;",
        f"{INDENT*3}}})",
        f"{INDENT*3}.catch(async (error) => {{",
        f"{INDENT*4}const installOption = await vscode.window.showWarningMessage(",
        f"{INDENT*5}'xregistry tool is not available. Do you want to install it?', 'Yes', 'No');",
        f"{INDENT*4}if (installOption === 'Yes') {{",
        f"{INDENT*5}await execShellCommand('pip install xrcg', outputChannel);",
        f"{INDENT*5}vscode.window.showInformationMessage('xregistry tool has been installed successfully.');",
        f"{INDENT*5}return true;",
        f"{INDENT*4}}}",
        f"{INDENT*4}return false;",
        f"{INDENT*3}}});",
        f"{INDENT}}} catch (error) {{",
        f"{INDENT*2}vscode.window.showErrorMessage('Error checking xregistry tool availability: ' + error);",
        f"{INDENT*2}return false;",
        f"{INDENT}}}",
        "}",
        "",
        "function execShellCommand(cmd: string, outputChannel?: vscode.OutputChannel): Promise<string> {",
        f"{INDENT}return new Promise((resolve, reject) => {{",
        f"{INDENT*2}const process = exec(cmd, (error, stdout, stderr) => {{",
        f"{INDENT*3}if (error) {{",
        f"{INDENT*4}reject(error);",
        f"{INDENT*3}}} else {{",
        f"{INDENT*4}resolve(stdout ? stdout : stderr);",
        f"{INDENT*3}}}",
        f"{INDENT*2}}});",
        f"{INDENT*2}if (outputChannel) {{",
        f"{INDENT*3}process.stdout?.on('data', (data) => {{",
        f"{INDENT*4}outputChannel.append(data.toString());",
        f"{INDENT*3}}});",
        f"{INDENT*3}process.stderr?.on('data', (data) => {{",
        f"{INDENT*4}outputChannel.append(data.toString());",
        f"{INDENT*3}}});",
        f"{INDENT*2}}}",
        f"{INDENT}}});",
        "}",
        "",
        "function executeCommand(command: string, outputPath: vscode.Uri | null, outputChannel: vscode.OutputChannel) {",
        f"{INDENT}exec(command, (error, stdout, stderr) => {{",
        f"{INDENT*2}if (error) {{",
        f"{INDENT*3}outputChannel.appendLine(`Error: ${{error.message}}`);",
        f"{INDENT*3}vscode.window.showErrorMessage(`Error: ${{stderr}}`);",
        f"{INDENT*2}}} else {{",
        f"{INDENT*3}outputChannel.appendLine(stdout);",
        f"{INDENT*3}if (outputPath) {{",
        f"{INDENT*4}if (fs.existsSync(outputPath.fsPath)) {{",
        f"{INDENT*5}const stats = fs.statSync(outputPath.fsPath);",
        f"{INDENT*5}if (stats.isFile()) {{",
        f"{INDENT*6}vscode.workspace.openTextDocument(outputPath).then((document) => {{",
        f"{INDENT*7}vscode.window.showTextDocument(document);",
        f"{INDENT*6}}});",
        f"{INDENT*5}}} else if (stats.isDirectory()) {{",
        f"{INDENT*6}vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(outputPath.fsPath), true);",
        f"{INDENT*5}}}",
        f"{INDENT*4}}}",
        f"{INDENT*3}}} else {{",
        f"{INDENT*4}vscode.workspace.openTextDocument({{ content: stdout }}).then((document) => {{",
        f"{INDENT*5}vscode.window.showTextDocument(document);",
        f"{INDENT*4}}});",
        f"{INDENT*3}}}",
        f"{INDENT*3}vscode.window.showInformationMessage(`Success: ${{stdout}}`);",
        f"{INDENT*2}}}",
        f"{INDENT}}});",
        "}",
        "",
        "export function activate(context: vscode.ExtensionContext) {",
        f"{INDENT}const disposables: vscode.Disposable[] = [];",
        f"{INDENT}(async () => {{",
        f"{INDENT*2}const outputChannel = vscode.window.createOutputChannel('xregistry');",
        ""
    ])
    
    # Generate command handlers
    for command in commands:
        cmd_id = command['command']
        language = command['language']
        style = command['style']
        
        extension_ts_content.append(f"{INDENT*2}disposables.push(vscode.commands.registerCommand('xrcg.{cmd_id}', async (uri: vscode.Uri) => {{")
        extension_ts_content.append(f"{INDENT*3}if (!await checkXRegistryTool(context, outputChannel)) {{ return; }}")
        extension_ts_content.append(f"{INDENT*3}const filePath = uri.fsPath;")
        extension_ts_content.append(f"{INDENT*3}const outputPathSuggestion = getSuggestedOutputPath(filePath, '{{input_file_name}}-{language}-{style}');")
        extension_ts_content.append(f"{INDENT*3}const outputPath = await vscode.window.showSaveDialog({{ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : {{ 'All Files': ['*'] }} }});")
        extension_ts_content.append(f"{INDENT*3}if (!outputPath) {{ return; }}")
        extension_ts_content.append(f"{INDENT*3}const command = `xrcg generate --projectname ${{path.basename(outputPath.fsPath)}} --language {language} --style {style} --definitions ${{filePath}} --output ${{outputPath.fsPath}}`;")
        extension_ts_content.append(f"{INDENT*3}executeCommand(command, outputPath, outputChannel);")
        extension_ts_content.append(f"{INDENT*2}}}));")
        extension_ts_content.append("")
    
    # Footer
    extension_ts_content.extend([
        f"{INDENT*2}context.subscriptions.push(...disposables);",
        f"{INDENT}}})();",
        "}",
        "",
        "export function deactivate() {}",
        "",
        "function getSuggestedOutputPath(inputFilePath: string, suggestedOutputPath: string) {",
        f"{INDENT}const inputFileName = inputFilePath ? path.basename(inputFilePath, path.extname(inputFilePath)) : '';",
        f"{INDENT}const outFileName = suggestedOutputPath.replace('{{input_file_name}}', inputFileName);",
        f"{INDENT}return path.join(path.dirname(inputFilePath), outFileName);",
        "}"
    ])
    
    # Write extension.ts
    with open(extension_ts_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(extension_ts_content))
    
    print(f"Generated src/extension.ts with {len(commands)} command handlers")


def main():
    """
    Main function to update VS Code extension project.
    """
    parser = argparse.ArgumentParser(description='Update VS Code extension project based on commands.json')
    parser.add_argument('--extension-root', type=str, 
                        help='The root path of the VS Code extension project (default: xregistry_vscode)')
    parser.add_argument('--commands', type=str,
                        help='The path to commands.json (default: xregistry/commands.json)')
    parser.add_argument('--update-extension-ts', action='store_true',
                        help='Also update src/extension.ts (default: only update package.json)')
    
    args = parser.parse_args()
    
    # Determine paths
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    extension_root = Path(args.extension_root) if args.extension_root else root_dir / 'xregistry_vscode'
    commands_file = Path(args.commands) if args.commands else root_dir / 'xregistry' / 'commands.json'
    
    if not extension_root.exists():
        print(f"Error: Extension root not found at {extension_root}")
        return 1
    
    if not commands_file.exists():
        print(f"Error: Commands file not found at {commands_file}")
        return 1
    
    # Load commands
    with open(commands_file, 'r', encoding='utf-8') as file:
        commands = json.load(file)
    
    print(f"Loaded {len(commands)} commands from {commands_file}")
    
    # Update package.json
    package_json_path = extension_root / 'package.json'
    update_package_json(package_json_path, commands)
    
    # Optionally update extension.ts
    if args.update_extension_ts:
        extension_ts_path = extension_root / 'src' / 'extension.ts'
        generate_extension_ts(extension_ts_path, commands)
    
    print("\nDone!")
    return 0


if __name__ == '__main__':
    exit(main())
