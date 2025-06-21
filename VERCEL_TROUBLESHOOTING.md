# Vercel Deployment Troubleshooting

## 🚨 Common Issues & Solutions

### **1. "Missing variable `handler` or `app` in file wsgi.py"**

**Solution**: ✅ Fixed
- Added `app = application` in `wsgi.py`
- Vercel requires the `app` variable to be defined

### **2. "No directory at: /var/task/staticfiles/"**

**Solution**: ✅ Fixed
- Updated `build_files.sh` to create staticfiles directory
- Changed static file storage to `CompressedStaticFilesStorage`
- Added proper static file collection

### **3. FUNCTION_INVOCATION_FAILED**

**Causes & Solutions**:

#### **A. Missing Dependencies**
```bash
# Install locally to test
pip install -r requirements_vercel.txt
```

#### **B. Database Connection Issues**
- Check Neon database connectivity
- Verify `DATABASE_URL` environment variable
- Test with SQLite fallback

#### **C. Static Files Issues**
- Ensure `staticfiles` directory exists
- Check `STATIC_ROOT` configuration
- Verify WhiteNoise middleware

## 🔧 Debugging Steps

### **1. Check Build Logs**
```bash
vercel logs
```

### **2. Test Locally with Production Settings**
```bash
# Set environment variables
set DJANGO_SETTINGS_MODULE=OCRtesrect.settings_production
set DATABASE_URL=your_neon_url
set DEBUG=False

# Run server
python manage.py runserver --settings=OCRtesrect.settings_production
```

### **3. Verify Static Files**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check if staticfiles directory exists
dir staticfiles
```

### **4. Test Database Connection**
```bash
python manage.py migrate --settings=OCRtesrect.settings_production
```

## 📁 File Structure Check

Ensure your project has this structure:
```
OCRtesrect/
├── wsgi.py                    # ✅ Entry point
├── manage.py                  # ✅ Django management
├── vercel.json               # ✅ Vercel config
├── requirements_vercel.txt    # ✅ Dependencies
├── build_files.sh            # ✅ Build script
├── static/                   # ✅ Static files
│   ├── css/
│   └── index.html
└── OCRtesrect/               # ✅ Django project
    ├── settings_production.py
    └── ocrapp/
```

## 🚀 Deployment Checklist

### **Before Deploying**:
- [ ] All dependencies in `requirements_vercel.txt`
- [ ] `wsgi.py` has `app = application`
- [ ] `build_files.sh` creates staticfiles directory
- [ ] Static files exist in `static/` directory
- [ ] Database URL is correct
- [ ] Environment variables set in `vercel.json`

### **After Deploying**:
- [ ] Check build logs: `vercel logs`
- [ ] Test health endpoint: `/health/`
- [ ] Test static files: `/static/css/style.css`
- [ ] Test OCR functionality: Upload an image

## 🔍 Environment Variables

**Required in vercel.json**:
```json
{
  "env": {
    "DJANGO_SETTINGS_MODULE": "OCRtesrect.settings_production",
    "DATABASE_URL": "your_neon_url",
    "SECRET_KEY": "your_secret_key",
    "OCR_SPACE_API_KEY": "helloworld",
    "DEBUG": "False"
  }
}
```

## 🛠️ Quick Fixes

### **If Static Files Don't Work**:
1. Check `STATICFILES_STORAGE` in settings
2. Ensure `staticfiles` directory exists
3. Verify WhiteNoise middleware is first

### **If Database Connection Fails**:
1. Test Neon database connectivity
2. Check `DATABASE_URL` format
3. Verify SSL mode is set correctly

### **If OCR Doesn't Work**:
1. Check OCR.Space API key
2. Verify image upload size limits
3. Test with simple text image

## 📞 Support

If issues persist:
1. Check Vercel function logs
2. Test locally with production settings
3. Verify all environment variables
4. Check Neon database status 