# Vercel Deployment Guide

## Project Structure
```
OCRtesrect/
├── manage.py                    # Root Django management
├── wsgi.py                      # Root WSGI for Vercel
├── vercel.json                  # Vercel configuration
├── requirements.txt             # Python dependencies
├── build_files.sh              # Build script
├── static/                      # Static files directory
└── OCRtesrect/                 # Django project directory
    ├── settings_production.py   # Production settings
    ├── ocrapp/                  # OCR application
    └── ...
```

## Deployment Steps

### 1. Vercel CLI Setup
```bash
npm i -g vercel
vercel login
```

### 2. Deploy to Vercel
```bash
vercel
```

### 3. Build Settings (if asked)
- **Framework Preset**: Other
- **Root Directory**: `./` (current directory)
- **Build Command**: `bash build_files.sh`
- **Output Directory**: Leave empty
- **Install Command**: Leave empty

### 4. Environment Variables
These are already configured in `vercel.json`:
- `DJANGO_SETTINGS_MODULE`: `OCRtesrect.settings_production`
- `DATABASE_URL`: Your Neon PostgreSQL URL
- `SECRET_KEY`: Django secret key

## Troubleshooting

### 404 Error
If you get a 404 error:

1. **Check the deployment logs**:
   ```bash
   vercel logs
   ```

2. **Verify the build**:
   - Check if `build_files.sh` executed successfully
   - Ensure migrations ran properly
   - Verify static files were collected

3. **Test locally with production settings**:
   ```bash
   python manage.py runserver --settings=OCRtesrect.settings_production
   ```

### Common Issues

1. **Database Connection**: Ensure Neon database is accessible
2. **Static Files**: Check if static files are being served
3. **Dependencies**: Verify all packages are in `requirements.txt`

## Local Development vs Production

### Local Development
```bash
cd OCRtesrect
python ../manage.py runserver
```

### Production (Vercel)
- Uses `wsgi.py` as entry point
- Uses `OCRtesrect.settings_production`
- Uses Neon PostgreSQL database
- Processes images in memory (no local storage)

## Health Check
After deployment, test the health endpoint:
```
https://your-app.vercel.app/health/
```

Should return:
```json
{
  "status": "healthy",
  "message": "OCR API is running"
}
``` 