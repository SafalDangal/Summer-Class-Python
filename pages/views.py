from django.shortcuts import render
from django.http import JsonResponse
import openai
import os

def generate_product_description(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name', '')
        product_features = request.POST.get('product_features', '')
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "Generate a marketing product description based on the product name and features. Keep it under 150 words."
                }, {
                    "role": "user",
                    "content": f"Product: {product_name}\nFeatures: {product_features}"
                }],
                api_key=os.getenv('OPENAI_API_KEY')
            )
            
            description = response.choices[0].message.content.strip()
            return JsonResponse({'description': description})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)
from django.http import HttpResponse
from .models import Pages

# Create your views here.
def pages(request, slug):
    page = Pages.objects.filter(slug=slug).first()
    if not page:
        return HttpResponse("Page not found", status=404)   