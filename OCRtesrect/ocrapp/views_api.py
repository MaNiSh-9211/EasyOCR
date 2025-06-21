from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
import logging
import tempfile
import io
import requests
import base64
import json
import os

logger = logging.getLogger(__name__)

def health_check(request):
    """Health check endpoint for Vercel"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'OCR API is running'
    })

def ocr_image_view_api(request):
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
            
            # Validate file size (5MB limit for API)
            if image_file.size > 5 * 1024 * 1024:
                error_message = "File size too large. Please upload an image smaller than 5MB."
                return render(request, 'ocrapp/ocr_form.html', {
                    'error_message': error_message
                })
            
            # Read image data
            image_data = image_file.read()
            
            # Convert to base64 for API
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Use OCR.Space API (free tier available)
            extracted_text = process_with_ocr_space(image_base64, image_file.name)
            
            if not extracted_text:
                error_message = "Could not extract text from image. Please try again."
            
            logger.info(f"OCR processing completed for file: {image_file.name}")
            
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        error_message = "An error occurred while processing the image. Please try again."
    
    return render(request, 'ocrapp/ocr_form.html', {
        'extracted_text': extracted_text, 
        'image_url': None,
        'error_message': error_message
    })

def process_with_ocr_space(image_base64, filename):
    """Process image using OCR.Space API"""
    try:
        # OCR.Space API (free tier: 500 requests/day)
        url = 'https://api.ocr.space/parse/image'
        
        payload = {
            'apikey': os.environ.get('OCR_SPACE_API_KEY', 'helloworld'),  # Free demo key
            'language': 'eng',
            'isOverlayRequired': False,
            'filetype': 'png',
            'base64Image': f'data:image/png;base64,{image_base64}'
        }
        
        response = requests.post(url, data=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('ParsedResults'):
                # Extract text from all parsed results
                texts = []
                for parsed_result in result['ParsedResults']:
                    if 'ParsedText' in parsed_result:
                        texts.append(parsed_result['ParsedText'].strip())
                
                return '\n'.join(texts)
            else:
                logger.error(f"OCR API error: {result.get('ErrorMessage', 'Unknown error')}")
                return None
        else:
            logger.error(f"OCR API request failed: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Error calling OCR API: {str(e)}")
        return None

def process_with_google_vision(image_base64):
    """Process image using Google Cloud Vision API (requires API key)"""
    try:
        # Google Cloud Vision API
        url = f'https://vision.googleapis.com/v1/images:annotate?key={os.environ.get("GOOGLE_VISION_API_KEY")}'
        
        payload = {
            'requests': [
                {
                    'image': {
                        'content': image_base64
                    },
                    'features': [
                        {
                            'type': 'TEXT_DETECTION'
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'responses' in result and result['responses']:
                text_annotations = result['responses'][0].get('textAnnotations', [])
                if text_annotations:
                    return text_annotations[0].get('description', '')
            
            return None
        else:
            logger.error(f"Google Vision API request failed: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Error calling Google Vision API: {str(e)}")
        return None 