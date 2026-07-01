let exps = [];

async function loadExps() {
    try {
        console.log('📥 Loading experiences...');
        const res = await apiCall('/api/admin/experiences');
        if (!res.success) {
            console.warn('⚠️  Load experiences failed:', res.message);
            showToast(res.message || 'Gagal load experiences', 'error');
            return;
        }
        exps = res.data || [];
        console.log(`✅ Loaded ${exps.length} experiences`);
        renderTable();
    } catch (err) {
        console.error('❌ Error in loadExps:', err);
        showToast('Terjadi kesalahan saat load experiences', 'error');
    }
}

function renderTable() {
    const tbody = document.getElementById('expBody');
    if (!exps.length) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#a09ab8;padding:24px;">Belum ada data pengalaman</td></tr>';
        return;
    }
    tbody.innerHTML = exps.map(e => `
        <tr>
            <td><strong>${e.company}</strong></td>
            <td>${e.position}</td>
            <td>${e.start_date || '—'} – ${e.is_current ? 'Sekarang' : (e.end_date || '—')}</td>
            <td>${e.is_current ? '<span class="badge badge-sage">Aktif</span>' : '<span class="badge badge-purple">Selesai</span>'}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="editExp(${e.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="confirmDelete(() => deleteExp(${e.id}))">Hapus</button>
            </td>
        </tr>
    `).join('');
}

function resetForm() {
    document.getElementById('expId').value = '';
    document.getElementById('modalTitle').textContent = 'Tambah Pengalaman';
    ['eCompany','ePosition','eStart','eEnd','eDesc'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('eCurrent').checked = false;
}

function editExp(id) {
    const e = exps.find(x => x.id === id);
    if (!e) return;
    document.getElementById('expId').value = e.id;
    document.getElementById('modalTitle').textContent = 'Edit Pengalaman';
    document.getElementById('eCompany').value = e.company || '';
    document.getElementById('ePosition').value = e.position || '';
    document.getElementById('eStart').value = e.start_date || '';
    document.getElementById('eEnd').value = e.end_date || '';
    document.getElementById('eCurrent').checked = !!e.is_current;
    document.getElementById('eDesc').value = e.description || '';
    openModal('expModal');
}

async function saveExp() {
    const id = document.getElementById('expId').value;
    const body = {
        company: document.getElementById('eCompany').value.trim(),
        position: document.getElementById('ePosition').value.trim(),
        start_date: document.getElementById('eStart').value.trim(),
        end_date: document.getElementById('eEnd').value.trim(),
        is_current: document.getElementById('eCurrent').checked ? 1 : 0,
        description: document.getElementById('eDesc').value.trim()
    };
    if (!body.company || !body.position) { alert('Perusahaan dan posisi wajib diisi'); return; }
    try {
        const url = id ? `/api/admin/experiences/${id}` : '/api/admin/experiences';
        const method = id ? 'PUT' : 'POST';
        console.log(`📤 ${method} ${url}`, body);
        const res = await apiCall(url, method, body);
        if (res.success) {
            showToast(res.message || 'Berhasil disimpan', 'success');
            closeModal('expModal');
            loadExps();
        } else {
            showToast(res.message || 'Gagal', 'error');
        }
    } catch (err) {
        console.error('❌ Error in saveExp:', err);
        showToast('Terjadi kesalahan saat save', 'error');
    }
}

async function deleteExp(id) {
    try {
        console.log(`📤 DELETE /api/admin/experiences/${id}`);
        const res = await apiCall(`/api/admin/experiences/${id}`, 'DELETE');
        if (res.success) {
            showToast(res.message || 'Berhasil dihapus', 'success');
            loadExps();
        } else {
            showToast(res.message || 'Gagal dihapus', 'error');
        }
    } catch (err) {
        console.error('❌ Error in deleteExp:', err);
        showToast('Terjadi kesalahan saat hapus', 'error');
    }
}

loadExps();
