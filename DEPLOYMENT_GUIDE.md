# 🚀 Complete Vercel Deployment Guide

This guide walks through deploying your Flask portfolio app to Vercel from scratch.

---

## 📋 Prerequisites

1. **GitHub Account** - Required for deploying via Vercel
2. **Vercel Account** - Go to https://vercel.com and sign up (free)
3. **TiDB Cluster** - Database instance with accessible host/credentials
4. **Code pushed to GitHub** - Your repo must be on GitHub

---

## Step 1: Push to GitHub

### If not already on GitHub:

```bash
# Navigate to project folder
cd path/to/TUGAS_PORTOFOLIO_REVISI

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Portfolio app ready for deployment"

# Create new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/repo-name.git
git branch -M main
git push -u origin main
```

---

## Step 2: Create Vercel Project

1. Go to https://vercel.com/dashboard
2. Click **Add New Project**
3. Select **Import Git Repository**
4. Find your GitHub repository and click **Import**
5. **Framework:** Select `Other` (since it's Flask, not a standard framework)
6. **Root Directory:** Leave blank or set to `.`
7. Click **Deploy**

⚠️ **It will fail** - this is expected. We need to set environment variables first.

---

## Step 3: Set Environment Variables

After the first failed deploy:

1. In Vercel Dashboard, go to **Settings** → **Environment Variables**
2. Add each variable below with these values:

### Critical Variables (Database Connection)

| Name | Value |
|------|-------|
| `TIDB_HOST` | your-tidb-host.tidbcloud.com |
| `TIDB_PORT` | 4000 |
| `TIDB_USER` | your-username |
| `TIDB_PASSWORD` | your-password |
| `TIDB_DB` | db_porto |

**How to find these:**
- Log in to TiDB Cloud Console
- Go to your cluster
- Click "Connect"
- Copy the connection details

### Optional Security Variables

```
FLASK_ENV=production
SECRET_KEY=your-random-secret-key
ADMIN_PASSWORD=change-from-admin123
```

**Generate a strong SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Optional: Image Upload (Cloudinary)

If you want image uploads to work:
```
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

Get from https://cloudinary.com → Settings → API

### Optional: Email (Resend)

If you want contact form emails:
```
RESEND_API_KEY=your-resend-key
RESEND_FROM_EMAIL=noreply@yourdomain.com
RESEND_TO_EMAIL=your-email@example.com
```

Get from https://resend.com

---

## Step 4: Configure TiDB Network Access

Your TiDB must be accessible from Vercel's servers.

### Option A: Allow All IPs (Easier but less secure)

1. TiDB Console → Cluster → Security Rules
2. Click **Add Rule**
3. IP Address/CIDR: `0.0.0.0/0` (allow all)
4. **Apply**

### Option B: Whitelist Vercel IPs (More secure)

Vercel IPs vary by region. For simplicity, use Option A in development.

---

## Step 5: Redeploy

1. Vercel Dashboard → Deployments
2. Click **Redeploy** on the failed deployment
3. Or push a new commit to trigger auto-deploy:
   ```bash
   git add .
   git commit -m "Add Vercel environment variables"
   git push
   ```

⏳ Wait 2-3 minutes for deployment to complete.

---

## Step 6: Test Deployment

Once deployment finishes:

### Test 1: Check Status
```
https://your-project.vercel.app/
```

Should show your portfolio home page.

### Test 2: Check Health
```
https://your-project.vercel.app/health
```

Should return:
```json
{"success": true, "status": "ok", "database": "connected"}
```

If it shows `"database": "disconnected"`:
- Check TiDB credentials in env vars
- Check if TiDB cluster is running
- Check if IP is whitelisted

### Test 3: Check API
```
https://your-project.vercel.app/api/skills
```

Should return JSON with skills data (or empty array if no data).

### Test 4: Admin Login
```
https://your-project.vercel.app/admin/login
```

Username: `admin`  
Password: `admin123` (or your custom `ADMIN_PASSWORD`)

---

## ✅ Success Indicators

✅ Portfolio page loads without "Internal Server Error"  
✅ `/health` shows `"database": "connected"`  
✅ Admin pages load after login  
✅ No red errors in browser console  

---

## ❌ Troubleshooting

### "This Serverless Function has crashed"

1. **Check Function Logs:**
   - Deployments → Latest Deployment → Function Logs
   - Look for error message
   - Copy exact error

2. **Common causes:**
   - Missing `TIDB_HOST` environment variable
   - Wrong TiDB credentials
   - TiDB cluster not running
   - IP not whitelisted

3. **Fix and redeploy:**
   ```bash
   # Fix the issue, then:
   git add .
   git commit -m "Fix deployment issue"
   git push
   ```

### "Database connection failed"

1. Check TiDB is running:
   - TiDB Cloud Console
   - Verify cluster status shows "Available"

2. Check credentials:
   - Copy exact host, user, password from TiDB
   - Paste into Vercel env vars (no extra spaces)

3. Check whitelist:
   - TiDB → Security Rules
   - Make sure IPs are whitelisted

### "Admin page doesn't load"

1. Check browser console for errors (F12)
2. Check `/health` endpoint
3. If `/health` shows "disconnected":
   - Fix database connection (see above)
   - Redeploy

---

## 📝 Custom Domain (Optional)

To use your own domain:

1. Vercel Dashboard → Project → Settings
2. Domains → Add Domain
3. Add your domain name
4. Follow DNS instructions (usually just add CNAME record)
5. Wait for DNS propagation (5-15 minutes)

---

## 🔄 Auto-Deployments

Every time you push to GitHub's `main` branch, Vercel automatically redeploys.

```bash
# Make changes locally
# Test with: python app.py

# Push to deploy
git add .
git commit -m "Update portfolio"
git push  # Vercel automatically redeploys!
```

---

## 📊 Monitoring

Check deployment status:
- Vercel Dashboard → Deployments
- Recent deployments show status
- Click deployment to see logs

---

## 🆘 Getting Help

If still having issues:

1. **Check Vercel logs:**
   ```bash
   vercel logs  # requires Vercel CLI installed
   ```

2. **Test locally first:**
   ```bash
   python app.py  # should work locally before deploying
   ```

3. **Provide to developer:**
   - Screenshot of Vercel Function Logs (error message)
   - Output of `/health` endpoint
   - TiDB credentials are correct (don't share password!)

---

## ✨ After Successful Deployment

1. **Add test data via admin:**
   - Go to `https://your-domain.com/admin/login`
   - Login and add profiles, skills, projects
   - Data appears on portfolio page

2. **Set up custom domain (optional):**
   - Vercel Settings → Domains
   - Add your domain

3. **Monitor performance:**
   - Vercel Analytics
   - Check Function Logs for errors

4. **Keep code updated:**
   - Use GitHub for version control
   - Each push auto-deploys

---

## 🎯 Quick Reference

| Task | Command/Link |
|------|------|
| Deploy new code | `git push origin main` |
| View logs | Dashboard → Deployments → Function Logs |
| Test health | `curl https://your-domain/health` |
| Admin login | `https://your-domain/admin/login` |
| Test API | Browser console: `fetch('/api/skills').then(r=>r.json()).then(d=>console.log(d))` |
| Redeploy | Dashboard → Redeploy button |
| View analytics | Dashboard → Analytics |

---

**🎉 Done! Your portfolio is now live on Vercel!**

For further questions, see `VERCEL_ENV_SETUP.md` or `DEBUGGING_GUIDE.md`.
