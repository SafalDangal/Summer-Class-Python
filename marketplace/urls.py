"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.static import static
from django.conf import settings
from . import views
from products import views as productviews
from siteconfig import views as siteconfigviews

urlpatterns = [
	path('admin/', admin.site.urls),
	path('home/',views.home),
	path('home-store/', views.home_store, name='home_store'),
	path('products/', include('products.urls')),
	path('blogs/', include('blogs.urls')),
	path('dashboard/', siteconfigviews.dashboard, name='dashboard'),
	path('', views.home, name='home'),  # Back to original home view
	path('store/', include('store.urls')),
	path('cart/', include('carts.urls')),
	path('products1/', productviews.products, name='products1'),  # Updated to use the new products view
	path('cart/', include('carts.urls')),  # Include carts URLs for cart functionality
	path('login/', siteconfigviews.login_user, name='login'),
	path('register/', siteconfigviews.register_user, name='register'),
	path('logout/', siteconfigviews.logout_user, name='logout'),
	path('profile/', siteconfigviews.profile, name='profile'),
	path('change-password/', siteconfigviews.change_password, name='change_password'),
	path('orders/', siteconfigviews.my_orders, name='orders'),
	path('pages/', include('pages.urls')),  # Add AI features
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
