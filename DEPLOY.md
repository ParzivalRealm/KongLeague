# 🚀 Deployment Guide - KongLeague

This guide covers deploying KongLeague to Railway.app and Render.com free tiers.

## Prerequisites

- Git repository with your code
- GitHub/GitLab account
- Railway or Render account (free tier available)

---

## Option 1: Railway.app (Recommended)

Railway offers a simple deployment process with generous free tier.

### Step 1: Prepare Your Project

1. **Ensure all files are committed to Git**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Verify these files exist:**
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `railway.json`

### Step 2: Deploy to Railway

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your KongLeague repository

3. **Configure Environment Variables**

   In Railway dashboard → Variables, add:

   ```
   SECRET_KEY=<generate-a-strong-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   ```

   **Generate a SECRET_KEY:**
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Deploy**
   - Railway will automatically detect Django
   - Build process will run migrations and collect static files
   - Wait for deployment to complete

5. **Setup Admin User**

   In Railway dashboard → your project → Terminal:
   ```bash
   python manage.py createsuperuser
   ```

6. **Load Demo Data (Optional)**
   ```bash
   python manage.py setup_demo_data
   ```

7. **Get Your URL**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Visit it to see your tournament site!

### Railway Tips

- Free tier includes 500 hours/month (enough for always-on small apps)
- Automatic deploys on git push
- Built-in PostgreSQL available (just add from dashboard)
- Easy to view logs and monitor app

---

## Option 2: Render.com

Render is another excellent free hosting option.

### Step 1: Prepare Your Project

Same as Railway - ensure all files are committed.

### Step 2: Deploy to Render

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the KongLeague repo

3. **Configure Service**

   **Basic Settings:**
   - Name: `kongleague` (or your choice)
   - Environment: `Python 3`
   - Region: Choose closest to your audience
   - Branch: `main`

   **Build Command:**
   ```bash
   ./build.sh
   ```

   **Start Command:**
   ```bash
   gunicorn kongleague.wsgi:application
   ```

4. **Environment Variables**

   Click "Advanced" → Add environment variables:

   ```
   SECRET_KEY=<generate-a-strong-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=*.onrender.com
   PYTHON_VERSION=3.12.0
   ```

5. **Create Service**
   - Click "Create Web Service"
   - Wait for build and deploy (5-10 minutes)

6. **Setup Admin**

   In Render dashboard → Shell:
   ```bash
   python manage.py createsuperuser
   ```

7. **Load Demo Data (Optional)**
   ```bash
   python manage.py setup_demo_data
   ```

8. **Access Your Site**
   - Render provides URL like: `https://kongleague.onrender.com`

### Render Tips

- Free tier spins down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds (cold start)
- Great for demos and low-traffic sites
- Easy to upgrade to paid tier if needed

---

## Post-Deployment Checklist

✅ **Site loads correctly**
- Visit your deployment URL
- Check that CSS is loading (Tailwind styles)
- Navigate between pages

✅ **Admin access works**
- Go to `/admin-login/`
- Login with your admin credentials
- Create a test team

✅ **Database persists**
- Add some data
- Restart the service
- Verify data is still there

✅ **Static files work**
- Check that Tailwind CSS is applied
- Verify page styling looks correct

---

## Using PostgreSQL (Production Database)

### Railway PostgreSQL

1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will provide a `DATABASE_URL`
4. Add to your environment variables:
   ```
   DATABASE_URL=postgresql://...
   ```

5. Update `settings.py` to use PostgreSQL in production:
   ```python
   import dj_database_url

   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   ```

6. Add to `requirements.txt`:
   ```
   dj-database-url>=2.1.0
   ```

### Render PostgreSQL

1. Create "New" → "PostgreSQL"
2. Copy the "Internal Database URL"
3. Add as `DATABASE_URL` environment variable
4. Follow same `settings.py` changes as above

---

## Troubleshooting

### Static Files Not Loading

**Check:**
1. `STATIC_ROOT` is set in settings.py
2. `python manage.py collectstatic` ran during build
3. Whitenoise is in MIDDLEWARE

**Fix:**
```bash
python manage.py collectstatic --no-input
```

### 500 Server Error

**Check logs:**
- Railway: Dashboard → Deployments → View Logs
- Render: Dashboard → Logs

**Common causes:**
- Missing environment variables
- Database migration issues
- Incorrect `ALLOWED_HOSTS`

### Database Issues

**Reset database (warning: deletes all data):**
```bash
python manage.py flush
python manage.py migrate
python manage.py setup_demo_data
```

### Permissions Error

Make sure `build.sh` is executable:
```bash
chmod +x build.sh
git add build.sh
git commit -m "Make build script executable"
git push
```

---

## Custom Domain Setup

### Railway

1. Go to your service → Settings
2. Click "Generate Domain" for free `.railway.app` subdomain
3. For custom domain:
   - Add your domain in settings
   - Update DNS records as shown
   - Update `ALLOWED_HOSTS` to include your domain

### Render

1. Go to your service → Settings → Custom Domain
2. Add your domain
3. Follow DNS configuration instructions
4. Update `ALLOWED_HOSTS`

---

## Monitoring and Maintenance

### View Logs

**Railway:**
```
Dashboard → Deployments → View Logs
```

**Render:**
```
Dashboard → Logs
```

### Run Commands

Both platforms provide shell access to run management commands:

```bash
python manage.py migrate           # Run migrations
python manage.py createsuperuser   # Create admin
python manage.py setup_demo_data   # Load sample data
```

### Automatic Deployments

Both Railway and Render support automatic deployments:
- Push to `main` branch
- Service automatically rebuilds and redeploys
- Zero downtime deployments

---

## Cost Considerations

### Railway Free Tier
- $5 free credit per month
- ~500 hours of usage
- Good for always-on hobby projects

### Render Free Tier
- Completely free
- Sleeps after 15 min inactivity
- 750 hours/month limit
- Great for demos and low-traffic sites

**Recommendation:** Start with free tier, upgrade if traffic grows.

---

## Security Best Practices

✅ **Never commit sensitive data**
- Use environment variables for secrets
- Keep `.env` in `.gitignore`

✅ **Use strong SECRET_KEY**
- Generate new one for production
- Never use the default from settings.py

✅ **Set DEBUG=False in production**
- Prevents error details from leaking

✅ **Configure ALLOWED_HOSTS properly**
- Only include your actual domain(s)

✅ **Regular updates**
```bash
pip install --upgrade django
pip freeze > requirements.txt
```

---

## Need Help?

- **Django Docs**: https://docs.djangoproject.com
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs

---

🦍 **Good luck with your deployment!** 🍌

**Muestra Tu Fuerza!**
