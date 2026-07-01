async function loadContacts() {
    try {
        console.log('📥 Loading contacts...');
        const res = await apiCall('/api/admin/contacts');
        if (!res.success) {
            console.warn('⚠️  Load contacts failed:', res.message);
            showToast(res.message || 'Gagal load contacts', 'error');
            return;
        }
        const contacts = res.data || [];
        const tbody = document.getElementById('contactBody');
        if (!contacts.length) {
            console.warn('⚠️  No contacts found');
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#a09ab8;padding:24px;">Belum ada pesan masuk</td></tr>';
            return;
        }
        console.log(`✅ Loaded ${contacts.length} contacts`);
        tbody.innerHTML = contacts.map(c => `
            <tr>
                <td><strong>${c.name}</strong></td>
                <td><a href="mailto:${c.email}" style="color:#8b78b8; text-decoration:none;">${c.email}</a></td>
                <td>${c.subject || '—'}</td>
                <td style="max-width:240px; color:#6b6480;">${c.message}</td>
                <td style="color:#a09ab8; font-size:12px; white-space:nowrap;">${formatDate(c.created_at)}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="confirmDelete(() => deleteContact(${c.id}))">Hapus</button>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        console.error('❌ Error in loadContacts:', err);
        showToast('Terjadi kesalahan saat load contacts', 'error');
    }
}

function formatDate(dt) {
    if (!dt) return '—';
    const d = new Date(dt);
    return d.toLocaleDateString('id-ID', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
}

async function deleteContact(id) {
    try {
        console.log(`📤 DELETE /api/admin/contacts/${id}`);
        const res = await apiCall(`/api/admin/contacts/${id}`, 'DELETE');
        if (res.success) {
            showToast(res.message || 'Berhasil dihapus', 'success');
            loadContacts();
        } else {
            showToast(res.message || 'Gagal dihapus', 'error');
        }
    } catch (err) {
        console.error('❌ Error in deleteContact:', err);
        showToast('Terjadi kesalahan saat hapus', 'error');
    }
}

loadContacts();
