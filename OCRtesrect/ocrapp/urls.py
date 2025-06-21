from django.urls import path
from .views import ocr_image_view, health_check

urlpatterns = [
    path('', ocr_image_view, name='ocr_image'),
    path('health/', health_check, name='health_check'),
] 