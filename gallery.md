---
layout: default
title: Gallery
description: Browse generated code examples for different languages and protocols
permalink: /gallery/
body_class: gallery-index-page
---

<div class="gallery-hero">
  <h1>Code Generation Gallery</h1>
  <p>Explore real-world code generation examples. Click any card to see the xRegistry definition, browse the generated files, and view code with syntax highlighting.</p>
</div>

<div class="gallery-filters">
  <button class="filter-tab active" data-filter="all">All</button>
  <button class="filter-tab" data-filter="python">Python</button>
  <button class="filter-tab" data-filter="csharp">C#</button>
  <button class="filter-tab" data-filter="java">Java</button>
  <button class="filter-tab" data-filter="typescript">TypeScript</button>
  <button class="filter-tab" data-filter="go">Go</button>
  <button class="filter-tab" data-filter="spec">Spec</button>
</div>

<div class="gallery-sections">
  {% if site.gallery.size > 0 %}
  
  <!-- Python Examples -->
  <div class="gallery-category" data-category="python">
    <div class="category-header">
      <h2>Python → Messaging Clients</h2>
      <p>Generate Python producers, consumers, and clients for various messaging protocols</p>
    </div>
    <div class="gallery-cards">
      {% for example in site.gallery %}
        {% if example.language == "Python" %}
        <a href="{{ example.url | relative_url }}" class="gallery-card" data-language="{{ example.language | downcase }}" data-protocol="{{ example.protocol | downcase }}" data-schema="{{ example.schema_format | downcase | replace: ' ', '' }}">
          <div class="card-content">
            <div class="card-header">
              <div class="card-title">{{ example.title }}</div>
              <div class="card-description">{{ example.description | default: "Generate " | append: example.language | append: " " | append: example.protocol | append: " " | append: example.role }}</div>
            </div>
            <div class="card-formats">
              <span class="format-badge source">{% if example.schema_format == "JSON Schema" %}<i class="devicon-json-plain"></i>{% elsif example.schema_format == "Avro" %}<i class="devicon-apache-plain"></i>{% elsif example.schema_format == "Protobuf" %}<i class="devicon-google-plain"></i>{% endif %}{{ example.schema_format }}
              </span>
              <span class="format-arrow">→</span>
              <span class="format-badge target">{{ example.protocol }}</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-command">
              <code>{{ example.command | default: "xrcg generate ..." }}</code>
              <a href="https://github.com/xregistry/codegen#readme" class="docs-link" onclick="event.stopPropagation()">docs</a>
            </div>
            <div class="card-link">View example →</div>
          </div>
        </a>
        {% endif %}
      {% endfor %}
    </div>
  </div>
  
  <!-- C# Examples -->
  <div class="gallery-category" data-category="csharp">
    <div class="category-header">
      <h2>C# → Messaging Clients</h2>
      <p>Generate C# producers, consumers, and clients for Azure and open-source messaging</p>
    </div>
    <div class="gallery-cards">
      {% for example in site.gallery %}
        {% if example.language == "C#" %}
        <a href="{{ example.url | relative_url }}" class="gallery-card" data-language="{{ example.language | downcase | replace: '#', 'sharp' }}" data-protocol="{{ example.protocol | downcase }}" data-schema="{{ example.schema_format | downcase | replace: ' ', '' }}">
          <div class="card-content">
            <div class="card-header">
              <div class="card-title">{{ example.title }}</div>
              <div class="card-description">{{ example.description | default: "Generate " | append: example.language | append: " " | append: example.protocol | append: " " | append: example.role }}</div>
            </div>
            <div class="card-formats">
              <span class="format-badge source">{% if example.schema_format == "JSON Schema" %}<i class="devicon-json-plain"></i>{% elsif example.schema_format == "Avro" %}<i class="devicon-apache-plain"></i>{% elsif example.schema_format == "Protobuf" %}<i class="devicon-google-plain"></i>{% endif %}{{ example.schema_format }}
              </span>
              <span class="format-arrow">→</span>
              <span class="format-badge target">{{ example.protocol }}</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-command">
              <code>{{ example.command | default: "xrcg generate ..." }}</code>
              <a href="https://github.com/xregistry/codegen#readme" class="docs-link" onclick="event.stopPropagation()">docs</a>
            </div>
            <div class="card-link">View example →</div>
          </div>
        </a>
        {% endif %}
      {% endfor %}
    </div>
  </div>
  
  <!-- Java Examples -->
  <div class="gallery-category" data-category="java">
    <div class="category-header">
      <h2>Java → Messaging Clients</h2>
      <p>Generate Java producers, consumers, and clients with Jackson annotations</p>
    </div>
    <div class="gallery-cards">
      {% for example in site.gallery %}
        {% if example.language == "Java" %}
        <a href="{{ example.url | relative_url }}" class="gallery-card" data-language="{{ example.language | downcase }}" data-protocol="{{ example.protocol | downcase }}" data-schema="{{ example.schema_format | downcase | replace: ' ', '' }}">
          <div class="card-content">
            <div class="card-header">
              <div class="card-title">{{ example.title }}</div>
              <div class="card-description">{{ example.description | default: "Generate " | append: example.language | append: " " | append: example.protocol | append: " " | append: example.role }}</div>
            </div>
            <div class="card-formats">
              <span class="format-badge source">{% if example.schema_format == "JSON Schema" %}<i class="devicon-json-plain"></i>{% elsif example.schema_format == "Avro" %}<i class="devicon-apache-plain"></i>{% elsif example.schema_format == "Protobuf" %}<i class="devicon-google-plain"></i>{% endif %}{{ example.schema_format }}
              </span>
              <span class="format-arrow">→</span>
              <span class="format-badge target">{{ example.protocol }}</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-command">
              <code>{{ example.command | default: "xrcg generate ..." }}</code>
              <a href="https://github.com/xregistry/codegen#readme" class="docs-link" onclick="event.stopPropagation()">docs</a>
            </div>
            <div class="card-link">View example →</div>
          </div>
        </a>
        {% endif %}
      {% endfor %}
    </div>
  </div>
  
  <!-- TypeScript Examples -->
  <div class="gallery-category" data-category="typescript">
    <div class="category-header">
      <h2>TypeScript → Messaging Clients</h2>
      <p>Generate TypeScript interfaces and clients with full type safety</p>
    </div>
    <div class="gallery-cards">
      {% for example in site.gallery %}
        {% if example.language == "TypeScript" %}
        <a href="{{ example.url | relative_url }}" class="gallery-card" data-language="{{ example.language | downcase }}" data-protocol="{{ example.protocol | downcase }}" data-schema="{{ example.schema_format | downcase | replace: ' ', '' }}">
          <div class="card-content">
            <div class="card-header">
              <div class="card-title">{{ example.title }}</div>
              <div class="card-description">{{ example.description | default: "Generate " | append: example.language | append: " " | append: example.protocol | append: " " | append: example.role }}</div>
            </div>
            <div class="card-formats">
              <span class="format-badge source">{% if example.schema_format == "JSON Schema" %}<i class="devicon-json-plain"></i>{% elsif example.schema_format == "Avro" %}<i class="devicon-apache-plain"></i>{% elsif example.schema_format == "Protobuf" %}<i class="devicon-google-plain"></i>{% endif %}{{ example.schema_format }}
              </span>
              <span class="format-arrow">→</span>
              <span class="format-badge target">{{ example.protocol }}</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-command">
              <code>{{ example.command | default: "xrcg generate ..." }}</code>
              <a href="https://github.com/xregistry/codegen#readme" class="docs-link" onclick="event.stopPropagation()">docs</a>
            </div>
            <div class="card-link">View example →</div>
          </div>
        </a>
        {% endif %}
      {% endfor %}
    </div>
  </div>
  
  <!-- Go Examples -->
  <div class="gallery-category" data-category="go">
    <div class="category-header">
      <h2>Go → Messaging Clients</h2>
      <p>Generate Go producers and consumers with idiomatic patterns</p>
    </div>
    <div class="gallery-cards">
      {% for example in site.gallery %}
        {% if example.language == "Go" %}
        <a href="{{ example.url | relative_url }}" class="gallery-card" data-language="{{ example.language | downcase }}" data-protocol="{{ example.protocol | downcase }}" data-schema="{{ example.schema_format | downcase | replace: ' ', '' }}">
          <div class="card-content">
            <div class="card-header">
              <div class="card-title">{{ example.title }}</div>
              <div class="card-description">{{ example.description | default: "Generate " | append: example.language | append: " " | append: example.protocol | append: " " | append: example.role }}</div>
            </div>
            <div class="card-formats">
              <span class="format-badge source">{% if example.schema_format == "JSON Schema" %}<i class="devicon-json-plain"></i>{% elsif example.schema_format == "Avro" %}<i class="devicon-apache-plain"></i>{% elsif example.schema_format == "Protobuf" %}<i class="devicon-google-plain"></i>{% endif %}{{ example.schema_format }}
              </span>
              <span class="format-arrow">→</span>
              <span class="format-badge target">{{ example.protocol }}</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-command">
              <code>{{ example.command | default: "xrcg generate ..." }}</code>
              <a href="https://github.com/xregistry/codegen#readme" class="docs-link" onclick="event.stopPropagation()">docs</a>
            </div>
            <div class="card-link">View example →</div>
          </div>
        </a>
        {% endif %}
      {% endfor %}
    </div>
  </div>
  
  <!-- Spec Generation Examples -->
  <div class="gallery-category" data-category="spec">
    <div class="category-header">
      <h2>Spec → API Documentation</h2>
      <p>Generate AsyncAPI and OpenAPI specifications from xRegistry definitions</p>
    </div>
    <div class="gallery-cards">
      {% for example in site.gallery %}
        {% if example.language == "AsyncAPI" or example.language == "OpenAPI" %}
        <a href="{{ example.url | relative_url }}" class="gallery-card" data-language="spec" data-protocol="{{ example.protocol | downcase }}" data-schema="{{ example.schema_format | downcase | replace: ' ', '' }}">
          <div class="card-content">
            <div class="card-header">
              <div class="card-title">{{ example.title }}</div>
              <div class="card-description">{{ example.description | default: "Generate " | append: example.language | append: " specification" }}</div>
            </div>
            <div class="card-formats">
              <span class="format-badge source">{% if example.schema_format == "JSON Schema" %}<i class="devicon-json-plain"></i>{% elsif example.schema_format == "Avro" %}<i class="devicon-apache-plain"></i>{% elsif example.schema_format == "Protobuf" %}<i class="devicon-google-plain"></i>{% endif %}{{ example.schema_format }}
              </span>
              <span class="format-arrow">→</span>
              <span class="format-badge target">{{ example.language }}</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-command">
              <code>{{ example.command | default: "xrcg generate ..." }}</code>
              <a href="https://github.com/xregistry/codegen#readme" class="docs-link" onclick="event.stopPropagation()">docs</a>
            </div>
            <div class="card-link">View example →</div>
          </div>
        </a>
        {% endif %}
      {% endfor %}
    </div>
  </div>
  
  {% else %}
  <div class="empty-state">
    <p>Gallery examples are generated during the CI build process.</p>
    <p>Run the gallery build script locally to see examples:</p>
    <code>python scripts/build_gallery.py</code>
  </div>
  {% endif %}
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const filterTabs = document.querySelectorAll('.filter-tab');
  const categories = document.querySelectorAll('.gallery-category');
  
  filterTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      // Update active tab
      filterTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      
      const filter = this.dataset.filter;
      
      // Show/hide categories
      categories.forEach(category => {
        const categoryType = category.dataset.category;
        if (filter === 'all' || categoryType === filter) {
          category.style.display = 'block';
        } else {
          category.style.display = 'none';
        }
      });
    });
  });
});
</script>

