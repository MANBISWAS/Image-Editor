from flask import Flask,render_template,request,flash
import os
from werkzeug.utils import secure_filename

import cv2




UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'avif' ,'webp','png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER







def processImage(filename , operation):
    print(f"The opreration is   {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")

    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
           

        case "cjpeg":
            newFilename = f"static/{filename}"
            cv2.imwrite(F"static/{filename.split('.')[0]}.jpeg", img)
            return filename
        
        case "cpng":
            newFilename = F"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cjpg":
            newFilename = F"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        
       
        
        case "cavif":
            newFilename = F"static/{filename.split('.')[0]}.AVIF"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cwebp":
            newFilename =F"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
       
        
           
            
            
       
    


@app.route("/")
def home():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/edit', methods=["GET" , "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # # If the user does not select a file, the browser submits an
        # # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "File not selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image have been processed and is available <a href = '/{new}' target = '_blank'>here</a>")
            return render_template("index.html")


debug = True
port = 5001
app.run(port = 5001)