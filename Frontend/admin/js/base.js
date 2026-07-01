// Toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => { toast.className = 'toast'; }, 3200);
}

// Open/close modal
function openModal(id) {
    document.getElementById(id).classList.add('open');
}
function closeModal(id) {
    document.getElementById(id).classList.remove('open');
}

// Generic API call with better error handling
async function apiCall(url, method = 'GET', body = null) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) opts.body = JSON.stringify(body);
    try {
        console.log(`📤 API: ${method} ${url}`, body || '');
        const res = await fetch(url, opts);
        const data = await res.json();
        console.log(`📥 Response: ${res.status}`, data);
        
        if (!res.ok) {
            console.warn(`⚠️  API error: ${res.status}`, data);
            data.success = false;
            data.message = data.message || `HTTP ${res.status}: ${res.statusText}`;
        }
        return data;
    } catch (err) {
        console.error('❌ API call error:', err);
        return { success: false, message: `Error: ${err.message}` };
    }
}

// Confirm delete
function confirmDelete(callback) {
    if (confirm('Yakin ingin menghapus data ini?')) callback();
}

console.log('✅ Base.js loaded');
