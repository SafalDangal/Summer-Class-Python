from django.urls import path
from . import views

urlpatterns = [
    path('generate-description/', views.generate_product_description, name='generate_description'),
]