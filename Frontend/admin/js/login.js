async function doLogin() {
    const btn = document.getElementById('loginBtn');
    const errEl = document.getElementById('login-error');
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    if (!username || !password) {
        showError('Username dan password wajib diisi.');
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Memproses...';
    errEl.style.display = 'none';

    try {
        const res = await fetch('/admin/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = '/admin/dashboard';
        } else {
            showError(data.message || 'Login gagal.');
        }
    } catch (e) {
        showError('Terjadi kesalahan. Coba lagi.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Masuk';
    }
}

function showError(msg) {
    const el = document.getElementById('login-error');
    el.textContent = msg;
    el.style.display = 'block';
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') doLogin();
});
