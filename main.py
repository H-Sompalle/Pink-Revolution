from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)

# Configuration for file upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Configuration for Azure Custom Vision Prediction API
ENDPOINT = "your_predicition_url"
HEADERS = {'Prediction-Key': 'your_prediction_key'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_image(image_data):
    response = requests.post(ENDPOINT, headers=HEADERS, data=image_data)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        image_data = file.read()
        prediction = process_image(image_data)
        return render_template('result.html', prediction=prediction)
    else:
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
