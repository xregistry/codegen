---
layout: default
title: Home
description: Generate messaging code from xRegistry message and endpoint definitions
---

<section class="hero">
  <h1>xRegistry Codegen</h1>
  <p class="hero-description">
    Generate production-ready messaging code from xRegistry message and endpoint definitions 
    for multiple languages and protocols.
  </p>
  <div class="hero-actions">
    <a href="{{ '/gallery/' | relative_url }}" class="btn btn-primary">
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="7" height="7"></rect>
        <rect x="14" y="3" width="7" height="7"></rect>
        <rect x="14" y="14" width="7" height="7"></rect>
        <rect x="3" y="14" width="7" height="7"></rect>
      </svg>
      View Gallery
    </a>
    <a href="https://github.com/xregistry/codegen" class="btn btn-secondary" target="_blank">
      <i class="devicon-github-original"></i>
      GitHub
    </a>
  </div>
</section>

<section class="install-section">
  <h2>Quick Start</h2>
  <div class="install-options">
    <div class="install-option">
      <div class="install-header">
        <i class="devicon-docker-plain"></i>
        <h3>Docker</h3>
        <span class="badge">Recommended</span>
      </div>
      <div class="install-command">
        <code>docker pull ghcr.io/xregistry/codegen/xrcg:latest</code>
        <button class="btn btn-icon copy-btn" data-copy="docker pull ghcr.io/xregistry/codegen/xrcg:latest" title="Copy">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
        </button>
      </div>
      <p class="install-note">No Python required. Works on Linux, macOS, and Windows.</p>
      <details class="install-details">
        <summary>Shell alias for convenience</summary>
        <div class="code-tabs">
          <div class="code-tab">
            <span class="tab-label">Linux/macOS</span>
            <pre><code>alias xrcg='docker run --rm -v $(pwd):/work ghcr.io/xregistry/codegen/xrcg:latest'</code></pre>
          </div>
          <div class="code-tab">
            <span class="tab-label">PowerShell</span>
            <pre><code>function xrcg { docker run --rm -v ${PWD}:/work ghcr.io/xregistry/codegen/xrcg:latest $args }</code></pre>
          </div>
        </div>
      </details>
    </div>
    <div class="install-option">
      <div class="install-header">
        <i class="devicon-python-plain"></i>
        <h3>Python</h3>
      </div>
      <div class="install-command">
        <code>pip install xrcg</code>
        <button class="btn btn-icon copy-btn" data-copy="pip install xrcg" title="Copy">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
        </button>
      </div>
      <p class="install-note">Requires Python 3.10+</p>
    </div>
  </div>
  
  <div class="quick-example">
    <h3>Generate your first SDK</h3>
    <div class="install-command wide">
      <code>xrcg generate --language py --style kafkaproducer -d https://raw.githubusercontent.com/xregistry/codegen/main/samples/message-definitions/inkjet.xreg.json -o ./output --projectname PrinterEvents</code>
      <button class="btn btn-icon copy-btn" data-copy="xrcg generate --language py --style kafkaproducer -d https://raw.githubusercontent.com/xregistry/codegen/main/samples/message-definitions/inkjet.xreg.json -o ./output --projectname PrinterEvents" title="Copy">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
      </button>
    </div>
  </div>
</section>

<section class="features-grid">
  <div class="card feature-card">
    <div class="feature-icon">
      <i class="devicon-python-plain"></i>
      <i class="devicon-csharp-plain"></i>
      <i class="devicon-java-plain"></i>
    </div>
    <h3>Multi-Language Support</h3>
    <p class="card-description">
      Generate code for C#, Java, Python, TypeScript, and Go with idiomatic patterns for each language.
    </p>
  </div>
  
  <div class="card feature-card">
    <div class="feature-icon">📡</div>
    <h3>Multiple Protocols</h3>
    <p class="card-description">
      AMQP, MQTT, Kafka, HTTP, Azure Event Hubs, Azure Service Bus, Azure Event Grid, and more.
    </p>
  </div>
  
  <div class="card feature-card">
    <div class="feature-icon">📋</div>
    <h3>Schema Format Flexibility</h3>
    <p class="card-description">
      Works with Apache Avro, JSON Schema, Protocol Buffers (protobuf), and XSD schema formats.
    </p>
  </div>
  
  <div class="card feature-card">
    <div class="feature-icon">☁️</div>
    <h3>CloudEvents Native</h3>
    <p class="card-description">
      First-class support for CloudEvents message format with proper type mappings and metadata handling.
    </p>
  </div>
  
  <div class="card feature-card">
    <div class="feature-icon">🔧</div>
    <h3>Extensible Templates</h3>
    <p class="card-description">
      Customizable Jinja2 templates allow you to tailor the generated code to your specific needs.
    </p>
  </div>
  
  <div class="card feature-card">
    <div class="feature-icon">✅</div>
    <h3>Production Ready</h3>
    <p class="card-description">
      Generated code includes proper error handling, logging, tests, and follows best practices.
    </p>
  </div>
</section>

