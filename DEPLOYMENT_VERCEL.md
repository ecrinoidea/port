# 🚀 PANDUAN DEPLOYMENT KE VERCEL

## Persiapan

1. **Push repository ke GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Verifikasi file penting sudah ada:**
   - ✅ `vercel.json` - Konfigurasi Vercel
   - ✅ `index.py` - Entry point WSGI
   - ✅ `requirements.txt` - Dependencies Python
   - ✅ `.env.example` - Template environment variables

## Langkah Deployment di Vercel

### 1. Login ke Vercel
- Buka https://vercel.com
- Login dengan akun GitHub
- Klik "New Project"

### 2. Import Repository
- Pilih repository Anda dari GitHub
- Klik "Import"

### 3. Konfigurasi Environment Variables
Di halaman "Environment Variables", tambahkan semua variabel dari `.env.example`:

**Database (TiDB):**
```
TIDB_HOST=your_tidb_host.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=your_tidb_user
TIDB_PASSWORD=your_tidb_password
TIDB_DB=db_porto
TIDB_SSL_CA=/etc/ssl/certs/ca-certificates.crt
```

**Secret:**
```
SECRET_KEY=your_very_secure_secret_key_here_change_me
FLASK_ENV=production
```

**Cloudinary (Opsional):**
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**Resend (Opsional untuk email):**
```
RESEND_API_KEY=your_resend_api_key
RESEND_FROM_EMAIL=noreply@example.com
RESEND_TO_EMAIL=your_email@example.com
```

**Admin:**
```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_admin_password
```

### 4. Deploy
- Klik "Deploy"
- Tunggu proses deployment selesai
- Cek URL aplikasi Anda

## Troubleshooting

### ❌ "Internal Server Error"
**Penyebab:** Database tidak terhubung atau variabel environment tidak lengkap

**Solusi:**
1. Cek apakah semua environment variables sudah diset di Vercel
2. Pastikan TiDB host dapat diakses dari Vercel
3. Lihat logs di Vercel Dashboard → Deployments → Function logs

### ❌ Static Files Tidak Muncul
**Penyebab:** Path static files tidak benar

**Solusi:**
- Sudah diperbaiki di `app.py` dengan `BASE_DIR` yang benar
- Pastikan folder `Frontend` ada dengan structure yang benar

### ❌ 502 Bad Gateway
**Penyebab:** Aplikasi crash saat startup

**Solusi:**
1. Cek error logs di Vercel
2. Pastikan `index.py` bisa dijalankan locally
3. Verifikasi semua imports bekerja

## Test Lokal Sebelum Deploy

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment variables
cp .env.example .env.local
# Edit .env.local dengan kredensial lokal

# 3. Run aplikasi
python app.py

# 4. Buka http://localhost:5000
```

## Monitoring Setelah Deploy

1. **Vercel Dashboard**
   - Check "Overview" untuk uptime
   - Check "Function logs" untuk errors
   - Check "Analytics" untuk traffic

2. **Real-time Logs**
   ```bash
   vercel logs <app-url>
   ```

## Debugging

Untuk melihat logs secara real-time:

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# View logs
vercel logs <your-app-name> --tail
```

## Notes Penting

⚠️ **Serverless Limitations:**
- Max 30 second execution time
- No persistent file storage (gunakan Cloudinary untuk images)
- Connection pooling mungkin diperlukan untuk database

✅ **Best Practices:**
- Jangan commit `.env.local`
- Selalu gunakan environment variables untuk secrets
- Test di environment production-like sebelum deploy
- Monitor logs secara regular

---
**Questions?** Cek Vercel docs: https://vercel.com/docs/concepts/functions/serverless-functions/python
