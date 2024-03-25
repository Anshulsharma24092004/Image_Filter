from flask import Flask, render_template, request, redirect, url_for
from PIL import ImageFilter, Image
from io import BytesIO
import numpy as np
import base64

app = Flask(__name__)

def apply_filter(image, filter_type):
    if filter_type == 'blur':
        return image.filter(ImageFilter.BLUR)
    elif filter_type == 'crop':
        width, height = image.size
        left = width / 4
        top = height / 4
        right = 3 * width / 4
        bottom = 3 * height / 4
        return image.crop((left, top, right, bottom))
    elif filter_type == 'rotate':
        return image.rotate(45)
    else:
        return image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    
    image_file = request.files['image']
    if image_file.filename == '':
        return redirect(request.url)

    filter_type = request.form['filter']
    
    image = Image.open(image_file)
    filtered_image = apply_filter(image, filter_type)

    buffered = BytesIO()
    filtered_image.save(buffered, format="JPEG")
    img_str = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()

    return render_template('result.html', result=img_str)

if __name__ == '__main__':
    app.run(debug=True)
