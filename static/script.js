const ITEMS_PER_PAGE = 5;
let currentPage = 1;
let totalItems = 0;
let allUrls = [];

function showAddForm() {
    document.getElementById('input-section').classList.remove('hidden');
}

function showNotification(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="toast-header bg-${type === 'success' ? 'success' : 'danger'} text-white">
            <strong class="me-auto">${type === 'success' ? 'Success' : 'Error'}</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    document.querySelector('.toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
}

document.addEventListener('DOMContentLoaded', () => {
    // Load initial data
    loadCollection();
    
    // Setup event listeners
    document.getElementById('search-input')?.addEventListener('input', handleSearch);
    document.getElementById('sort-select')?.addEventListener('change', handleSort);
    
    // URL input validation
    document.getElementById('url-input')?.addEventListener('input', (e) => {
        const isValid = /^https?:\/\/.+/.test(e.target.value);
        e.target.classList.toggle('is-invalid', !isValid);
        document.getElementById('add-url-button').disabled = !isValid;
    });
    
    document.querySelectorAll('input[name="time-filter"]').forEach(radio => {
        radio.addEventListener('change', handleTimeFilter);
    });
    document.querySelectorAll('input[name="status-filter"]').forEach(radio => {
        radio.addEventListener('change', handleStatusFilter);
    });

    // Modal event listeners
    const urlModal = document.getElementById('url-modal');
    if (urlModal) {
        urlModal.addEventListener('click', (e) => {
            if (e.target.id === 'url-modal') {
                const modal = bootstrap.Modal.getInstance(urlModal);
                modal?.hide();
            }
        });
    }

    // Escape key handler
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modal = bootstrap.Modal.getInstance(document.getElementById('urlModal'));
            modal?.hide();
        }
    });
});