<section class="what-you-get-section">
  <h2>What You Get</h2>
  <p class="section-intro">Unlike snippet generators, this tool produces complete SDK-like projects:</p>
  
  <div class="features-grid">
    <div class="card">
      <h4>🎯 Type-safe Clients</h4>
      <p>Producer/consumer classes with strongly-typed methods per message</p>
    </div>
    <div class="card">
      <h4>📦 Data Classes</h4>
      <p>Schema-derived classes via Avrotize (JSON Schema, Avro, Protobuf)</p>
    </div>
    <div class="card">
      <h4>🔧 Build Files</h4>
      <p>pom.xml, .csproj, package.json, pyproject.toml with correct dependencies</p>
    </div>
    <div class="card">
      <h4>🧪 Integration Tests</h4>
      <p>Docker-based tests using Testcontainers for Kafka, MQTT, AMQP brokers</p>
    </div>
    <div class="card">
      <h4>📁 Project Structure</h4>
      <p>Language-idiomatic layout ready for IDE import</p>
    </div>
    <div class="card">
      <h4>📚 Documentation</h4>
      <p>Generated README and inline documentation</p>
    </div>
  </div>
</section>

<section class="command-reference-section">
  <h2>Command Reference</h2>
  
  <div class="command-block">
    <h3>The Generate Command</h3>
    <pre><code>xrcg generate --projectname &lt;name&gt; --language &lt;lang&gt; --style &lt;style&gt; \
  --definitions &lt;file-or-url&gt; --output &lt;dir&gt;</code></pre>
    
    <table class="options-table">
      <thead>
        <tr><th>Option</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr><td><code>--projectname</code></td><td>Project/namespace name for generated code</td></tr>
        <tr><td><code>--language</code></td><td>Target language: <code>java</code>, <code>cs</code>, <code>py</code>, <code>ts</code>, <code>go</code>, <code>asyncapi</code>, <code>openapi</code></td></tr>
        <tr><td><code>--style</code></td><td>Protocol binding: <code>kafkaproducer</code>, <code>ehconsumer</code>, <code>mqttclient</code>, etc.</td></tr>
        <tr><td><code>--definitions</code>, <code>-d</code></td><td>Path or URL to xRegistry JSON/YAML definition</td></tr>
        <tr><td><code>--output</code>, <code>-o</code></td><td>Output directory (will be created/overwritten)</td></tr>
        <tr><td><code>--templates</code></td><td>Custom template directory (optional)</td></tr>
        <tr><td><code>--template-args</code></td><td>Extra args as key=value (optional)</td></tr>
      </tbody>
    </table>
  </div>
  
  <div class="command-block">
    <h3>Other Commands</h3>
    <div class="command-examples">
      <div class="example-block">
        <h4>List available templates</h4>
        <pre><code>xrcg list</code></pre>
      </div>
      <div class="example-block">
        <h4>Validate definition files</h4>
        <pre><code>xrcg validate --definitions ./catalog.json</code></pre>
      </div>
      <div class="example-block">
        <h4>Configure defaults</h4>
        <pre><code>xrcg config set defaults.language java
xrcg config set defaults.output_dir ./generated
xrcg config list</code></pre>
      </div>
    </div>
  </div>
</section>

<section class="examples-section">
  <h2>Example Usage</h2>
  
  <div class="example-block">
    <h3>Apache Kafka</h3>
    <pre><code># Python Kafka Producer
xrcg generate --language py --style kafkaproducer -d contoso-erp.xreg.json -o ./output

# C# Kafka Consumer  
xrcg generate --language cs --style kafkaconsumer -d contoso-erp.xreg.json -o ./output

# Java Kafka Producer
xrcg generate --language java --style kafkaproducer -d contoso-erp.xreg.json -o ./output</code></pre>
  </div>
  
  <div class="example-block">
    <h3>Azure Event Hubs</h3>
    <pre><code># TypeScript Event Hubs Producer
xrcg generate --language ts --style ehproducer -d fabrikam.xreg.json -o ./output

# C# Event Hubs Consumer with Azure Functions
xrcg generate --language cs --style ehazfn -d fabrikam.xreg.json -o ./output</code></pre>
  </div>
  
  <div class="example-block">
    <h3>MQTT 5.0</h3>
    <pre><code># Python MQTT Client
xrcg generate --language py --style mqttclient -d smartoven.xreg.json -o ./output

# Java MQTT Client
xrcg generate --language java --style mqttclient -d smartoven.xreg.json -o ./output</code></pre>
  </div>
  
  <div class="example-block">
    <h3>AMQP 1.0 (RabbitMQ, Artemis, Qpid)</h3>
    <pre><code># C# AMQP Producer
xrcg generate --language cs --style amqpproducer -d inkjet.xreg.json -o ./output

# Java AMQP Consumer
xrcg generate --language java --style amqpconsumer -d inkjet.xreg.json -o ./output</code></pre>
  </div>
  
  <div class="example-block">
    <h3>AsyncAPI / OpenAPI</h3>
    <pre><code># Generate AsyncAPI 3.0 spec
xrcg generate --language asyncapi --style consumer -d contoso-erp.xreg.json -o ./output

