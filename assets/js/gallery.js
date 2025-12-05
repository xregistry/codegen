/**
 * xRegistry Codegen Gallery - Interactive file browser
 */

document.addEventListener('DOMContentLoaded', function() {
  initGallery();
});

/**
 * Initialize the gallery viewer
 */
function initGallery() {
  const dataElement = document.getElementById('gallery-data');
  if (!dataElement) return;
  
  let filesData;
  try {
    filesData = JSON.parse(dataElement.textContent);
  } catch (e) {
    console.error('Failed to parse gallery data:', e);
    return;
  }
  
  initFileTree(filesData);
  initPanelToggles();
  initCopyCodeButton();
  initKeyboardNavigation(filesData);
  initHashNavigation(filesData);
  
  // Check for file path in URL hash, otherwise try README.md, then first file
  const hashPath = getFilePathFromHash();
  if (hashPath) {
    const fileFromHash = filesData.files.find(f => f.path === hashPath);
    if (fileFromHash) {
      selectFileByPath(hashPath, filesData);
    } else {
      // Hash doesn't match any file, try README.md or first file
      loadDefaultFile(filesData);
    }
  } else {
    // No hash, try README.md or first file
    loadDefaultFile(filesData);
  }
}

/**
 * Initialize the file tree from data
 */
function initFileTree(filesData) {
  const fileTree = document.getElementById('file-tree');
  if (!fileTree) return;
  
  // Build tree structure
  const tree = buildTreeStructure(filesData.files);
  fileTree.innerHTML = renderTree(tree, filesData);
  
  // Add click handlers
  fileTree.querySelectorAll('.file-tree-item').forEach(item => {
    item.addEventListener('click', function(e) {
      const path = this.dataset.path;
      const isFolder = this.classList.contains('folder');
      
      if (isFolder) {
        toggleFolder(this);
      } else {
        selectFile(this, path, filesData);
      }
    });
  });
}

/**
 * Build tree structure from flat file list
 */
function buildTreeStructure(files) {
  const root = { name: '', children: {}, isFolder: true };
  
  files.forEach(file => {
    const parts = file.path.split('/');
    let current = root;
    
    parts.forEach((part, index) => {
      if (!current.children[part]) {
        current.children[part] = {
          name: part,
          children: {},
          isFolder: index < parts.length - 1,
          path: parts.slice(0, index + 1).join('/')
        };
      }
      current = current.children[part];
    });
    
    // Add file content reference
    current.content = file.content;
  });
  
  return root;
}

/**
 * Render tree as HTML
 */
function renderTree(node, filesData, level = 0) {
  const children = Object.values(node.children);
  if (children.length === 0) return '';
  
  // Sort: folders first, then files, alphabetically
  children.sort((a, b) => {
    if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1;
    return a.name.localeCompare(b.name);
  });
  
  let html = '<ul>';
  
  children.forEach(child => {
    const extension = getFileExtension(child.name);
    const iconClass = child.isFolder ? 'folder-icon' : `file-icon-${extension}`;
    const itemClass = child.isFolder ? 'folder' : 'file';
    
    html += `<li>`;
    html += `<div class="file-tree-item ${itemClass}" data-path="${child.path || ''}">`;
    
    if (child.isFolder) {
      html += `<svg class="folder-toggle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>`;
      html += `<svg class="file-icon folder-icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
      </svg>`;
    } else {
      html += `<svg class="file-icon ${iconClass}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
      </svg>`;
    }
    
    html += `<span class="file-name">${escapeHtml(child.name)}</span>`;
    html += `</div>`;
    
    if (child.isFolder) {
      html += `<div class="folder-contents">`;
      html += renderTree(child, filesData, level + 1);
      html += `</div>`;
    }
    
    html += `</li>`;
  });
  
  html += '</ul>';
  return html;
}

/**
 * Toggle folder open/closed
 */
function toggleFolder(element) {
  const toggle = element.querySelector('.folder-toggle');
  const contents = element.nextElementSibling;
  
  if (toggle && contents) {
    toggle.classList.toggle('collapsed');
    contents.classList.toggle('collapsed');
  }
}

/**
 * Select a file and show its content
 */
function selectFile(element, path, filesData) {
  // Update active state
  document.querySelectorAll('.file-tree-item.active').forEach(item => {
    item.classList.remove('active');
  });
  element.classList.add('active');
  
  // Update URL hash with file path
  updateUrlHash(path);
  
  // Find file content
  const file = filesData.files.find(f => f.path === path);
  if (file) {
    loadFileContent(path, file.content, filesData);
  }
}

/**
 * Select a file by its path (used for hash navigation)
 */
function selectFileByPath(path, filesData) {
  const element = document.querySelector(`.file-tree-item[data-path="${path}"]`);
  if (element) {
    // Ensure parent folders are expanded
    expandParentFolders(element);
    selectFile(element, path, filesData);
    element.scrollIntoView({ block: 'nearest' });
  }
}

/**
 * Expand all parent folders of an element
 */
function expandParentFolders(element) {
  let parent = element.parentElement;
  while (parent) {
    if (parent.classList && parent.classList.contains('folder-contents')) {
      parent.classList.remove('collapsed');
      // Also update the folder toggle icon
      const folderItem = parent.previousElementSibling;
      if (folderItem) {
        const toggle = folderItem.querySelector('.folder-toggle');
        if (toggle) {
          toggle.classList.remove('collapsed');
        }
      }
    }
    parent = parent.parentElement;
  }
}

/**
 * Update the URL hash with the file path
 */
function updateUrlHash(path) {
  // Use encodeURIComponent for the path to handle special characters
  const hash = 'file=' + encodeURIComponent(path);
  // Use replaceState to avoid adding to browser history for every file click
  history.replaceState(null, '', '#' + hash);
}

