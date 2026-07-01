// Navbar scroll effect
window.addEventListener('scroll', () => {
    const nb = document.getElementById('navbar');
    if (nb) nb.classList.toggle('scrolled', window.scrollY > 40);
});

// Scroll fade-in
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });

// Load profile
async function loadProfile() {
    try {
        const res = await fetch('/api/profile');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log('📥 Profile data:', data);
        const p = data.data;
        if (!p) {
            console.warn('⚠️  No profile data received');
            return;
        }

        document.getElementById('heroName').textContent = p.name || 'Nama Saya';
        document.getElementById('heroTitle').textContent = p.title || '';
        document.getElementById('heroBio').textContent = p.bio || '';
        document.title = `${p.name || 'Portofolio'} — Portfolio`;

        // Socials
        const socials = document.getElementById('heroSocials');
        if (p.github) socials.innerHTML += `<a href="${p.github}" class="social-link" target="_blank">⟨/⟩ GitHub</a>`;
        if (p.linkedin) socials.innerHTML += `<a href="${p.linkedin}" class="social-link" target="_blank">in LinkedIn</a>`;
        if (p.instagram) socials.innerHTML += `<a href="${p.instagram}" class="social-link" target="_blank">📷 Instagram</a>`;
        if (p.email) socials.innerHTML += `<a href="mailto:${p.email}" class="social-link">✉ Email</a>`;

        // About
        const aboutContent = [
            p.email    ? `<div class="about-item"><div class="about-item-label">Email</div><div class="about-item-value"><a href="mailto:${p.email}">${p.email}</a></div></div>` : '',
            p.phone    ? `<div class="about-item"><div class="about-item-label">Telepon</div><div class="about-item-value">${p.phone}</div></div>` : '',
            p.location ? `<div class="about-item"><div class="about-item-label">Lokasi</div><div class="about-item-value">${p.location}</div></div>` : '',
            p.github   ? `<div class="about-item"><div class="about-item-label">GitHub</div><div class="about-item-value"><a href="${p.github}" target="_blank">${p.github.replace('https://','')}</a></div></div>` : '',
            p.linkedin ? `<div class="about-item"><div class="about-item-label">LinkedIn</div><div class="about-item-value"><a href="${p.linkedin}" target="_blank">Lihat Profil</a></div></div>` : '',
            p.instagram ? `<div class="about-item"><div class="about-item-label">Instagram</div><div class="about-item-value"><a href="${p.instagram}" target="_blank">${p.instagram.replace('https://','')}</a></div></div>` : '',
        ].filter(Boolean).join('');
        
        let htmlAbout = '';
        if (p.photo_url) {
            htmlAbout += `<div class="about-photo-wrapper"><img src="${p.photo_url}" alt="${p.name}" class="about-photo"></div>`;
            htmlAbout += `<div class="about-info">${aboutContent || '<p style="color:#a09ab8;">Belum ada data profil.</p>'}</div>`;
        } else {
            htmlAbout = `<div class="about-info-full">${aboutContent || '<p style="color:#a09ab8;">Belum ada data profil.</p>'}</div>`;
        }
        
        document.getElementById('aboutInfo').innerHTML = htmlAbout;
        console.log('✅ Profile loaded successfully');
    } catch (e) {
        console.error('❌ Error loading profile:', e);
    }
}

// Load skills
async function loadSkills() {
    try {
        const res = await fetch('/api/skills');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log('📥 Skills data:', data);
        const skills = data.data || [];
        const grid = document.getElementById('skillsGrid');
        if (!skills.length) {
            console.warn('⚠️  No skills data');
            grid.innerHTML = '<p style="color:#a09ab8;">Belum ada data skill.</p>';
            return;
        }
        grid.innerHTML = skills.map(s => `
            <div class="skill-card fade-in">
                <div class="skill-header">
                    <span class="skill-name">${s.name}</span>
                    <span class="skill-level">${s.level}%</span>
                </div>
                <div class="skill-cat">${s.category || ''}</div>
                <div class="progress">
                    <div class="progress-bar" style="width:0%" data-width="${s.level}%"></div>
                </div>
            </div>
        `).join('');
        // Animate bars on scroll
        grid.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
        // Trigger bar animation
        setTimeout(() => {
            document.querySelectorAll('.progress-bar[data-width]').forEach(bar => {
                bar.style.width = bar.dataset.width;
            });
        }, 400);
        console.log('✅ Skills loaded successfully');
    } catch (e) {
        console.error('❌ Error loading skills:', e);
    }
}