function renderCurrentPage() {
    const list = document.getElementById('url-list');
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const pageItems = allUrls.slice(startIndex, endIndex);

    // Batch DOM updates using DocumentFragment
    const fragment = document.createDocumentFragment();
    pageItems.forEach(entry => {
        const div = document.createElement('div');
        div.className = "list-group-item d-flex align-items-center position-relative";
        div.innerHTML = `
            <div class="flex-shrink-0 me-3" style="width: 64px; height: 64px;">
                ${entry.thumbnail ? `
                    <img src="${entry.thumbnail}" alt="" 
                        class="img-fluid rounded shadow-sm" 
                        style="transition: transform 0.2s ease"
                        onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' class=\'h-100 w-100 text-secondary\' viewBox=\'0 0 24 24\'%3E%3Crect width=\'24\' height=\'24\' fill=\'%23f3f4f6\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23666\' font-size=\'8\'%3E${entry.title.charAt(0)}%3C/text%3E%3C/svg%3E';">
                ` : `
                    <div class="w-100 h-100 rounded bg-light d-flex align-items-center justify-content-center">
                        <span class="text-secondary" style="font-size: 24px;">${entry.title.charAt(0).toUpperCase()}</span>
                    </div>
                `}
            </div>
            <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2">
                    <a href="${entry.url}" target="_blank" 
                       class="text-decoration-none position-relative text-primary"
                       style="transition: all 0.2s ease">
                        ${entry.title || entry.url}
                        <i class="fas fa-external-link-alt ms-2 opacity-0" 
                           style="transition: all 0.2s ease"></i>
                    </a>
                    <i class="fas ${entry.isRead ? 'fa-eye text-success' : 'fa-eye-slash text-muted'}" 
                       style="font-size: 14px;"></i>
                    ${entry.clickCount > 0 ? `
                        <span class="badge bg-primary rounded-pill" title="Click count">
                            ${entry.clickCount}
                        </span>
                    ` : ''}
                </div>
                <div class="small text-muted mt-1">${formatDate(entry.added)}</div>
            </div>
            <div class="d-flex gap-2">
                <button class="btn btn-outline-primary btn-sm" 
                    onclick="showEditModal('${entry.url}')"
                    title="Edit URL">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-outline-secondary btn-sm" 
                    onclick="summarizeUrl('${encodeURIComponent(entry.url)}')"
                    title="Summarize">
                    <i class="fas fa-robot"></i>
                </button>
                <div class="dropdown">
                    <button class="btn btn-outline-danger btn-sm ms-3" 
                        data-bs-toggle="dropdown" 
                        title="Delete URL">
                        <i class="fas fa-trash"></i>
                    </button>
                    <div class="dropdown-menu p-2 text-center">
                        <p class="mb-2">Are you sure?</p>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-secondary" data-bs-dismiss="dropdown">Cancel</button>
                            <button class="btn btn-sm btn-danger" onclick="deleteUrl('${entry.url}')" data-bs-dismiss="dropdown">Delete</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add click handler for the link
        const link = div.querySelector('a');
        const readIcon = div.querySelector('.fa-eye, .fa-eye-slash');
        link.addEventListener('click', (e) => {
            readIcon.className = 'fas fa-eye text-success';
            updateUrlReadStatus(entry.url, true);
            incrementClickCount(entry.url);
        });
        initializeTooltip(div, entry);
        div.addEventListener('mouseenter', () => {
            div.classList.add('shadow-sm', 'bg-light');
            div.querySelector('.fa-external-link-alt').style.opacity = '1';
            if (entry.thumbnail) {
                div.querySelector('img').style.transform = 'scale(1.05)';
            }
        });
        div.addEventListener('mouseleave', () => {
            div.classList.remove('shadow-sm', 'bg-light');
            div.querySelector('.fa-external-link-alt').style.opacity = '0';
            if (entry.thumbnail) {
                div.querySelector('img').style.transform = 'scale(1)';
            }
        });
        fragment.appendChild(div);
    });

    list.innerHTML = '';
    list.appendChild(fragment);

    cleanupTooltips();
    updatePaginationInfo();
}

function updatePagination() {
    const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage === totalPages;
    document.getElementById('url-count').textContent = `${totalItems} URLs saved`;
    updatePaginationInfo();
}

function updatePaginationInfo() {
    const startItem = (currentPage - 1) * ITEMS_PER_PAGE + 1;
    const endItem = Math.min(currentPage * ITEMS_PER_PAGE, totalItems);
    const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
    
    document.getElementById('pagination-info').textContent = 
        `Showing ${startItem}-${endItem} of ${totalItems} • Page ${currentPage} of ${totalPages}`;
}

function changePage(direction) {
    if (direction === 'prev' && currentPage > 1) {
        currentPage--;
    } else if (direction === 'next' && currentPage < Math.ceil(totalItems / ITEMS_PER_PAGE)) {
        currentPage++;
    }
    renderCurrentPage();
    updatePagination();
}

function toggleAddLoading(isLoading) {
    const button = document.querySelector('#add-url-button');
    const loadingText = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Adding...
    `;
    button.disabled = isLoading;
    button.innerHTML = isLoading ? loadingText : '<i class="fas fa-plus me-2"></i> Add URL';
}

function addUrl() {
    const input = document.getElementById('url-input');
    const url = input.value.trim();
    
    if (!url) {
        showNotification('Please enter a URL', 'error');
        input.classList.add('is-invalid');
        return;
    }
    
    toggleAddLoading(true);
    fetch('/api/urls/add_url', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url })
    }).then(res => {
        if (res.status === 409) {
            throw new Error('duplicate');
        }
        if (!res.ok) {
            throw new Error('failed');
        }
        return res.json();
    }).then(data => {
        // Close modal using Bootstrap's modal API
        const modal = bootstrap.Modal.getInstance(document.getElementById('urlModal'));
        modal.hide();
        input.value = '';
        showNotification('URL added successfully');
        // Reload the collection
        loadCollection();
    })
    .catch((err) => {
        if (err.message === 'duplicate') {
            showNotification('This URL already exists in your collection', 'error');
            input.classList.add('is-invalid');
        } else {
            showNotification('Failed to add URL. Please try again.', 'error');
        }
    })
    .finally(() => {
        toggleAddLoading(false);
    });
}

function deleteUrl(url) {
    fetch('/api/urls/delete_url', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url })
    }).then(() => {
        loadCollection();
        showNotification('URL deleted successfully');
    })
    .catch(() => showNotification('Failed to delete URL', 'error'));
}

function cancelAdd() {
    document.getElementById('input-section').classList.add('hidden');
    document.getElementById('url-input').value = '';
}

function handleSearch() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    if (!searchInput.trim()) {
        // Reset to original list if search is empty
        allUrls = [...originalUrlsList];
        totalItems = allUrls.length;
        currentPage = 1;
        updatePagination();
        renderCurrentPage();
        return;
    }

    const keywords = searchInput.split(' ').filter(k => k.length > 0);
    const filteredUrls = originalUrlsList.filter(item => {
        const title = (item.title || '').toLowerCase();
        return keywords.every(keyword => title.includes(keyword));
    });
    
    totalItems = filteredUrls.length;
    currentPage = 1;
    allUrls = filteredUrls;
    updatePagination();
    renderCurrentPage();
}

