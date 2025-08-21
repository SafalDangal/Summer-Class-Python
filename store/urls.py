from django.urls import path
from . import views

urlpatterns = [
	# Dynamic store routes
	path('', views.store, name='store'),
	path('category/<slug:category_slug>/', views.store, name='products_by_category'),
	# Product detail must come before the subcategory route to avoid slug collisions
	path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
	path('category/<slug:category_slug>/<slug:subcategory_slug>/', views.store, name='products_by_subcategory'),
	path('search/', views.search, name='search'),
	path('ai/ask/', views.ai_product_answer, name='ai_product_answer'),

	# Backwards-compatible product detail by id -> redirect to canonical slug URL
	path('product/<int:pk>/', views.product_detail_by_id, name='product_detail_by_id'),

	# My dashboard & product management
	path('me/', views.my_dashboard, name='store_dashboard'),
	path('me/products/', views.my_products, name='my_products'),
	path('me/products/add/', views.product_create, name='product_create'),
	path('me/products/<int:pk>/edit/', views.product_update, name='product_update'),
	path('me/products/<int:pk>/delete/', views.product_delete, name='product_delete'),

	# Variation management
	path('me/products/<int:product_id>/variations/', views.variation_list, name='variation_list'),
	path('me/products/<int:product_id>/variations/add/', views.variation_create, name='variation_create'),
	path('me/products/<int:product_id>/variations/<int:variation_id>/delete/', views.variation_delete, name='variation_delete'),
	
	# Categories list
	path('categories/', views.categories_list, name='categories_list'),

	# Static category routes (backup)
	path('static/category/tshirt/', views.tshirt_category, name='tshirt_category'),
	path('static/category/electronics/', views.electronics_category, name='electronics_category'),
	path('static/category/home-living/', views.home_living_category, name='home_living_category'),
	path('static/category/books/', views.books_category, name='books_category'),
	path('static/category/accessories/', views.accessories_category, name='accessories_category'),
]
