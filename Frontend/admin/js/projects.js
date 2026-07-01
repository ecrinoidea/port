let projects = [];

async function loadProjects() {
    try {
        console.log('📥 Loading projects...');
        const res = await apiCall('/api/admin/projects');
        if (!res.success) {
            console.warn('⚠️  Load projects failed:', res.message);
            showToast(res.message || 'Gagal load projects', 'error');
            return;
        }
        projects = res.data || [];
        console.log(`✅ Loaded ${projects.length} projects`);
        renderTable();
    } catch (err) {
        console.error('❌ Error in loadProjects:', err);
        showToast('Terjadi kesalahan saat load projects', 'error');
    }
}

function renderTable() {
    const tbody = document.getElementById('projBody');
    if (!projects.length) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#a09ab8;padding:24px;">Belum ada proyek</td></tr>';
        return;
    }
    tbody.innerHTML = projects.map(p => `
        <tr>
            <td>${p.image_url ? `<img src="${p.image_url}" class="img-thumb" onerror="this.style.display='none'">` : '—'}</td>
            <td><strong>${p.title}</strong><br><small style="color:#a09ab8;">${(p.description||'').substring(0,60)}${p.description && p.description.length > 60 ? '...' : ''}</small></td>
            <td><small style="color:#8b83a4;">${p.tech_stack || '—'}</small></td>
            <td>${p.is_featured ? '<span class="badge badge-amber">⭐ Featured</span>' : '—'}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="editProj(${p.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="confirmDelete(() => deleteProj(${p.id}))">Hapus</button>
            </td>
        </tr>
    `).join('');
}

function resetForm() {
    document.getElementById('projId').value = '';
    document.getElementById('modalTitle').textContent = 'Tambah Proyek';
    ['pjTitle','pjDesc','pjTech','pjImage','pjDemo','pjRepo'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('pjFeatured').checked = false;
}

function editProj(id) {
    const p = projects.find(x => x.id === id);
    if (!p) return;
    document.getElementById('projId').value = p.id;
    document.getElementById('modalTitle').textContent = 'Edit Proyek';
    document.getElementById('pjTitle').value = p.title || '';
    document.getElementById('pjDesc').value = p.description || '';
    document.getElementById('pjTech').value = p.tech_stack || '';
    document.getElementById('pjImage').value = p.image_url || '';
    document.getElementById('pjDemo').value = p.demo_url || '';
    document.getElementById('pjRepo').value = p.repo_url || '';
    document.getElementById('pjFeatured').checked = !!p.is_featured;
    openModal('projModal');
}

async function saveProj() {
    const id = document.getElementById('projId').value;
    const body = {
        title: document.getElementById('pjTitle').value.trim(),
        description: document.getElementById('pjDesc').value.trim(),
        tech_stack: document.getElementById('pjTech').value.trim(),
        image_url: document.getElementById('pjImage').value.trim(),
        demo_url: document.getElementById('pjDemo').value.trim(),
        repo_url: document.getElementById('pjRepo').value.trim(),
        is_featured: document.getElementById('pjFeatured').checked ? 1 : 0
    };
    if (!body.title) { alert('Judul proyek wajib diisi'); return; }
    try {
        const url = id ? `/api/admin/projects/${id}` : '/api/admin/projects';
        const method = id ? 'PUT' : 'POST';
        console.log(`📤 ${method} ${url}`, body);
        const res = await apiCall(url, method, body);
        if (res.success) {
            showToast(res.message || 'Berhasil disimpan', 'success');
            closeModal('projModal');
            loadProjects();
        } else {
            showToast(res.message || 'Gagal', 'error');
        }
    } catch (err) {
        console.error('❌ Error in saveProj:', err);
        showToast('Terjadi kesalahan saat save', 'error');
    }
}

async function deleteProj(id) {
    try {
        console.log(`📤 DELETE /api/admin/projects/${id}`);
        const res = await apiCall(`/api/admin/projects/${id}`, 'DELETE');
        if (res.success) {
            showToast(res.message || 'Berhasil dihapus', 'success');
            loadProjects();
        } else {
            showToast(res.message || 'Gagal dihapus', 'error');
        }
    } catch (err) {
        console.error('❌ Error in deleteProj:', err);
        showToast('Terjadi kesalahan saat hapus', 'error');
    }
}

// File upload trigger
document.getElementById('projImgFile').addEventListener('change', async function() {
    const file = this.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/api/admin/upload', { method: 'POST', body: formData });
    const data = await res.json();
    if (data.success) {
        document.getElementById('pjImage').value = data.url;
        showToast('Gambar diupload ke Cloudinary', 'success');
    } else {
        showToast(data.message, 'error');
    }
});

loadProjects();
