# Islington MarketPlace

A clean, organized Django e-commerce marketplace application that recreates the exact functionality and design from [http://deploying.xyz/](http://deploying.xyz/).

## Website Recreation

This project recreates the exact same website as [deploying.xyz](http://deploying.xyz/) with:

### Header Features
- Language selection (English)
- Currency selection (USD)
- Contact information (Email, Call us)
- Logo and branding
- Category dropdown (All Products, Tshirt, Electronics, Home & Living, Books, Accessories)
- Store button
- Search functionality
- User menu (Login, Register, Dashboard)
- Shopping cart with item count

### Homepage Content
- **Popular products** section with exact same products:
  - Wireless Noise Cancelling Headphones - Rs. 15999
  - Wooden Study Lamp - Rs. 3450
  - The Psychology of Money - Rs. 1499
  - Vintage Leather Wallet - Rs. 2899
  - Smart Fitness Band - Rs. 3299
  - Basic White T-Shirt - Rs. 2000
  - 4K Android Smart TV – 43 Inch - Rs. 45000
  - Decorative Wall Clock - Rs. 2250

### Footer Content
- Copyright: © 2025 Market Place
- Website: https://www.deploying.xyz/
- Phone: 9822342212
- Address: Kamalpokhari, Kathmandu, Nepal
- Payment methods: Visa, PayPal, Mastercard

## Project Structure

### Templates
All templates are organized in the `templates/extending/` directory:

- **`base1.html`** - Main base template with header, footer, and content blocks
- **`header1.html`** - Navigation header matching deploying.xyz exactly
- **`footer1.html`** - Footer with company information and payment methods
- **`home1.html`** - Homepage with popular products section
- **`store.html`** - Store page with all products
- **`products.html`** - Product listing page
- **`product_details.html`** - Individual product detail page
- **`blogs.html`** - Blog listing page
- **`blog_details.html`** - Individual blog post page
- **`cart.html`** - Shopping cart page
- **`login.html`** - User login page
- **`register.html`** - User registration page
- **`dashboard.html`** - User dashboard page

### Key Features

- **Exact Website Match**: Recreates deploying.xyz with identical content and structure
- **Clean Template Structure**: Header, footer, and content sections are properly separated
- **Responsive Design**: Bootstrap-based responsive layout
- **SEO Optimized**: Proper meta tags and structured content
- **User Management**: Login, registration, and dashboard functionality
- **Product Management**: Product listing and detail views
- **Shopping Cart**: Basic cart functionality

### Template Blocks

The base template provides these customizable blocks:
- `title` - Page title
- `description` - Meta description
- `keywords` - Meta keywords
- `og_title` - Open Graph title
- `og_description` - Open Graph description
- `extra_css` - Additional CSS files
- `extra_js` - Additional JavaScript files
- `content` - Main page content

### Usage

1. **Extend the base template**: `{% extends 'extending/base1.html' %}`
2. **Override blocks as needed**: `{% block title %}Custom Title{% endblock %}`
3. **Add your content**: `{% block content %}Your content here{% endblock %}`

### Static Files

- CSS: `static/css/`
- JavaScript: `static/js/`
- Images: `static/images/`
- Fonts: `static/fonts/`

### Running the Project

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Start development server: `python manage.py runserver`
4. Access the site at: `http://localhost:8000`

## Website Match

This Django application perfectly recreates [http://deploying.xyz/](http://deploying.xyz/) with:

✅ **Identical Header**: Same navigation, categories, search, and user menu
✅ **Same Products**: All 8 products with exact names and prices
✅ **Same Layout**: Product grid with 4 columns
✅ **Same Footer**: Company info, contact details, and payment methods
✅ **Same Branding**: Islington MarketPlace logo and styling
✅ **Same Functionality**: Category navigation, search, cart, user accounts

The codebase is now clean, organized, and follows Django best practices while maintaining the exact same look and functionality as your original website.
