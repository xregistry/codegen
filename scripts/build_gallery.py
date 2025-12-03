#!/usr/bin/env python3
"""
Gallery Build Script for xRegistry Codegen

This script generates code examples for the gallery using xrcg,
creates Jekyll pages for each example, and packages them as ZIP files.
"""

import json
import os
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Gallery examples configuration
GALLERY_EXAMPLES = [
    # Python Examples
    {"id": "py-kafka-contoso-producer", "definition": "contoso-erp.xreg.json", "style": "py/kafkaproducer", "language": "Python", "language_icon": "python", "protocol": "Kafka", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "py-kafka-contoso-consumer", "definition": "contoso-erp.xreg.json", "style": "py/kafkaconsumer", "language": "Python", "language_icon": "python", "protocol": "Kafka", "role": "Consumer", "schema_format": "JSON Schema"},
    {"id": "py-eh-fabrikam-producer", "definition": "fabrikam-motorsports.xreg.json", "style": "py/ehproducer", "language": "Python", "language_icon": "python", "protocol": "Event Hubs", "role": "Producer", "schema_format": "Avro"},
    {"id": "py-kafka-smartoven-jsonschema", "definition": "smartoven-jsonschema.xreg.json", "style": "py/kafkaproducer", "language": "Python", "language_icon": "python", "protocol": "Kafka", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "py-kafka-smartoven-proto", "definition": "smartoven-proto.xreg.json", "style": "py/kafkaproducer", "language": "Python", "language_icon": "python", "protocol": "Kafka", "role": "Producer", "schema_format": "Protobuf"},
    {"id": "py-amqp-inkjet-producer", "definition": "inkjet.xreg.json", "style": "py/amqpproducer", "language": "Python", "language_icon": "python", "protocol": "AMQP", "role": "Producer", "schema_format": "Avro"},
    {"id": "py-mqtt-lightbulb", "definition": "lightbulb.xreg.json", "style": "py/mqttclient", "language": "Python", "language_icon": "python", "protocol": "MQTT", "role": "Client", "schema_format": "Avro"},

    # C# Examples
    {"id": "cs-kafka-contoso-producer", "definition": "contoso-erp.xreg.json", "style": "cs/kafkaproducer", "language": "C#", "language_icon": "csharp", "protocol": "Kafka", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "cs-sb-contoso-producer", "definition": "contoso-erp.xreg.json", "style": "cs/sbproducer", "language": "C#", "language_icon": "csharp", "protocol": "Service Bus", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "cs-eh-smartoven-jsonschema", "definition": "smartoven-jsonschema.xreg.json", "style": "cs/ehproducer", "language": "C#", "language_icon": "csharp", "protocol": "Event Hubs", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "cs-eh-smartoven-proto", "definition": "smartoven-proto.xreg.json", "style": "cs/ehproducer", "language": "C#", "language_icon": "csharp", "protocol": "Event Hubs", "role": "Producer", "schema_format": "Protobuf"},
    {"id": "cs-eh-fabrikam-consumer", "definition": "fabrikam-motorsports.xreg.json", "style": "cs/ehconsumer", "language": "C#", "language_icon": "csharp", "protocol": "Event Hubs", "role": "Consumer", "schema_format": "Avro"},
    {"id": "cs-amqp-inkjet-producer", "definition": "inkjet.xreg.json", "style": "cs/amqpproducer", "language": "C#", "language_icon": "csharp", "protocol": "AMQP", "role": "Producer", "schema_format": "Avro"},
    {"id": "cs-mqtt-lightbulb", "definition": "lightbulb.xreg.json", "style": "cs/mqttclient", "language": "C#", "language_icon": "csharp", "protocol": "MQTT", "role": "Client", "schema_format": "Avro"},

    # Java Examples
    {"id": "java-kafka-contoso-producer", "definition": "contoso-erp.xreg.json", "style": "java/kafkaproducer", "language": "Java", "language_icon": "java", "protocol": "Kafka", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "java-kafka-contoso-consumer", "definition": "contoso-erp.xreg.json", "style": "java/kafkaconsumer", "language": "Java", "language_icon": "java", "protocol": "Kafka", "role": "Consumer", "schema_format": "JSON Schema"},
    {"id": "java-kafka-smartoven-jsonschema", "definition": "smartoven-jsonschema.xreg.json", "style": "java/kafkaproducer", "language": "Java", "language_icon": "java", "protocol": "Kafka", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "java-kafka-inkjet-proto", "definition": "inkjet-proto.xreg.json", "style": "java/kafkaproducer", "language": "Java", "language_icon": "java", "protocol": "Kafka", "role": "Producer", "schema_format": "Protobuf"},
    {"id": "java-eh-fabrikam-producer", "definition": "fabrikam-motorsports.xreg.json", "style": "java/ehproducer", "language": "Java", "language_icon": "java", "protocol": "Event Hubs", "role": "Producer", "schema_format": "Avro"},
    {"id": "java-mqtt-lightbulb", "definition": "lightbulb.xreg.json", "style": "java/mqttclient", "language": "Java", "language_icon": "java", "protocol": "MQTT", "role": "Client", "schema_format": "Avro"},

    # TypeScript Examples
    {"id": "ts-kafka-contoso-producer", "definition": "contoso-erp.xreg.json", "style": "ts/kafkaproducer", "language": "TypeScript", "language_icon": "typescript", "protocol": "Kafka", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "ts-kafka-contoso-consumer", "definition": "contoso-erp.xreg.json", "style": "ts/kafkaconsumer", "language": "TypeScript", "language_icon": "typescript", "protocol": "Kafka", "role": "Consumer", "schema_format": "JSON Schema"},
    {"id": "ts-eh-smartoven-jsonschema", "definition": "smartoven-jsonschema.xreg.json", "style": "ts/ehproducer", "language": "TypeScript", "language_icon": "typescript", "protocol": "Event Hubs", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "ts-eh-fabrikam-producer", "definition": "fabrikam-motorsports.xreg.json", "style": "ts/ehproducer", "language": "TypeScript", "language_icon": "typescript", "protocol": "Event Hubs", "role": "Producer", "schema_format": "Avro"},
    {"id": "ts-mqtt-lightbulb", "definition": "lightbulb.xreg.json", "style": "ts/mqttclient", "language": "TypeScript", "language_icon": "typescript", "protocol": "MQTT", "role": "Client", "schema_format": "Avro"},

    # Go Examples
    {"id": "go-kafka-contoso-producer", "definition": "contoso-erp.xreg.json", "style": "go/kafkaproducer", "language": "Go", "language_icon": "go", "protocol": "Kafka", "role": "Producer", "schema_format": "JSON Schema"},
    {"id": "go-kafka-fabrikam-consumer", "definition": "fabrikam-motorsports.xreg.json", "style": "go/kafkaconsumer", "language": "Go", "language_icon": "go", "protocol": "Kafka", "role": "Consumer", "schema_format": "Avro"},

    # AsyncAPI/OpenAPI Examples
    {"id": "asyncapi-contoso-consumer", "definition": "contoso-erp.xreg.json", "style": "asyncapi/consumer", "language": "AsyncAPI", "language_icon": "adonisjs", "protocol": "Spec", "role": "Consumer", "schema_format": "JSON Schema"},
    {"id": "openapi-contoso-producer", "definition": "contoso-erp.xreg.json", "style": "openapi/producer", "language": "OpenAPI", "language_icon": "swagger", "protocol": "Spec", "role": "Producer", "schema_format": "JSON Schema"},
]


