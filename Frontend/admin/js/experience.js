let currentExperienceId = null;

document.getElementById('experienceForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        company: document.getElementById('eCompany').value.trim(),
        position: document.getElementById('ePosition').value.trim(),
        start_date: document.getElementById('eStartDate').value.trim() || null,
        end_date: document.getElementById('eEndDate').value.trim() || null,
        is_current: document.getElementById('eIsCurrent').checked ? 1 : 0,
        description: document.getElementById('eDescription').value.trim() || null,
        logo_url: document.getElementById('eLogoUrl').value.trim() || null
    };

    if (!body.company || !body.position) {
        alert('Perusahaan dan posisi harus diisi!');
        return;
    }

    try {
        const url = currentExperienceId ? `/api/admin/experiences/${currentExperienceId}` : '/api/admin/experiences';
        const method = currentExperienceId ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            document.getElementById('experienceForm').reset();
            currentExperienceId = null;
            loadExperiences();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

async function loadExperiences() {
    try {
        const res = await fetch('/api/admin/experiences');
        const data = await res.json();
        const list = document.getElementById('experienceList');
        
        if (!data.data || data.data.length === 0) {
            list.innerHTML = '<p style="color:#999;">Tidak ada data pengalaman</p>';
            return;
        }
        
        list.innerHTML = data.data.map(e => `
            <div class="experience-card">
                <div class="card-header">
                    <div>
                        <div class="card-title">${e.position}</div>
                        <div class="card-subtitle">${e.company}</div>
                    </div>
                    <div style="display:flex;gap:8px;">
                        ${e.is_current ? '<span class="badge current">Aktif</span>' : ''}
                        <button class="btn-edit" onclick="editExperience(${e.id})">Edit</button>
                        <button class="btn-danger" onclick="deleteExperience(${e.id})">Hapus</button>
                    </div>
                </div>
                <div class="card-meta">
                    <span>📅 ${e.start_date || 'N/A'} - ${e.is_current ? 'Sekarang' : (e.end_date || 'N/A')}</span>
                </div>
                ${e.description ? `<div class="card-description">${e.description}</div>` : ''}
            </div>
        `).join('');
    } catch (e) {
        console.error('Error loading experiences:', e);
    }
}

async function editExperience(id) {
    try {
        const res = await fetch('/api/admin/experiences');
        const data = await res.json();
        const exp = data.data.find(e => e.id === id);
        
        if (exp) {
            currentExperienceId = id;
            document.getElementById('eId').value = exp.id;
            document.getElementById('eCompany').value = exp.company || '';
            document.getElementById('ePosition').value = exp.position || '';
            document.getElementById('eStartDate').value = exp.start_date || '';
            document.getElementById('eEndDate').value = exp.end_date || '';
            document.getElementById('eIsCurrent').checked = exp.is_current;
            document.getElementById('eDescription').value = exp.description || '';
            document.getElementById('eLogoUrl').value = exp.logo_url || '';
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

async function deleteExperience(id) {
    if (!confirm('Yakin ingin menghapus pengalaman ini?')) return;
    
    try {
        const res = await fetch(`/api/admin/experiences/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            loadExperiences();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

loadExperiences();
