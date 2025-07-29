from .models import Pages
def pages_links (request): 
    pages= Pages.objects.all()
    return {'pages_links': pages}