@dataclass
class GalleryExample:
    """Represents a gallery example configuration."""
    id: str
    definition: str
    style: str
    language: str
    language_icon: str
    protocol: str
    role: str
    schema_format: str
    
    @property
    def project_name(self) -> str:
        """Generate a project name from the definition filename."""
        # Convert "contoso-erp.xreg.json" -> "ContosoErp"
        base = self.definition.replace('.xreg.json', '').replace('.cereg.yaml', '')
        # Convert kebab-case to PascalCase
        return ''.join(word.capitalize() for word in base.split('-'))
    
    @property
    def title(self) -> str:
        """Generate a human-readable title."""
        def_name = self.definition.replace('.xreg.json', '').replace('-', ' ').title()
        return f"{def_name} → {self.protocol} {self.role}"
    
    @property
    def command(self) -> str:
        """Generate the xrcg command used."""
        parts = self.style.split('/')
        if len(parts) == 2:
            lang, style = parts
            return f"xrcg generate --language {lang} --style {style} -d {self.definition} --output ./output --projectname {self.project_name}"
        return f"xrcg generate --style {self.style} -d {self.definition} --output ./output --projectname {self.project_name}"


def find_definitions_dir() -> Path:
    """Find the samples/message-definitions directory."""
    # Look in common locations
    candidates = [
        Path("../samples/message-definitions"),  # From scripts/ dir
        Path("samples/message-definitions"),      # From repo root
        Path("../../samples/message-definitions"), # From gh-pages branch
    ]
    
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    
    # Try to find it relative to the script
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    # Check if we're in gh-pages (no samples dir) - need to fetch from main
    return repo_root / "samples" / "message-definitions"


