let currentProjectId = null;

document.getElementById('projectForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        title: document.getElementById('prTitle').value.trim(),
        description: document.getElementById('prDescription').value.trim() || null,
        tech_stack: document.getElementById('prTechStack').value.trim() || null,
        image_url: document.getElementById('prImageUrl').value.trim() || null,
        demo_url: document.getElementById('prDemoUrl').value.trim() || null,
        repo_url: document.getElementById('prRepoUrl').value.trim() || null,
        is_featured: document.getElementById('prIsFeatured').checked ? 1 : 0
    };

    if (!body.title) {
        alert('Judul proyek harus diisi!');
        return;
    }

    try {
        const url = currentProjectId ? `/api/admin/projects/${currentProjectId}` : '/api/admin/projects';
        const method = currentProjectId ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            document.getElementById('projectForm').reset();
            currentProjectId = null;
            loadProjects();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

async function loadProjects() {
    try {
        const res = await fetch('/api/admin/projects');
        const data = await res.json();
        const list = document.getElementById('projectsList');
        
        if (!data.data || data.data.length === 0) {
            list.innerHTML = '<p style="color:#999;">Tidak ada data proyek</p>';
            return;
        }
        
        list.innerHTML = data.data.map(p => {
            const techs = (p.tech_stack || '').split(',').map(t => t.trim()).filter(Boolean);
            return `
            <div class="project-card">
                <div class="card-header">
                    <div style="flex:1;">
                        <div class="card-title">${p.title}</div>
                        ${p.is_featured ? '<span class="badge featured">⭐ Featured</span>' : ''}
                    </div>
                    <div style="display:flex;gap:8px;">
                        <button class="btn-edit" onclick="editProject(${p.id})">Edit</button>
                        <button class="btn-danger" onclick="deleteProject(${p.id})">Hapus</button>
                    </div>
                </div>
                ${p.description ? `<div class="card-description">${p.description}</div>` : ''}
                ${techs.length ? `<div class="card-meta">Tech: ${techs.join(', ')}</div>` : ''}
                <div class="card-actions">
                    ${p.demo_url ? `<a href="${p.demo_url}" target="_blank" class="btn-edit" style="text-decoration:none;">Demo</a>` : ''}
                    ${p.repo_url ? `<a href="${p.repo_url}" target="_blank" class="btn-edit" style="text-decoration:none;">Repo</a>` : ''}
                </div>
            </div>
            `;
        }).join('');
    } catch (e) {
        console.error('Error loading projects:', e);
    }
}

async function editProject(id) {
    try {
        const res = await fetch('/api/admin/projects');
        const data = await res.json();
        const project = data.data.find(p => p.id === id);
        
        if (project) {
            currentProjectId = id;
            document.getElementById('prId').value = project.id;
            document.getElementById('prTitle').value = project.title || '';
            document.getElementById('prDescription').value = project.description || '';
            document.getElementById('prTechStack').value = project.tech_stack || '';
            document.getElementById('prImageUrl').value = project.image_url || '';
            document.getElementById('prDemoUrl').value = project.demo_url || '';
            document.getElementById('prRepoUrl').value = project.repo_url || '';
            document.getElementById('prIsFeatured').checked = project.is_featured;
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

async function deleteProject(id) {
    if (!confirm('Yakin ingin menghapus proyek ini?')) return;
    
    try {
        const res = await fetch(`/api/admin/projects/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            loadProjects();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

loadProjects();