/**
 * Get file path from URL hash
 */
function getFilePathFromHash() {
  const hash = window.location.hash;
  if (!hash || hash.length <= 1) return null;
  
  // Parse hash - expecting format: #file=path/to/file
  const hashContent = hash.substring(1); // Remove the # character
  if (hashContent.startsWith('file=')) {
    return decodeURIComponent(hashContent.substring(5));
  }
  return null;
}

/**
 * Initialize hash change listener for browser back/forward navigation
 */
function initHashNavigation(filesData) {
  window.addEventListener('hashchange', function() {
    const hashPath = getFilePathFromHash();
    if (hashPath) {
      const file = filesData.files.find(f => f.path === hashPath);
      if (file) {
        selectFileByPath(hashPath, filesData);
      }
    }
  });
}

/**
 * Load file content into the viewer
 */
function loadFileContent(path, content, filesData) {
  const viewer = document.getElementById('code-viewer');
  const title = document.getElementById('code-panel-title');
  
  if (!viewer || !title) return;
  
  // Update title
  const fileName = path.split('/').pop();
  title.textContent = fileName;
  
  // Determine language
  const extension = getFileExtension(fileName);
  const language = getPrismLanguage(extension);
  
  // Update code viewer
  viewer.className = `language-${language}`;
  viewer.textContent = content;
  
  // Re-highlight
  if (typeof Prism !== 'undefined') {
    Prism.highlightElement(viewer);
  }
}

/**
 * Find the first non-folder file
 */
function findFirstFile(filesData) {
  if (!filesData.files || filesData.files.length === 0) return null;
  return filesData.files[0];
}

/**
 * Load the default file: try README.md first, then fall back to first file
 */
function loadDefaultFile(filesData) {
  // Try to find README.md (case-insensitive)
  const readmeFile = filesData.files.find(f => 
    f.path.toLowerCase() === 'readme.md' || 
    f.path.toLowerCase().endsWith('/readme.md')
  );
  
  if (readmeFile) {
    selectFileByPath(readmeFile.path, filesData);
  } else {
    // Fall back to first file
    const firstFile = findFirstFile(filesData);
    if (firstFile) {
      selectFileByPath(firstFile.path, filesData);
    }
  }
}

/**
 * Initialize panel toggle buttons
 */
function initPanelToggles() {
  document.querySelectorAll('.panel-toggle').forEach(toggle => {
    toggle.addEventListener('click', function() {
      const panel = this.closest('.gallery-sidebar');
      if (panel) {
        panel.classList.toggle('collapsed');
      }
    });
  });
}

/**
 * Initialize copy code button
 */
function initCopyCodeButton() {
  const copyBtn = document.getElementById('copy-code');
  if (!copyBtn) return;
  
  copyBtn.addEventListener('click', async function() {
    const viewer = document.getElementById('code-viewer');
    if (!viewer) return;
    
    try {
      await navigator.clipboard.writeText(viewer.textContent);
      
      // Visual feedback
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
}

/**
 * Initialize keyboard navigation
 */
function initKeyboardNavigation(filesData) {
  document.addEventListener('keydown', function(e) {
    const activeItem = document.querySelector('.file-tree-item.active');
    if (!activeItem) return;
    
    const allItems = Array.from(document.querySelectorAll('.file-tree-item:not(.folder)'));
    const currentIndex = allItems.indexOf(activeItem);
    
    let newIndex = currentIndex;
    
    switch (e.key) {
      case 'ArrowDown':
      case 'j':
        e.preventDefault();
        newIndex = Math.min(currentIndex + 1, allItems.length - 1);
        break;
      case 'ArrowUp':
      case 'k':
        e.preventDefault();
        newIndex = Math.max(currentIndex - 1, 0);
        break;
      default:
        return;
    }
    
    if (newIndex !== currentIndex && allItems[newIndex]) {
      const path = allItems[newIndex].dataset.path;
      selectFile(allItems[newIndex], path, filesData);
      allItems[newIndex].scrollIntoView({ block: 'nearest' });
    }
  });
}

/**
 * Utility: Get file extension
 */
function getFileExtension(path) {
  const parts = path.split('.');
  return parts.length > 1 ? parts.pop().toLowerCase() : '';
}

/**
 * Utility: Get Prism language from extension
 */
function getPrismLanguage(extension) {
  const map = {
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
    'mod': 'go',
    'sln': 'plaintext'
  };
  return map[extension] || 'plaintext';
}

/**
 * Utility: Escape HTML
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Gallery index page: Filter functionality
 */
function initGalleryFilters() {
  const filterTabs = document.querySelectorAll('.filter-tab');
  const galleryCards = document.querySelectorAll('.gallery-card');
  
  filterTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      const filterType = this.dataset.filterType;
      const filterValue = this.dataset.filterValue;
      
      // Update active tab in this group
      const group = this.closest('.filter-tabs');
      group.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      
      // Apply filters
      applyFilters();
    });
  });
  
  function applyFilters() {
    const activeFilters = {};
    document.querySelectorAll('.filter-tab.active').forEach(tab => {
      const type = tab.dataset.filterType;
      const value = tab.dataset.filterValue;
      if (value !== 'all') {
        activeFilters[type] = value;
      }
    });
    
    galleryCards.forEach(card => {
      let visible = true;
      
      for (const [type, value] of Object.entries(activeFilters)) {
        if (card.dataset[type] !== value) {
          visible = false;
          break;
        }
      }
      
      card.style.display = visible ? '' : 'none';
    });
  }
}

// Initialize filters if on gallery index page
if (document.querySelector('.gallery-filters')) {
  document.addEventListener('DOMContentLoaded', initGalleryFilters);
}