def run_xrcg_generate(definition_path: Path, style: str, output_dir: Path, project_name: str) -> bool:
    """Run xrcg generate command.
    
    Args:
        definition_path: Path to the xRegistry definition file
        style: Template style in format "language/style" (e.g., "py/kafkaproducer")
        output_dir: Directory to generate code into
        project_name: Project name for the generated code
    """
    # Split style into language and style parts (e.g., "py/kafkaproducer" -> "py", "kafkaproducer")
    parts = style.split('/')
    if len(parts) != 2:
        print(f"  ⚠️  Invalid style format: {style} (expected 'language/style')")
        return False
    language, style_name = parts
    
    cmd = [
        sys.executable, "-m", "xrcg", "generate",
        "--language", language,
        "--style", style_name,
        "-d", str(definition_path),
        "--output", str(output_dir),
        "--projectname", project_name
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            print(f"  ⚠️  xrcg failed (exit {result.returncode}): {result.stderr[:300]}")
            return False
        # Check if any files were actually generated
        if not any(output_dir.rglob('*')):
            print(f"  ⚠️  xrcg succeeded but no files created")
            if result.stdout:
                print(f"     stdout: {result.stdout[:200]}")
            if result.stderr:
                print(f"     stderr: {result.stderr[:200]}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  xrcg timed out")
        return False
    except Exception as e:
        print(f"  ⚠️  Error running xrcg: {e}")
        return False


def collect_files(directory: Path, base_path: Optional[Path] = None) -> list:
    """Collect all files in a directory with their contents."""
    if base_path is None:
        base_path = directory
    
    files = []
    
    for item in sorted(directory.iterdir()):
        if item.name.startswith('.'):
            continue
            
        relative_path = item.relative_to(base_path)
        
        if item.is_file():
            try:
                content = item.read_text(encoding='utf-8')
                files.append({
                    "path": str(relative_path).replace("\\", "/"),
                    "content": content
                })
            except UnicodeDecodeError:
                # Binary file - just note it exists
                files.append({
                    "path": str(relative_path).replace("\\", "/"),
                    "content": f"[Binary file: {item.stat().st_size} bytes]"
                })
        elif item.is_dir():
            files.extend(collect_files(item, base_path))
    
    return files


def create_zip(source_dir: Path, output_path: Path) -> None:
    """Create a ZIP file from a directory."""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                arcname = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)


def generate_file_tree_html(files: list) -> str:
    """Generate HTML for the file tree."""
    # Build tree structure
    tree = {}
    for f in files:
        parts = f["path"].split("/")
        current = tree
        for i, part in enumerate(parts):
            if part not in current:
                current[part] = {} if i < len(parts) - 1 else None
            if current[part] is not None:
                current = current[part]
    
    def render_tree(node: dict, prefix: str = "") -> str:
        html = "<ul>"
        items = sorted(node.items(), key=lambda x: (x[1] is None, x[0]))
        
        for name, children in items:
            path = f"{prefix}/{name}" if prefix else name
            if children is None:
                # File
                ext = name.split('.')[-1] if '.' in name else ''
                html += f'<li><div class="file-tree-item file" data-path="{path}">'
                html += f'<span class="file-name">{name}</span></div></li>'
            else:
                # Directory
                html += f'<li><div class="file-tree-item folder" data-path="{path}">'
                html += f'<span class="folder-toggle">▶</span>'
                html += f'<span class="file-name">{name}/</span></div>'
                html += f'<div class="folder-contents">{render_tree(children, path)}</div></li>'
        
        html += "</ul>"
        return html
    
    return render_tree(tree)


