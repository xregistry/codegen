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
    <a href="https://github.com/xregistry/xregistry-codegen" class="btn btn-secondary" target="_blank">
      <i class="devicon-github-original"></i>
      GitHub
    </a>
  </div>
</section>

<section class="install-section">
  <h2>Quick Install</h2>
  <div class="install-command">
    <code>pip install xrcg</code>
    <button class="btn btn-icon" id="copy-install" title="Copy command">
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
    </button>
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

<section>
  <h2>Example Usage</h2>
  
  <h3>Generate a Kafka Consumer in C#</h3>
  
```bash
xrcg generate --style cs/kafkaconsumer -d contoso-erp.xreg.json -o ./output
```
  
  <h3>Generate an MQTT Client in Python</h3>
  
```bash
xrcg generate --style py/mqttclient -d smartoven.xreg.json -o ./output
```
  
  <h3>Generate an AMQP Producer in Java</h3>
  
```bash
xrcg generate --style java/amqpproducer -d fabrikam.xreg.json -o ./output
```
</section>

<section>
  <h2>Supported Templates</h2>
  
  <div class="features-grid">
    <div class="card">
      <h4><i class="devicon-csharp-plain"></i> C# / .NET</h4>
      <ul>
        <li>AMQP Consumer/Producer</li>
        <li>Kafka Consumer/Producer</li>
        <li>MQTT Client</li>
        <li>Event Hubs Consumer/Producer</li>
        <li>Service Bus Consumer/Producer</li>
        <li>Event Grid Producer</li>
        <li>Azure Functions</li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-java-plain"></i> Java</h4>
      <ul>
        <li>AMQP Consumer/Producer</li>
        <li>Kafka Consumer/Producer</li>
        <li>MQTT Client</li>
        <li>Event Hubs Consumer/Producer</li>
        <li>Service Bus Consumer/Producer</li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-python-plain"></i> Python</h4>
      <ul>
        <li>AMQP Consumer/Producer</li>
        <li>Kafka Consumer/Producer</li>
        <li>MQTT Client</li>
        <li>Event Hubs Consumer/Producer</li>
        <li>Service Bus Consumer/Producer</li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-typescript-plain"></i> TypeScript</h4>
      <ul>
        <li>AMQP Consumer/Producer</li>
        <li>Kafka Consumer/Producer</li>
        <li>MQTT Client</li>
        <li>Event Hubs Consumer/Producer</li>
        <li>Service Bus Consumer/Producer</li>
        <li>HTTP Producer</li>
        <li>Dashboard</li>
      </ul>
    </div>
    
    <div class="card">
      <h4><i class="devicon-go-plain"></i> Go</h4>
      <ul>
        <li>Kafka Consumer/Producer</li>
      </ul>
    </div>
    
    <div class="card">
      <h4>📄 Specifications</h4>
      <ul>
        <li>AsyncAPI (Consumer/Producer)</li>
        <li>OpenAPI (Producer/Subscriber)</li>
        <li>Azure Stream Analytics</li>
      </ul>
    </div>
  </div>
</section>

<script>
document.getElementById('copy-install')?.addEventListener('click', async function() {
  try {
    await navigator.clipboard.writeText('pip install xrcg');
    this.innerHTML = `
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
    `;
    setTimeout(() => {
      this.innerHTML = `
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
      `;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy:', err);
  }
});
</script>
