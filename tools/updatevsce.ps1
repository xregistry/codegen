#!/usr/bin/env pwsh
# Update VS Code extension from commands.json

python tools/update_vscode_extension.py --extension-root ./xregistry_vscode --commands ./xregistry/commands.json
