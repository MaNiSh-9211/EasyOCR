# OCR Text Recognition App

A Django-based OCR (Optical Character Recognition) application that extracts text from uploaded images using EasyOCR.

## Features

- Upload images for text extraction
- Real-time OCR processing using EasyOCR
- Production-ready configuration for Vercel
- PostgreSQL database support (Neon)
- Secure file upload handling
- Health check endpoint

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL (Neon)
- **OCR Engine**: EasyOCR
- **Deployment**: Vercel
- **Static Files**: WhiteNoise

## Production Deployment

### Prerequisites

1. **Neon Database**: Already configured with your credentials
2. **Vercel Account**: For deployment
3. **Git Repository**: For version control

### Deployment Steps

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```

4. **Set Environment Variables** (if needed):
   - `SECRET_KEY`: Your Django secret key
   - `DATABASE_URL`: Your Neon database URL (already configured)

### Environment Variables

The following environment variables are already configured in `vercel.json`:

- `DJANGO_SETTINGS_MODULE`: `OCRtesrect.settings_production`
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `SECRET_KEY`: Django secret key

## Local Development

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd OCRtesrect
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start development server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `GET /`: Main OCR upload form
- `GET /health/`: Health check endpoint
- `POST /`: Upload image for OCR processing

## File Structure

```
OCRtesrect/
├── OCRtesrect/
│   ├── settings.py              # Development settings
│   ├── settings_production.py   # Production settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # Development WSGI
│   └── wsgi_production.py       # Production WSGI
├── ocrapp/
│   ├── views.py                 # OCR views
│   ├── urls.py                  # App URLs
│   └── templates/               # HTML templates
├── vercel.json                  # Vercel configuration
├── requirements.txt             # Python dependencies
├── build_files.sh              # Build script
├── manage.py                   # Development management
├── manage_production.py        # Production management
└── README.md                   # This file
```

## Security Features

- CSRF protection enabled
- Secure cookie settings
- HSTS headers
- XSS protection
- Content type sniffing protection
- File upload validation
- Size limits (10MB)

## Performance Optimizations

- Database connection pooling
- Static file compression
- Caching with database backend
- Optimized middleware stack

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure your Neon database is accessible
2. **File Uploads**: Check file size limits and storage configuration
3. **Static Files**: Verify WhiteNoise configuration
4. **OCR Processing**: Ensure EasyOCR dependencies are installed

### Logs

Check Vercel function logs for debugging:
```bash
vercel logs
```

## License

This project is licensed under the MIT License. 