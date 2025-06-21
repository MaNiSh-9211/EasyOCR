from django.shortcuts import render
from django.http import JsonResponse
import easyocr
from PIL import Image
import logging
import tempfile
import io

logger = logging.getLogger(__name__)

def health_check(request):
    """Health check endpoint for Vercel"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'OCR API is running'
    })

def ocr_image_view_memory_only(request):
    extracted_text = None
    error_message = None
    
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            image_file = request.FILES['image']
            
            # Validate file type
            if not image_file.content_type.startswith('image/'):
                error_message = "Please upload a valid image file."
                return render(request, 'ocrapp/ocr_form.html', {
                    'error_message': error_message
                })
            
            # Validate file size (10MB limit)
            if image_file.size > 10 * 1024 * 1024:
                error_message = "File size too large. Please upload an image smaller than 10MB."
                return render(request, 'ocrapp/ocr_form.html', {
                    'error_message': error_message
                })
            
            # Read image data into memory
            image_data = image_file.read()
            
            # Use EasyOCR for text extraction
            reader = easyocr.Reader(['en'], gpu=False)
            
            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Save to temporary file for EasyOCR processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                pil_image.save(temp_file.name, 'PNG')
                temp_path = temp_file.name
            
            try:
                # Process with EasyOCR
                result = reader.readtext(temp_path, detail=0, paragraph=True)
                extracted_text = '\n'.join(result)
                
                logger.info(f"OCR processing completed for file: {image_file.name}")
                
            finally:
                # Clean up temporary file
                import os
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        error_message = "An error occurred while processing the image. Please try again."
    
    return render(request, 'ocrapp/ocr_form.html', {
        'extracted_text': extracted_text, 
        'image_url': None,  # No image storage
        'error_message': error_message
    }) 