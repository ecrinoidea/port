let currentSkillId = null;

document.getElementById('skillForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        name: document.getElementById('sName').value.trim(),
        category: document.getElementById('sCategory').value || null,
        level: parseInt(document.getElementById('sLevel').value) || 80,
        icon: document.getElementById('sIcon').value.trim() || null
    };

    if (!body.name) {
        alert('Nama skill harus diisi!');
        return;
    }

    try {
        const url = currentSkillId ? `/api/admin/skills/${currentSkillId}` : '/api/admin/skills';
        const method = currentSkillId ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            document.getElementById('skillForm').reset();
            currentSkillId = null;
            loadSkills();
        } else {
            alert('Error: ' + (data.message || JSON.stringify(data)));
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

async function loadSkills() {
    try {
        const res = await fetch('/api/admin/skills');
        const data = await res.json();
        const tbody = document.getElementById('skillsList');
        
        if (!data.data || data.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#999;">Tidak ada data skill</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.data.map(s => `
            <tr>
                <td>${s.name}</td>
                <td>${s.category || '-'}</td>
                <td>${s.level}%</td>
                <td>${s.icon || '-'}</td>
                <td>
                    <button class="btn-edit" onclick="editSkill(${s.id})">Edit</button>
                    <button class="btn-danger" onclick="deleteSkill(${s.id})">Hapus</button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        console.error('Error loading skills:', e);
        alert('Error loading skills: ' + e.message);
    }
}

async function editSkill(id) {
    try {
        const res = await fetch('/api/admin/skills');
        const data = await res.json();
        const skill = data.data.find(s => s.id === id);
        
        if (skill) {
            currentSkillId = id;
            document.getElementById('sId').value = skill.id;
            document.getElementById('sName').value = skill.name || '';
            document.getElementById('sCategory').value = skill.category || '';
            document.getElementById('sLevel').value = skill.level || 80;
            document.getElementById('sIcon').value = skill.icon || '';
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

async function deleteSkill(id) {
    if (!confirm('Yakin ingin menghapus skill ini?')) return;
    
    try {
        const res = await fetch(`/api/admin/skills/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            loadSkills();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

loadSkills();
