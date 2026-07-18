let currentProfileId = null;

document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        name: document.getElementById('pName').value.trim(),
        title: document.getElementById('pTitle').value.trim(),
        bio: document.getElementById('pBio').value.trim(),
        email: document.getElementById('pEmail').value.trim(),
        phone: document.getElementById('pPhone').value.trim(),
        location: document.getElementById('pLocation').value.trim(),
        github: document.getElementById('pGithub').value.trim(),
        linkedin: document.getElementById('pLinkedin').value.trim(),
        instagram: document.getElementById('pInstagram').value.trim(),
        photo_url: document.getElementById('pPhoto').value.trim()
    };

    if (!body.name) {
        alert('Nama harus diisi!');
        return;
    }

    try {
        const url = currentProfileId ? `/api/admin/profiles/${currentProfileId}` : '/api/admin/profiles';
        const method = currentProfileId ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            document.getElementById('profileForm').reset();
            currentProfileId = null;
            loadProfiles();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

async function loadProfiles() {
    try {
        const res = await fetch('/api/admin/profiles');
        const data = await res.json();
        const list = document.getElementById('profilesList');
        
        if (!data.data || data.data.length === 0) {
            list.innerHTML = '<p style="color:#999;">Tidak ada data profil</p>';
            return;
        }
        
        list.innerHTML = data.data.map(p => `
            <div class="profile-card">
                <div class="card-header">
                    <div>
                        <div class="card-title">${p.name}</div>
                        <div class="card-subtitle">${p.title || 'N/A'}</div>
                    </div>
                    <div>
                        <button class="btn-edit" onclick="editProfile(${p.id})">Edit</button>
                        <button class="btn-danger" onclick="deleteProfile(${p.id})">Hapus</button>
                    </div>
                </div>
                <div class="card-description">${p.bio || 'Tidak ada deskripsi'}</div>
                <div class="card-meta">
                    ${p.email ? `<span>📧 ${p.email}</span>` : ''}
                    ${p.phone ? `<span>📱 ${p.phone}</span>` : ''}
                    ${p.location ? `<span>📍 ${p.location}</span>` : ''}
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error('Error loading profiles:', e);
    }
}

async function editProfile(id) {
    try {
        const res = await fetch('/api/admin/profiles');
        const data = await res.json();
        const profile = data.data.find(p => p.id === id);
        
        if (profile) {
            currentProfileId = id;
            document.getElementById('pName').value = profile.name || '';
            document.getElementById('pTitle').value = profile.title || '';
            document.getElementById('pBio').value = profile.bio || '';
            document.getElementById('pEmail').value = profile.email || '';
            document.getElementById('pPhone').value = profile.phone || '';
            document.getElementById('pLocation').value = profile.location || '';
            document.getElementById('pGithub').value = profile.github || '';
            document.getElementById('pLinkedin').value = profile.linkedin || '';
            document.getElementById('pInstagram').value = profile.instagram || '';
            document.getElementById('pPhoto').value = profile.photo_url || '';
            document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

async function deleteProfile(id) {
    if (!confirm('Yakin ingin menghapus profil ini?')) return;
    
    try {
        const res = await fetch(`/api/admin/profiles/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            loadProfiles();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

loadProfiles();
