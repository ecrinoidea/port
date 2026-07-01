let skills = [];

async function loadSkills() {
    try {
        console.log('📥 Loading skills...');
        const res = await apiCall('/api/admin/skills');
        if (!res.success) {
            console.warn('⚠️  Load skills failed:', res.message);
            showToast(res.message || 'Gagal load skills', 'error');
            return;
        }
        skills = res.data || [];
        console.log(`✅ Loaded ${skills.length} skills`);
        renderTable();
    } catch (err) {
        console.error('❌ Error in loadSkills:', err);
        showToast('Terjadi kesalahan saat load skills', 'error');
    }
}

const catColors = { Backend: 'badge-purple', Frontend: 'badge-sage', Database: 'badge-amber', Tools: 'badge-blush' };

function renderTable() {
    const tbody = document.getElementById('skillBody');
    if (!skills.length) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#a09ab8;padding:24px;">Belum ada skill</td></tr>';
        return;
    }
    tbody.innerHTML = skills.map(s => `
        <tr>
            <td><strong>${s.name}</strong></td>
            <td>${s.category ? `<span class="badge ${catColors[s.category] || 'badge-purple'}">${s.category}</span>` : '—'}</td>
            <td>
                <div style="display:flex; align-items:center; gap:10px; min-width:160px;">
                    <div class="progress-bar" style="flex:1;">
                        <div class="progress-fill" style="width:${s.level}%"></div>
                    </div>
                    <span style="font-size:12px; color:#8b83a4; min-width:32px;">${s.level}%</span>
                </div>
            </td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="editSkill(${s.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="confirmDelete(() => deleteSkill(${s.id}))">Hapus</button>
            </td>
        </tr>
    `).join('');
}

function resetForm() {
    document.getElementById('skillId').value = '';
    document.getElementById('modalTitle').textContent = 'Tambah Skill';
    document.getElementById('sName').value = '';
    document.getElementById('sCategory').value = '';
    document.getElementById('sLevel').value = 80;
    document.getElementById('levelVal').textContent = '80';
}

function editSkill(id) {
    const s = skills.find(x => x.id === id);
    if (!s) return;
    document.getElementById('skillId').value = s.id;
    document.getElementById('modalTitle').textContent = 'Edit Skill';
    document.getElementById('sName').value = s.name || '';
    document.getElementById('sCategory').value = s.category || '';
    document.getElementById('sLevel').value = s.level || 80;
    document.getElementById('levelVal').textContent = s.level || 80;
    openModal('skillModal');
}

async function saveSkill() {
    const id = document.getElementById('skillId').value;
    const body = {
        name: document.getElementById('sName').value.trim(),
        category: document.getElementById('sCategory').value.trim(),
        level: parseInt(document.getElementById('sLevel').value)
    };
    if (!body.name) { alert('Nama skill wajib diisi'); return; }
    try {
        const url = id ? `/api/admin/skills/${id}` : '/api/admin/skills';
        const method = id ? 'PUT' : 'POST';
        console.log(`📤 ${method} ${url}`, body);
        const res = await apiCall(url, method, body);
        if (res.success) {
            showToast(res.message || 'Berhasil disimpan', 'success');
            closeModal('skillModal');
            loadSkills();
        } else {
            showToast(res.message || 'Gagal', 'error');
        }
    } catch (err) {
        console.error('❌ Error in saveSkill:', err);
        showToast('Terjadi kesalahan saat save', 'error');
    }
}

async function deleteSkill(id) {
    try {
        console.log(`📤 DELETE /api/admin/skills/${id}`);
        const res = await apiCall(`/api/admin/skills/${id}`, 'DELETE');
        if (res.success) {
            showToast(res.message || 'Berhasil dihapus', 'success');
            loadSkills();
        } else {
            showToast(res.message || 'Gagal dihapus', 'error');
        }
    } catch (err) {
        console.error('❌ Error in deleteSkill:', err);
        showToast('Terjadi kesalahan saat hapus', 'error');
    }
}

loadSkills();