// Load experiences
async function loadExperiences() {
    try {
        const res = await fetch('/api/experiences');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log('📥 Experiences data:', data);
        const exps = data.data || [];
        const tl = document.getElementById('timeline');
        if (!exps.length) {
            console.warn('⚠️  No experiences data');
            tl.innerHTML = '<p style="color:#a09ab8;">Belum ada data pengalaman.</p>';
            return;
        }
        tl.innerHTML = exps.map(e => `
            <div class="timeline-item fade-in">
                <div class="timeline-dot"></div>
                <div class="timeline-card">
                    <div class="exp-header">
                        <div>
                            <div class="exp-position">${e.position}</div>
                            <div class="exp-company">${e.company}</div>
                        </div>
                        <div style="display:flex; flex-direction:column; align-items:flex-end; gap:5px;">
                            <span class="exp-period">${e.start_date || ''} – ${e.is_current ? 'Sekarang' : (e.end_date || '')}</span>
                            ${e.is_current ? '<span class="exp-badge">✓ Aktif</span>' : ''}
                        </div>
                    </div>
                    ${e.description ? `<p class="exp-desc">${e.description}</p>` : ''}
                </div>
            </div>
        `).join('');
        tl.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
        console.log('✅ Experiences loaded successfully');
    } catch (e) {
        console.error('❌ Error loading experiences:', e);
    }
}

// Load projects
async function loadProjects() {
    try {
        const res = await fetch('/api/projects');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log('📥 Projects data:', data);
        const projects = data.data || [];
        const grid = document.getElementById('projectsGrid');
        if (!projects.length) {
            console.warn('⚠️  No projects data');
            grid.innerHTML = '<p style="color:#a09ab8;">Belum ada data proyek.</p>';
            return;
        }
        grid.innerHTML = projects.map(p => {
            const techs = (p.tech_stack || '').split(',').map(t => t.trim()).filter(Boolean);
            return `
            <div class="proj-card fade-in">
                <div class="proj-img">
                    ${p.image_url ? `<img src="${p.image_url}" alt="${p.title}" onerror="this.parentElement.innerHTML='📁'">` : '📁'}
                </div>
                <div class="proj-body">
                    ${p.is_featured ? '<span class="proj-featured">⭐ Featured</span>' : ''}
                    <div class="proj-title">${p.title}</div>
                    <p class="proj-desc">${p.description || ''}</p>
                    ${techs.length ? `<div class="proj-tech">${techs.map(t => `<span class="tech-tag">${t}</span>`).join('')}</div>` : ''}
                    <div class="proj-links">
                        ${p.demo_url ? `<a href="${p.demo_url}" target="_blank" class="proj-link proj-link-demo">↗ Demo</a>` : ''}
                        ${p.repo_url ? `<a href="${p.repo_url}" target="_blank" class="proj-link proj-link-repo">⟨/⟩ Repo</a>` : ''}
                    </div>
                </div>
            </div>
        `}).join('');
        grid.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
        console.log('✅ Projects loaded successfully');
    } catch (e) {
        console.error('❌ Error loading projects:', e);
    }
}

// Send contact
async function sendContact() {
    const btn = document.getElementById('sendBtn');
    const msgEl = document.getElementById('formMsg');
    const body = {
        name: document.getElementById('cName').value.trim(),
        email: document.getElementById('cEmail').value.trim(),
        subject: document.getElementById('cSubject').value.trim(),
        message: document.getElementById('cMessage').value.trim()
    };
    if (!body.name || !body.email || !body.message) {
        showMsg('Nama, email, dan pesan wajib diisi.', 'error');
        return;
    }
    btn.disabled = true;
    btn.textContent = 'Mengirim...';
    try {
        const res = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log('📥 Contact response:', data);
        if (data.success) {
            showMsg('Pesan berhasil dikirim! Terima kasih ☺', 'success');
            ['cName','cEmail','cSubject','cMessage'].forEach(id => document.getElementById(id).value = '');
            console.log('✅ Contact message sent successfully');
        } else {
            showMsg(data.message || 'Gagal mengirim pesan.', 'error');
        }
    } catch (e) {
        console.error('❌ Error sending contact:', e);
        showMsg('Terjadi kesalahan. Coba lagi.', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Kirim Pesan →';
    }
}

function showMsg(text, type) {
    const el = document.getElementById('formMsg');
    el.textContent = text;
    el.className = `form-msg ${type}`;
    el.style.display = 'block';
    if (type === 'success') setTimeout(() => { el.style.display = 'none'; }, 5000);
}

// Init
console.log('🚀 Initializing portfolio...');
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
loadProfile();
loadSkills();
loadExperiences();
loadProjects();
console.log('✅ Portfolio initialization complete');
