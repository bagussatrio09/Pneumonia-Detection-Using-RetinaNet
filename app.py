from flask import Flask, render_template, request
from PIL import Image
from utils import plot_image, detection, delete_file, checking_file_format
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = '124-407-823'
app.config['UPLOAD_FOLDER'] = 'static/files/'

@app.route('/')
def index():
    delete_file(app.config['UPLOAD_FOLDER'])
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    delete_file(app.config['UPLOAD_FOLDER'])
    
    image = request.files['image']
    if image.filename == '':
        return render_template('index.html', alert="File Belum Diupload")
    if image and checking_file_format(image.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pneumonia.jpg')
        image.save(filename)
        img = Image.open(filename)
        img_gray = img.convert('L')
        gray_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pneumonia.jpg')
        img_gray.save(gray_filename)
        plot_img = plot_image(filename)
        return render_template('index.html', plot_img=plot_img, alert="File Berhasil Diupload")
    return render_template('index.html', alert="Format file harus: jpg, jpeg, png")

@app.route('/process', methods=['POST'])
def process():
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pneumonia.jpg')
    if os.path.exists(filename):
        plot_img = plot_image(filename)
        plot_url, detectionStatus = detection()
        if detectionStatus:
            return render_template('index.html', plot_img=plot_img,plot_url=plot_url, alert="Terdeteksi Pneumonia")
        else:
            return render_template('index.html', plot_img=plot_img,plot_url=plot_url, alert="Sehat")
    return render_template('index.html', alert="Tidak ada file yang dipilih")

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True, port=8000, ) 