def generate_gallery_page(example: GalleryExample, files: list, definition_content: str, collection_dir: Path, zip_url: str) -> None:
    """Generate a Jekyll collection item for a gallery example."""
    # Create the Jekyll front matter and content
    files_json = json.dumps({"files": files}, indent=2)
    
    page_content = f"""---
layout: gallery-viewer
title: "{example.title}"
definition_name: "{example.definition}"
language: "{example.language}"
language_icon: "{example.language_icon}"
protocol: "{example.protocol}"
role: "{example.role}"
schema_format: "{example.schema_format}"
command: "{example.command}"
zip_url: "{zip_url}"
definition_content: |
{indent_content(definition_content, 2)}
files_json: |
{indent_content(files_json, 2)}
file_tree_html: |
{indent_content(generate_file_tree_html(files), 2)}
---
"""
    
    # Write as a Jekyll collection item (e.g., _gallery/py-kafka-contoso-producer.html)
    (collection_dir / f"{example.id}.html").write_text(page_content, encoding='utf-8')


def indent_content(content: str, spaces: int) -> str:
    """Indent content for YAML block scalar."""
    indent = " " * spaces
    lines = content.split("\n")
    return "\n".join(indent + line for line in lines)


def main():
    """Main entry point."""
    print("🚀 Building xRegistry Codegen Gallery\n")
    
    # Determine paths
    script_dir = Path(__file__).parent
    site_root = script_dir.parent
    collection_dir = site_root / "_gallery"  # Jekyll collection folder
    files_dir = site_root / "gallery" / "files"  # Static files folder
    
    # Try to find definitions
    definitions_dir = find_definitions_dir()
    
    if not definitions_dir.exists():
        print(f"⚠️  Definitions directory not found at {definitions_dir}")
        print("   Will attempt to fetch from main branch during CI")
        return 1
    
    print(f"📁 Definitions: {definitions_dir}")
    print(f"📁 Gallery output: {collection_dir}\n")
    
    # Clean previous gallery content
    if collection_dir.exists():
        shutil.rmtree(collection_dir)
    collection_dir.mkdir(parents=True, exist_ok=True)
    
    if files_dir.exists():
        shutil.rmtree(files_dir)
    files_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each example
    success_count = 0
    fail_count = 0
    
    for example_config in GALLERY_EXAMPLES:
        example = GalleryExample(**example_config)
        print(f"📦 {example.id}: {example.title}")
        
        definition_path = definitions_dir / example.definition
        if not definition_path.exists():
            print(f"   ⚠️  Definition not found: {example.definition}")
            fail_count += 1
            continue
        
        # Create output directory
        output_dir = files_dir / example.id / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Run xrcg generate
        if not run_xrcg_generate(definition_path, example.style, output_dir, example.project_name):
            print(f"   ⚠️  Generation failed, skipping")
            fail_count += 1
            continue
        
        # Collect generated files
        files = collect_files(output_dir)
        if not files:
            print(f"   ⚠️  No files generated")
            fail_count += 1
            continue
        
        # Read definition content
        definition_content = definition_path.read_text(encoding='utf-8')
        
        # Create ZIP file
        zip_path = files_dir / example.id / f"{example.id}.zip"
        create_zip(output_dir, zip_path)
        zip_url = f"/codegen/gallery/files/{example.id}/{example.id}.zip"
        
        # Generate gallery page
        generate_gallery_page(
            example, files, definition_content, 
            collection_dir, zip_url
        )
        
        print(f"   ✅ Generated {len(files)} files, ZIP: {zip_path.stat().st_size // 1024}KB")
        success_count += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Completed: {success_count} examples")
    if fail_count:
        print(f"⚠️  Failed: {fail_count} examples")
    
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
