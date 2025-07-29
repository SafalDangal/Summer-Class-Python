from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Blog


def blogs(request):
    all_blogs = Blog.objects.all()
    return render(request, 'extending/blogs1.html', {'blogs': all_blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})

