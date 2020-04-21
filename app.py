import os
from flask import Flask, request, make_response
from werkzeug.utils import secure_filename
from fastai2.vision.all import *

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bird', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return {'error': 'no image found.'}, 200

    file = request.files['image'] 
    if file.filename == '':
        return {'error': 'no image found.'}, 200

    if file and allowed_file(file.filename): 
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        learn_inf = load_learner('export.pkl')
        prediction = learn_inf.predict(filepath)
        return {'success': prediction[0]}, 200

    return {'error': 'something went wrong.'}

if __name__ == '__main__':
    port = os.getenv('PORT',5000)
    app.run(debug=True, host='0.0.0.0', port=port)
