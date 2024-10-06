from PIL import Image
import os

for filename in os.listdir():
    if filename.endswith('.webp'):
        image = Image.open(filename)
        png_filename = os.path.splitext(filename)[0] + '.png'
        image.save(png_filename, 'PNG')

        print(f'changed {filename} for {png_filename}')

print('success')
