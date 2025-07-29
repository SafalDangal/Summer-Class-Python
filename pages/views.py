from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages

# Create your views here.
def pages(request, slug):
    page = Pages.objects.filter(slug=slug).first()
    if not page:
        return HttpResponse("Page not found", status=404)   