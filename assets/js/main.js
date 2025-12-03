/**
 * xRegistry Codegen - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
  initCodeCopy();
  initSmoothScroll();
});

/**
 * Initialize copy-to-clipboard functionality for code blocks
 */
function initCodeCopy() {
  // Add copy buttons to all code blocks
  document.querySelectorAll('pre[class*="language-"]').forEach(function(pre) {
    if (pre.querySelector('.copy-button')) return; // Already has button
    
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.innerHTML = `
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
      <span>Copy</span>
    `;
    button.title = 'Copy to clipboard';
    
    button.addEventListener('click', async function() {
      const code = pre.querySelector('code');
      const text = code ? code.textContent : pre.textContent;
      
      try {
        await navigator.clipboard.writeText(text);
        button.innerHTML = `
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span>Copied!</span>
        `;
        button.classList.add('copied');
        
        setTimeout(function() {
          button.innerHTML = `
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>Copy</span>
          `;
          button.classList.remove('copied');
        }, 2000);
      } catch (err) {
        console.error('Failed to copy:', err);
        button.innerHTML = `
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
          <span>Failed</span>
        `;
        
        setTimeout(function() {
          button.innerHTML = `
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>Copy</span>
          `;
        }, 2000);
      }
    });
    
    // Position button
    pre.style.position = 'relative';
    pre.appendChild(button);
  });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // Update URL without jumping
        history.pushState(null, null, '#' + targetId);
      }
    });
  });
}

/**
 * Utility: Get file extension from path
 */
function getFileExtension(path) {
  const parts = path.split('.');
  return parts.length > 1 ? parts.pop().toLowerCase() : '';
}

/**
 * Utility: Get Prism language from file extension
 */
function getPrismLanguage(extension) {
  const languageMap = {
    'cs': 'csharp',
    'csproj': 'xml',
    'java': 'java',
    'py': 'python',
    'ts': 'typescript',
    'js': 'javascript',
    'go': 'go',
    'json': 'json',
    'yaml': 'yaml',
    'yml': 'yaml',
    'xml': 'xml',
    'proto': 'protobuf',
    'avsc': 'json',
    'md': 'markdown',
    'html': 'html',
    'css': 'css',
    'sh': 'bash',
    'bat': 'batch',
    'ps1': 'powershell',
    'toml': 'toml',
    'mod': 'go-module',
    'sln': 'plaintext',
    'txt': 'plaintext'
  };
  
  return languageMap[extension] || 'plaintext';
}

/**
 * Utility: Get file icon class from extension
 */
function getFileIconClass(extension) {
  const iconMap = {
    'cs': 'devicon-csharp-plain',
    'java': 'devicon-java-plain',
    'py': 'devicon-python-plain',
    'ts': 'devicon-typescript-plain',
    'js': 'devicon-javascript-plain',
    'go': 'devicon-go-plain',
    'json': 'devicon-json-plain',
    'yaml': 'devicon-yaml-plain',
    'yml': 'devicon-yaml-plain',
    'xml': 'devicon-xml-plain',
    'proto': 'devicon-protobuf-plain',
    'md': 'devicon-markdown-original',
    'html': 'devicon-html5-plain',
    'css': 'devicon-css3-plain'
  };
  
  return iconMap[extension] || 'file-icon';
}

// Add copy button styles
const copyButtonStyles = document.createElement('style');
copyButtonStyles.textContent = `
  .copy-button {
    position: absolute;
    top: 8px;
    right: 8px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 500;
    font-family: var(--font-sans);
    color: var(--color-text-muted);
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: 4px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s ease, background-color 0.2s ease;
  }
  
  pre:hover .copy-button {
    opacity: 1;
  }
  
  .copy-button:hover {
    background-color: var(--color-bg-alt);
    color: var(--color-text);
  }
  
  .copy-button.copied {
    color: var(--color-success);
    border-color: var(--color-success);
  }
  
  .copy-button .icon {
    width: 14px;
    height: 14px;
  }
`;
document.head.appendChild(copyButtonStyles);
