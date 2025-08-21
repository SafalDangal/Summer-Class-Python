import os
import base64

def write_file(path, data_bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data_bytes)

# 1x1 PNG (transparent)
png_b64 = b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
png = base64.b64decode(png_b64)

# write to several locations
files = [
    'static/images/placeholder.jpg',
    'static/images/banners/2.jpg',
    'media/photos/products/placeholder.jpg',
]
for p in files:
    write_file(p, png)

# simple favicon.ico (reuse png bytes; browsers accept PNG in many contexts)
write_file('static/images/favicons/favicon.ico', png)

# tiny placeholder font files (not real fonts, just to avoid 404s)
font_paths = [
    'static/fonts/fontawesome/webfonts/fa-solid-900.woff2',
    'static/fonts/fontawesome/webfonts/fa-solid-900.woff',
    'static/fonts/fontawesome/webfonts/fa-solid-900.ttf',
]
for p in font_paths:
    write_file(p, b"placeholder-font-file")

print('Wrote placeholder files:')
for p in files + ['static/images/favicons/favicon.ico'] + font_paths:
    print(' -', p)
