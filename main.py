import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from ArabicOcr import arabicocr

upload_folder = r"C:\Users\eslam\PycharmProjects\MyAPI\static"
allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

app = Flask(__name__)
app.config['upload_folder'] = upload_folder

@app.route('/media/upload', methods = ['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error': 'Media not provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("filename : ", filename)
        #imagePath=os.path.join(app.config['upload_folder'], filename)
        #print("imagePath : ", imagePath)
        file.save(os.path.join(app.config['upload_folder'], filename))
        result=processImage(os.path.join(app.config['upload_folder'], filename))
    return jsonify({'result': result})

def processImage(image_path):
    # image_path = r'C:\Users\eslam\Downloads\Graduation Project\2.png'
    out_image = r'C:\Users\eslam\OneDrive\Desktop\out2.jpg'
    results = arabicocr.arabic_ocr(image_path, out_image)
    print(results)
    words = []
    for i in range(len(results)):
        word = results[i][1]
        words.append(word)
    with open('file.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(str(words))
    return words

if __name__ == "__main__":
    app.run(debug=True, port=5000)