function handleSort() {
    const sortValue = document.getElementById('sort-select').value;
    
    allUrls.sort((a, b) => {
        const aText = a.title || a.url;
        const bText = b.title || b.url;
        const aDate = new Date(a.added);
        const bDate = new Date(b.added);
        
        switch(sortValue) {
            case 'newest': return bDate - aDate;
            case 'oldest': return aDate - bDate;
            case 'az': return aText.localeCompare(bText);
            case 'za': return bText.localeCompare(aText);
            default: return 0;
        }
    });
    
    renderCurrentPage();
}

function handleTimeFilter() {
    const timeFilter = document.querySelector('input[name="time-filter"]:checked').value;
    
    if (timeFilter === 'all') {
        // Reset to original list for 'all' filter
        allUrls = [...originalUrlsList];
        totalItems = allUrls.length;
        currentPage = 1;
        updatePagination();
        renderCurrentPage();
        return;
    }

    const now = new Date();
    const originalUrls = [...allUrls]; // Keep original array
    
    const filteredUrls = originalUrls.filter(item => {
        const itemDate = new Date(item.added);
        
        switch(timeFilter) {
            case 'today':
                return itemDate.toDateString() === now.toDateString();
            case 'week':
                const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                return itemDate >= weekAgo;
            case 'month':
                const monthAgo = new Date(now.getTime());
                monthAgo.setMonth(monthAgo.getMonth() - 1);
                return itemDate >= monthAgo;
            default: // 'all'
                return true;
        }
    });
    
    totalItems = filteredUrls.length;
    currentPage = 1;
    allUrls = filteredUrls;
    updatePagination();
    renderCurrentPage();
}

function handleStatusFilter() {
    const statusFilter = document.querySelector('input[name="status-filter"]:checked').value;
    
    if (statusFilter === 'all') {
        allUrls = [...originalUrlsList];
        totalItems = allUrls.length;
        currentPage = 1;
        updatePagination();
        renderCurrentPage();
        return;
    }

    const filteredUrls = originalUrlsList.filter(item => {
        if (statusFilter === 'read') {
            return item.isRead === true;
        } else {
            return !item.isRead;
        }
    });
    
    totalItems = filteredUrls.length;
    currentPage = 1;
    allUrls = filteredUrls;
    updatePagination();
    renderCurrentPage();
}

// Update the existing loadCollection function to include URL count
let originalUrlsList = []; // Add this at the top with other variables
function loadCollection() {
    cleanupTooltips();
    const list = document.getElementById('url-list');
    list.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div></div>';
    
    fetch('/api/urls/get_urls')  // Updated URL
    .then(res => res.json())
    .then(data => {
        if (!Array.isArray(data)) {
            throw new Error('Invalid data format');
        }
        originalUrlsList = [...data];
        // Sort by newest first
        data.sort((a, b) => new Date(b.added) - new Date(a.added));
        allUrls = data;
        totalItems = data.length;
        // Set sort select to 'newest'
        document.getElementById('sort-select').value = 'newest';
        updatePagination();
        renderCurrentPage();
    })
    .catch((error) => {
        console.error('Error loading URLs:', error);
        list.innerHTML = `
            <div class="alert alert-danger text-center" role="alert">
                Failed to load URLs. Please try again.
            </div>
        `;
    });
}

// Clean up tooltips before updating content
function cleanupTooltips() {
    // Update tooltip cleanup to handle all tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"], .tooltip');
    tooltips.forEach(element => {
        const tooltip = bootstrap.Tooltip.getInstance(element);
        if (tooltip) {
            tooltip.dispose();
        }
        // Also remove any orphaned tooltip elements
        if (element.classList.contains('tooltip')) {
            element.remove();
        }
    });
}

