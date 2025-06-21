from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os
import easyocr
from PIL import Image
import logging
import tempfile
import boto3
from botocore.exceptions import NoCredentialsError
import io

logger = logging.getLogger(__name__)

def health_check(request):
    """Health check endpoint for Vercel"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'OCR API is running'
    })

def ocr_image_view_cloud(request):
    extracted_text = None
    image_url = None
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
            
            # Process image in memory (no local storage)
            image_data = image_file.read()
            
            # Use EasyOCR with in-memory processing
            reader = easyocr.Reader(['en'], gpu=False)
            
            # Convert to PIL Image for processing
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Save to temporary file for EasyOCR
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                pil_image.save(temp_file.name, 'PNG')
                temp_path = temp_file.name
            
            try:
                # Process with EasyOCR
                result = reader.readtext(temp_path, detail=0, paragraph=True)
                extracted_text = '\n'.join(result)
                
                # Upload to cloud storage (AWS S3 example)
                image_url = upload_to_cloud_storage(image_data, image_file.name)
                
                logger.info(f"OCR processing completed for file: {image_file.name}")
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        error_message = "An error occurred while processing the image. Please try again."
    
    return render(request, 'ocrapp/ocr_form.html', {
        'extracted_text': extracted_text, 
        'image_url': image_url,
        'error_message': error_message
    })

def upload_to_cloud_storage(image_data, filename):
    """Upload image to cloud storage (AWS S3 example)"""
    try:
        # Configure S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        
        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f'ocr_images/{filename}',
            Body=image_data,
            ContentType='image/png'
        )
        
        # Return public URL
        return f"https://{bucket_name}.s3.amazonaws.com/ocr_images/{filename}"
        
    except NoCredentialsError:
        logger.error("AWS credentials not found")
        return None
    except Exception as e:
        logger.error(f"Error uploading to S3: {str(e)}")
        return None 