# Generate OpenAPI 3.0 spec
xrcg generate --language openapi --style producer -d contoso-erp.xreg.json -o ./output</code></pre>
  </div>
</section>

<section>
  <h2>Available Templates</h2>
  
  <div class="features-grid">
    <div class="card">
      <h4><i class="devicon-csharp-plain"></i> C# / .NET 6+</h4>
      <ul>
        <li><code>kafkaproducer</code>, <code>kafkaconsumer</code></li>
        <li><code>ehproducer</code>, <code>ehconsumer</code>, <code>ehazfn</code></li>
        <li><code>sbproducer</code>, <code>sbconsumer</code>, <code>sbazfn</code></li>
        <li><code>egproducer</code>, <code>egazfn</code></li>
        <li><code>amqpproducer</code>, <code>amqpconsumer</code></li>
        <li><code>mqttclient</code></li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-java-plain"></i> Java 21+</h4>
      <ul>
        <li><code>kafkaproducer</code>, <code>kafkaconsumer</code></li>
        <li><code>ehproducer</code>, <code>ehconsumer</code></li>
        <li><code>sbproducer</code>, <code>sbconsumer</code></li>
        <li><code>amqpproducer</code>, <code>amqpconsumer</code></li>
        <li><code>mqttclient</code></li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-python-plain"></i> Python 3.9+</h4>
      <ul>
        <li><code>kafkaproducer</code>, <code>kafkaconsumer</code></li>
        <li><code>ehproducer</code>, <code>ehconsumer</code></li>
        <li><code>amqpproducer</code>, <code>amqpconsumer</code></li>
        <li><code>mqttclient</code></li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-typescript-plain"></i> TypeScript</h4>
      <ul>
        <li><code>kafkaproducer</code>, <code>kafkaconsumer</code></li>
        <li><code>ehproducer</code>, <code>ehconsumer</code></li>
        <li><code>sbproducer</code>, <code>sbconsumer</code></li>
        <li><code>egproducer</code></li>
        <li><code>amqpproducer</code>, <code>amqpconsumer</code></li>
        <li><code>mqttclient</code></li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-go-plain"></i> Go</h4>
      <ul>
        <li><code>kafkaproducer</code>, <code>kafkaconsumer</code></li>
      </ul>
    </div>
    
    <div class="card">
      <h4>📄 Specifications</h4>
      <ul>
        <li><code>asyncapi</code> - AsyncAPI 3.0</li>
        <li><code>openapi</code> - OpenAPI 3.0</li>
        <li>Azure Stream Analytics</li>
      </ul>
    </div>
  </div>
</section>

<section class="xregistry-section">
  <h2>What is xRegistry?</h2>
  <p>
    <a href="https://xregistry.io/" target="_blank">xRegistry</a> is a CNCF project defining a standard format for describing messaging and eventing infrastructure. A message catalog document contains:
  </p>
  <ul class="xregistry-list">
    <li><strong>Schema groups</strong> — Payload schemas (JSON Schema, Avro, Protobuf)</li>
    <li><strong>Message groups</strong> — Message definitions with <a href="https://cloudevents.io/" target="_blank">CloudEvents</a> envelope metadata</li>
    <li><strong>Endpoints</strong> — Protocol bindings (Kafka topics, AMQP queues, HTTP endpoints)</li>
  </ul>
  <p>
    The code generator follows references between these elements to produce cohesive, type-safe SDKs.
  </p>
  
  <h3>Sample Definitions</h3>
  <p>Try these sample definitions from the repository:</p>
  <table class="options-table">
    <thead>
      <tr><th>File</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>contoso-erp.xreg.json</code></td><td>ERP system events (orders, payments, inventory)</td></tr>
      <tr><td><code>fabrikam-motorsports.xreg.json</code></td><td>Motorsports telemetry stream</td></tr>
      <tr><td><code>inkjet.xreg.json</code></td><td>IoT printer events</td></tr>
    </tbody>
  </table>
</section>

<section class="community-section">
  <h2>Community</h2>
  <div class="community-links">
    <a href="http://slack.cncf.io/" target="_blank" class="community-link">
      <span class="community-icon">💬</span>
      <span>#cloudevents on CNCF Slack</span>
    </a>
    <a href="https://lists.cncf.io/g/cncf-cloudevents" target="_blank" class="community-link">
      <span class="community-icon">📧</span>
      <span>Mailing List</span>
    </a>
    <a href="https://github.com/xregistry/codegen" target="_blank" class="community-link">
      <i class="devicon-github-original"></i>
      <span>GitHub</span>
    </a>
  </div>
</section>

<script>
// Generic copy button handler
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async function() {
    const textToCopy = this.dataset.copy;
    if (!textToCopy) return;
    
    try {
      await navigator.clipboard.writeText(textToCopy);
      const originalHTML = this.innerHTML;
      this.innerHTML = `
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      `;
      this.classList.add('copied');
      setTimeout(() => {
        this.innerHTML = originalHTML;
        this.classList.remove('copied');
      }, 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  });
});
</script>