// Add new function for tooltip initialization
function initializeTooltip(element, entry) {
    cleanupTooltips(); // Clean up before creating new tooltip
    
    const tooltip = new bootstrap.Tooltip(element, {
        template: `
            <div class="tooltip" role="tooltip">
                <div class="tooltip-arrow"></div>
                <div class="tooltip-inner"></div>
            </div>
        `,
        title: `
            <div style="max-width: 250px;">
                ${entry.thumbnail ? `
                    <img src="${entry.thumbnail}" class="img-fluid rounded mb-2" 
                         style="max-height: 150px; width: 100%; object-fit: cover;"
                         onerror="this.style.display='none'">
                ` : ''}
                <div class="fw-bold mb-1">${entry.title || entry.url}</div>
                <div class="small text-muted">
                    ${entry.clickCount ? `Visited ${entry.clickCount} ${entry.clickCount === 1 ? 'time' : 'times'}` : 'Not visited yet'}
                </div>
            </div>
        `,
        html: true,
        delay: { show: 300, hide: 100 },
        placement: 'top',
        trigger: 'hover'
    });

    // Add event listener to cleanup tooltip when element is removed
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList' && !document.contains(element)) {
                tooltip.dispose();
                observer.disconnect();
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Update the observer initialization
document.addEventListener('DOMContentLoaded', () => {
    const urlList = document.getElementById('url-list');
    if (!urlList) return;

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList') {
                // Clean up existing tooltips before reinitializing
                cleanupTooltips();
                
                // Reinitialize tooltips for new elements
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element node
                        const entry = allUrls.find(url => 
                            url.url === node.querySelector('a')?.href
                        );
                        if (entry) {
                            initializeTooltip(node, entry);
                        }
                    }
                });
            }
        });
    });

    observer.observe(urlList, {
        childList: true,
        subtree: true
    });
});

function resetFilters() {
    allUrls = [...originalUrlsList];
    // Sort by newest first
    allUrls.sort((a, b) => new Date(b.added) - new Date(a.added));
    totalItems = allUrls.length;
    currentPage = 1;
    document.getElementById('search-input').value = '';
    document.getElementById('sort-select').value = 'newest';
    document.querySelector('input[name="time-filter"][value="all"]').checked = true;
    document.querySelector('input[name="status-filter"][value="all"]').checked = true;
    updatePagination();
    renderCurrentPage();
}

function showEditModal(url) {
    const entry = allUrls.find(item => item.url === url);
    if (!entry) return;

    document.getElementById('edit-url-id').value = url;
    document.getElementById('edit-title-input').value = entry.title || '';
    document.getElementById('edit-url-input').value = entry.url;
    document.getElementById('edit-thumbnail-input').value = entry.thumbnail || '';

    const modal = new bootstrap.Modal(document.getElementById('editUrlModal'));
    modal.show();
}

function saveUrlEdit() {
    const url = document.getElementById('edit-url-id').value;
    const title = document.getElementById('edit-title-input').value;
    const thumbnail = document.getElementById('edit-thumbnail-input').value;

    fetch('/api/urls/edit_url', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url, title, thumbnail })
    }).then(res => {
        if (!res.ok) throw new Error('failed');
        return res.json();
    }).then(() => {
        const modal = bootstrap.Modal.getInstance(document.getElementById('editUrlModal'));
        modal.hide();
        showNotification('URL updated successfully');
        loadCollection();
    })
    .catch(() => showNotification('Failed to update URL', 'error'));
}

