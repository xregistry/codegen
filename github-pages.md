# GitHub Pages Site for xRegistry Code Generation CLI

## Overview

Create a GitHub Pages documentation site for the xRegistry Code Generation CLI (`xrcg`) that serves as:
1. **Home page** for the project
2. **Gallery** of code generation examples (similar to avrotize/structurize gallery)

The visual style should align with https://xregistry.io (CNCF project styling with CloudEvents heritage).

## Reference Architecture

Based on analysis of [avrotize gh-pages branch](https://github.com/clemensv/avrotize/tree/gh-pages):

```
gh-pages branch structure:
├── .github/workflows/        # CI/CD for building and deploying
├── _layouts/                 # Jekyll templates
│   ├── default.html          # Base layout with nav/footer
│   └── gallery-viewer.html   # Gallery item detail view
├── assets/
│   ├── css/style.css         # Main stylesheet
│   └── js/main.js            # JS utilities
├── gallery/                  # Generated gallery pages (one per example)
│   └── {example-id}/
│       └── index.html        # Jekyll front matter + file tree
├── pages/
│   ├── gallery.html          # Gallery index page
│   └── index.html            # Home page (optional)
├── scripts/
│   └── build_gallery.py      # Python script to generate gallery content
├── _config.yml               # Jekyll configuration
├── Gemfile                   # Ruby dependencies
├── index.html                # Site home page
└── .gitignore
```

---

## Work Task Checklist

### Phase 1: Site Foundation

- [ ] **1.1** Create orphaned `gh-pages` branch structure
  - Create `_config.yml` for Jekyll (baseurl: `/codegen`, site title, theme)
  - Create `Gemfile` with Jekyll dependencies
  - Create `.gitignore` for Jekyll/Python build artifacts

- [ ] **1.2** Create `_layouts/default.html`
  - Navigation: Home, Gallery, Documentation, GitHub link
  - Footer: xRegistry branding, CNCF affiliation, links
  - Include Prism.js for syntax highlighting
  - Include Devicons for language/framework icons
  - Style aligned with xregistry.io color palette

- [ ] **1.3** Create `_layouts/gallery-viewer.html`
  - Three-panel layout: Source | File Tree | Output
  - Resizable panels with collapse/expand
  - Syntax highlighted code viewing
  - Binary file download handling

- [ ] **1.4** Create `assets/css/style.css`
  - xRegistry-aligned color palette (light theme with dark header/footer)
  - White/gray content areas, blue accents (`#2879d0`)
  - Dark header gradient (`#1e2b3a` to `#0d1117`)
  - Gallery cards, tabs, navigation components
  - Responsive design for mobile/tablet

- [ ] **1.5** Create `assets/js/main.js`
  - Mobile nav toggle
  - Gallery panel resize/collapse logic
  - File tree click handlers

### Phase 2: Home Page

- [ ] **2.1** Create `index.html` home page
  - Hero section with xRegistry branding
  - Project description: "Generate production-ready messaging SDKs from xRegistry message catalogs"
  - Key features section:
    - Multi-language: C#, Java, Python, TypeScript
    - Multi-protocol: AMQP, Kafka, MQTT, EventHubs, ServiceBus, HTTP
    - Type-safe CloudEvents integration
    - Compile-ready project output with tests
  - Quick start / installation section
  - Links to gallery and documentation

- [ ] **2.2** Create navigation structure
  - Home → Gallery → Docs → GitHub
  - Protocol filters on gallery (AMQP, Kafka, MQTT, etc.)
  - Language filters on gallery (C#, Java, Python, TypeScript)

### Phase 3: Gallery Build System

- [ ] **3.1** Create `scripts/build_gallery.py`
  - Define gallery items (input definition + language + style combinations)
  - Run `xrcg generate` for each item
  - Build file tree structure from output
  - Generate Jekyll front-matter pages
  - **ZIP file creation** for each example (downloadable)
  - Copy generated files to `gallery/files/{id}/` for serving

- [ ] **3.2** Define gallery examples matrix
  
  **Input Definitions (from `samples/message-definitions/`):**
  
  *Avro Schema Format (original):*
  - `contoso-erp.xreg.json` - Enterprise ERP events (JSON Schema, complex, real-world)
  - `fabrikam-motorsports.xreg.json` - IoT telemetry (Avro, embedded schemas)
  - `inkjet.xreg.json` - Industrial protocol (Avro, simple)
  - `lightbulb.xreg.json` - Smart home (Avro, minimal)
  - `smartoven.xreg.json` - Smart appliance (Avro, enums)
  - `Microsoft.Storage.xreg.json` - Azure events (JSON Schema, cloud native)

  *JSON Schema Format Variants:*
  - `smartoven-jsonschema.xreg.json` - SmartOven with JSON Schema schemas
  - `inkjet-jsonschema.xreg.json` - InkJet with JSON Schema schemas  
  - `fabrikam-motorsports-jsonschema.xreg.json` - Motorsports with JSON Schema schemas

  *Protobuf Format Variants:*
  - `smartoven-proto.xreg.json` - SmartOven with Proto3 schemas
  - `inkjet-proto.xreg.json` - InkJet with Proto3 schemas
  - `fabrikam-motorsports-proto.xreg.json` - Motorsports with Proto3 schemas

  **Languages & Styles:**
  | Language | Producer Styles | Consumer Styles |
  |----------|-----------------|-----------------|
  | C# (cs) | kafkaproducer, ehproducer, sbproducer, amqpproducer, mqttclient | kafkaconsumer, ehconsumer, sbconsumer, amqpconsumer |
  | Java | kafkaproducer, ehproducer, amqpproducer, mqttclient | kafkaconsumer, ehconsumer, amqpconsumer |
  | Python (py) | kafkaproducer, ehproducer, amqpproducer, mqttclient | kafkaconsumer, ehconsumer, amqpconsumer |
  | TypeScript (ts) | kafkaproducer, ehproducer, sbproducer, amqpproducer, mqttclient | kafkaconsumer, ehconsumer, sbconsumer, amqpconsumer |

- [ ] **3.3** Organize gallery by tabs (similar to Avrotize/Structurize)
  - **Tab 1: By Language** - Group examples by target language (Python dev sees all Python samples)
  - **Tab 2: By Protocol** - Group by messaging protocol (Kafka, EventHubs, etc.)
  - **Tab 3: By Schema Format** - Group by schema format (Avro, JSON Schema, Protobuf)
  - Each card shows: Input definition → Output style → Schema format badge → Command used

### Phase 4: Gallery Content

- [ ] **4.1** Python Examples (rich selection for Python developers)
  - Contoso ERP → Kafka Producer (JSON Schema)
  - Contoso ERP → Kafka Consumer (JSON Schema)
  - Fabrikam Motorsports → EventHubs Producer (Avro)
  - SmartOven JSON Schema → Kafka Producer (JSON Schema)
  - SmartOven Proto → Kafka Producer (Protobuf)
  - Inkjet → AMQP Producer (Avro)
  - Lightbulb → MQTT Client (Avro)
  - Microsoft Storage → EventHubs Consumer (JSON Schema)

- [ ] **4.2** C# Examples
  - Contoso ERP → Kafka Producer (JSON Schema)
  - Contoso ERP → Service Bus Producer (JSON Schema)
  - SmartOven JSON Schema → EventHubs Producer (JSON Schema)
  - SmartOven Proto → EventHubs Producer (Protobuf)
  - Fabrikam Motorsports → EventHubs Consumer (Avro)
  - Inkjet → AMQP Producer (Avro)
  - Lightbulb → MQTT Client (Avro)

- [ ] **4.3** Java Examples
  - Contoso ERP → Kafka Producer (JSON Schema)
  - Contoso ERP → Kafka Consumer (JSON Schema)
  - SmartOven JSON Schema → Kafka Producer (JSON Schema)
  - Inkjet Proto → Kafka Producer (Protobuf)
  - Fabrikam Motorsports → EventHubs Producer (Avro)
  - Lightbulb → MQTT Client (Avro)

- [ ] **4.4** TypeScript Examples
  - Contoso ERP → Kafka Producer (JSON Schema)
  - Contoso ERP → Kafka Consumer (JSON Schema)
  - SmartOven JSON Schema → EventHubs Producer (JSON Schema)
  - Inkjet Proto → Dashboard (Protobuf)
  - Fabrikam Motorsports → EventHubs Producer (Avro)
  - Lightbulb → MQTT Client (Avro)

- [ ] **4.5** Schema Format Comparison Examples
  - SmartOven (Avro) → Python Kafka Producer
  - SmartOven (JSON Schema) → Python Kafka Producer
  - SmartOven (Protobuf) → Python Kafka Producer
  - Inkjet (Avro) → C# AMQP Producer
  - Inkjet (JSON Schema) → C# AMQP Producer
  - Inkjet (Protobuf) → C# AMQP Producer

- [ ] **4.6** AsyncAPI/OpenAPI Output Examples
  - Contoso ERP → AsyncAPI 
  - Microsoft Storage → OpenAPI

### Phase 5: Gallery Page Features

- [ ] **5.1** Create `pages/gallery.html` index
  - Tab navigation (By Language / By Protocol)
  - Card grid layout with filtering
  - Each card shows:
    - Input definition name
    - Target language/framework icon (Devicons)
    - Protocol badge (Kafka, AMQP, etc.)
    - Brief description
    - Command used to generate
    - "View Example →" link

- [ ] **5.2** Individual gallery pages (`gallery/{id}/index.html`)
  - Jekyll front matter with metadata
  - Three-panel viewer:
    - Source: Input xRegistry definition
    - File Tree: Generated project structure  
    - Output: Code viewer with syntax highlighting
  - Download ZIP button
  - Back to gallery link
  - Command used to regenerate

- [ ] **5.3** ZIP file download feature
  - Each example includes downloadable ZIP
  - ZIP contains complete generated project
  - Ready to open in VS Code and compile

### Phase 6: CI/CD

- [ ] **6.1** Create `.github/workflows/deploy-pages.yml`
  - Trigger: Push to gh-pages, manual dispatch
  - Steps:
    1. Checkout gh-pages branch
    2. Setup Python 3.10+
    3. Install xrcg from main branch (pip install)
    4. Run `scripts/build_gallery.py`
    5. Build Jekyll site
    6. Deploy to GitHub Pages

- [ ] **6.2** Create `.github/workflows/rebuild-gallery.yml`
  - Scheduled rebuild (weekly or on release)
  - Can be triggered manually
  - Uses latest xrcg version

### Phase 7: Documentation Integration

- [ ] **7.1** Add documentation section
  - Link to main README
  - Link to `docs/` folder files
  - Quick reference for commands

- [ ] **7.2** Create style guide page (optional)
  - Show template authoring info
  - Link to `docs/authoring_templates.md`

---

## Visual Design Notes

### Color Palette (aligned with xregistry.io)

Based on xRegistry website analysis (xregistry/xregistry.github.io):
```css
:root {
  /* LIGHT THEME - matching xregistry.io */
  
  /* Header: Dark gradient (only header is dark) */
  --color-header-bg: linear-gradient(135deg, #1e2b3a, #0d1117);
  
  /* Main content: Light background */
  --color-bg: #ffffff;
  --color-bg-light: #f8f9fa;
  --color-surface: #ffffff;
  --color-surface-alt: #f8f8f8;
  
  /* Primary accent - xRegistry blue */
  --color-primary: #2879d0;
  --color-primary-hover: #1e5f9e;
  
  /* xRegistry brand colors */
  --color-xregistry: #2879d0;     /* Blue from site accents */
  --color-cloudevents: #F04E1F;   /* CloudEvents orange */
  
  /* Problem/Solution colors (from xregistry.io cards) */
  --color-problem: #e53e3e;       /* Red for problem cards */
  --color-problem-bg: #fff5f5;
  --color-solution: #38a169;      /* Green for solution cards */
  --color-solution-bg: #f0fff4;
  
  /* Text - Dark on light */
  --color-text: #333333;
  --color-text-muted: #666666;
  --color-text-light: #999999;
  
  /* Borders and shadows */
  --color-border: #e0e0e0;
  --color-border-light: #eee;
  --shadow-card: 0 3px 10px rgba(0,0,0,0.08);
  --shadow-card-hover: 0 8px 15px rgba(0,0,0,0.1);
  
  /* Footer: Dark (matching header) */
  --color-footer-bg: #151d28;
  
  /* Code blocks */
  --color-code-bg: #f2f2f2;
  
  /* Language accent colors */
  --color-python: #3776AB;
  --color-csharp: #68217A;
  --color-java: #ED8B00;
  --color-typescript: #3178C6;
}
```

### Key Visual Elements from xregistry.io

1. **Header**: Dark gradient (`#1e2b3a` to `#0d1117`) with xRegistry logo
2. **Body**: White/light gray backgrounds (`#ffffff`, `#f8f9fa`)
3. **Cards**: White with subtle shadows, blue icon accents
4. **Buttons**: Blue primary (`#2879d0`), white text
5. **Feature boxes**: Grid layout with blue accent icons
6. **Footer**: Dark background with CNCF sandbox branding
7. **Typography**: Inter font family

### Navigation Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  xRegistry Codegen     Home  Gallery  Docs  [GitHub]            │
└─────────────────────────────────────────────────────────────────┘
```

### Gallery Card Design

```
┌──────────────────────────────────────────┐
│  [Python]  Contoso ERP → Kafka Producer  │
│  ─────────────────────────────────────── │
│  [🐍 Python] → [Apache Kafka]            │
│                                          │
│  Generate Kafka producer from enterprise │
│  event definitions with CloudEvents.     │
│                                          │
│  xrcg generate --language py ...         │
│                                          │
│  View Example → | Download ZIP           │
└──────────────────────────────────────────┘
```

---

## Gallery Examples Matrix (Recommended Selection)

To provide variety while keeping the gallery navigable, select ~35-40 examples showcasing schema format diversity:

### By Language Tab

| Language | Examples |
|----------|----------|
| Python | 8 examples (Kafka prod/cons, EventHubs prod, AMQP prod, MQTT, JSON Schema + Proto variants) |
| C# | 7 examples (Kafka prod, ServiceBus prod/cons, EventHubs prod/cons, MQTT, schema variants) |
| Java | 6 examples (Kafka prod/cons, EventHubs prod, AMQP JMS, MQTT, Proto variant) |
| TypeScript | 6 examples (Kafka prod/cons, Dashboard, EventHubs, MQTT, JSON Schema variant) |
| AsyncAPI/OpenAPI | 2 examples (spec output formats) |

### By Protocol Tab

| Protocol | Languages Shown |
|----------|-----------------|
| Apache Kafka | All 4 languages |
| Azure EventHubs | C#, Python, TypeScript |
| Azure ServiceBus | C#, TypeScript |
| AMQP 1.0 | C#, Java, Python |
| MQTT | All 4 languages |
| HTTP | TypeScript (dashboard) |

### By Schema Format Tab

| Schema Format | Input Definitions |
|---------------|-------------------|
| Avro | `fabrikam-motorsports.xreg.json`, `inkjet.xreg.json`, `lightbulb.xreg.json`, `smartoven.xreg.json` |
| JSON Schema | `contoso-erp.xreg.json`, `smartoven-jsonschema.xreg.json`, `inkjet-jsonschema.xreg.json`, `fabrikam-motorsports-jsonschema.xreg.json` |
| Protobuf | `smartoven-proto.xreg.json`, `inkjet-proto.xreg.json`, `fabrikam-motorsports-proto.xreg.json` |

---

## File Structure for Implementation

```
gh-pages/ (orphaned branch)
├── .github/
│   └── workflows/
│       ├── deploy-pages.yml
│       └── rebuild-gallery.yml
├── _layouts/
│   ├── default.html
│   └── gallery-viewer.html
├── assets/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── gallery/
│   ├── files/                    # Generated code files (served statically)
│   │   └── {example-id}/
│   │       ├── *.py, *.cs, etc.
│   │       └── example.zip       # Downloadable ZIP
│   └── {example-id}/
│       └── index.html            # Gallery viewer page
├── pages/
│   └── gallery.html              # Gallery index
├── scripts/
│   └── build_gallery.py          # Gallery build script
├── _config.yml
├── Gemfile
├── index.html                    # Home page
├── .gitignore
└── README.md                     # Branch documentation
```

---

## Success Criteria

1. ✅ Site is accessible at `https://xregistry.github.io/codegen/`
2. ✅ Gallery shows examples organized by language AND by protocol
3. ✅ Each language (Python, C#, Java, TypeScript) has 5-6 rich examples
4. ✅ Each example is downloadable as a ZIP file
5. ✅ Visual style aligns with xregistry.io branding
6. ✅ Gallery viewer shows source → generated code with syntax highlighting
7. ✅ Mobile-responsive design
8. ✅ CI/CD automatically rebuilds gallery on changes

---

## Next Steps

1. Create orphaned gh-pages branch
2. Implement Phase 1 (site foundation)
3. Build out gallery script
4. Generate initial example set
5. Deploy and test