// Add this helper function
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = now - date;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        const hours = Math.floor(diffTime / (1000 * 60 * 60));
        if (hours === 0) {
            const minutes = Math.floor(diffTime / (1000 * 60));
            return `${minutes} min ago`;
        }
        return `${hours}h ago`;
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`;
    } else if (diffDays < 365) {
        const months = Math.floor(diffDays / 30);
        return `${months} ${months === 1 ? 'month' : 'months'} ago`;
    }
    return date.toLocaleDateString();
}

function updateUrlReadStatus(url, isRead) {
    fetch('/api/urls/update_url_status', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url, isRead })
    }).then(() => loadCollection());
}

function incrementClickCount(url) {
    fetch('/api/urls/increment_click', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url })
    });
}

function showQueueModal() {
    fetch('/api/queue/get_queue')
        .then(res => res.json())
        .then(data => {
            const tableBody = document.getElementById('queueTable');
            tableBody.innerHTML = data.map((item, index) => `
                <tr>
                    <td>
                        <input type="checkbox" class="form-check-input queue-item" 
                               data-title="${item.title}"
                               data-url="${item.url}" 
                               onchange="updateMoveButton()">
                    </td>
                    <td>${item.title}</td>
                    <td>${formatDate(item.added)}</td>
                </tr>
            `).join('');
            
            const queueModal = new bootstrap.Modal(document.getElementById('queueModal'));
            queueModal.show();
        })
        .catch(() => showNotification('Failed to load queued URLs', 'error'));
}

function toggleAllQueueItems() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.queue-item');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
    updateMoveButton();
}

function updateMoveButton() {
    const selectedItems = document.querySelectorAll('.queue-item:checked');
    document.getElementById('moveSelectedBtn').disabled = selectedItems.length === 0;
}

async function moveSelectedUrls() {
    const moveBtn = document.getElementById('moveSelectedBtn');
    const btnText = moveBtn.querySelector('span');
    const originalText = btnText.textContent;
    
    try {
        moveBtn.disabled = true;
        btnText.textContent = 'Moving...';
        
        // Get selected items with their titles
        const selectedItems = Array.from(document.querySelectorAll('.queue-item:checked'))
            .map(cb => (
                cb.getAttribute('data-url')
            ));
        console.log('Selected items:', selectedItems);
        if (selectedItems.length === 0) {
            showNotification('No items selected to move', 'error');
            return;
        }

        const response = await fetch('/api/queue/move_queued_urls', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ items: selectedItems })
        });

        if (!response.ok) throw new Error('Failed to move items');

        showNotification('Selected items moved successfully');
        closeQueueModal();
        loadCollection();
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        moveBtn.disabled = false;
        btnText.textContent = originalText;
    }
}

function closeQueueModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('queueModal'));
    modal?.hide();
}

// Add mutation observer to handle dynamic content updates
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
            // Reinitialize tooltips for new elements
            const tooltips = mutation.target.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltips.forEach(element => {
                new bootstrap.Tooltip(element);
            });
        }
    });
});

// Start observing dynamic content areas
document.addEventListener('DOMContentLoaded', () => {
    // Observe URL list for changes
    observer.observe(document.getElementById('url-list'), {
        childList: true,
        subtree: true
    });
});

// Improve modal cleanup
function cleanupModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    
    // Clear form inputs
    modal.querySelectorAll('input').forEach(input => {
        input.value = '';
        input.classList.remove('is-invalid');
    });
    
    // Remove any error messages
    modal.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
}

// Add debouncing for search input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const debouncedSearch = debounce(() => {
    handleSearch();
}, 300);

// Update search input handler
document.getElementById('search-input')?.addEventListener('input', debouncedSearch);

// Remove the old summarizeUrl function and replace with:
function summarizeUrl(url) {
    const modal = new bootstrap.Modal(document.getElementById('summarizeModal'));
    document.getElementById('summarize-loading').classList.remove('d-none');
    document.getElementById('summarize-result').innerText = '';
    document.getElementById('ai-summary-section').classList.add('d-none');
    modal.show();
    fetch('/api/urls/summarize_url', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url: decodeURIComponent(url) })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('summarize-loading').classList.add('d-none');
        let summary = data.summary || '';
        // Split <think>...</think> if present
        const { aiSummary, mainContent } = splitSummary(summary);
        if (aiSummary) {
            document.getElementById('ai-summary-content').innerText = aiSummary;
            document.getElementById('ai-summary-section').classList.remove('d-none');
        } else {
            document.getElementById('ai-summary-section').classList.add('d-none');
        }
        document.getElementById('summarize-result').innerText = mainContent || 'No summary available.';
    })
    .catch(() => {
        document.getElementById('summarize-loading').classList.add('d-none');
        document.getElementById('summarize-result').innerText = 'Failed to summarize.';
        document.getElementById('ai-summary-section').classList.add('d-none');
    });
}

// Add this helper function near the top or before summarizeUrl
function splitSummary(raw) {
    const thinkMatch = raw.match(/<think>([\s\S]*?)<\/think>/i);
    let aiSummary = '';
    let mainContent = raw;
    if (thinkMatch) {
        aiSummary = thinkMatch[1].trim();
        mainContent = raw.replace(thinkMatch[0], '').trim();
    }
    return { aiSummary, mainContent };
}

// Add this function if not already present
function toggleThinkSummary() {
  const content = document.getElementById('ai-summary-content');
  const btnText = document.getElementById('think-toggle-text');
  if (content.classList.contains('d-none')) {
    content.classList.remove('d-none');
    btnText.textContent = 'Hide Think';
  } else {
    content.classList.add('d-none');
    btnText.textContent = 'Show Think';
  }
}
