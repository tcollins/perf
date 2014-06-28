# imports
import os
from flask import request, render_template, url_for, redirect
from werkzeug import secure_filename

from app import app

# Front page
@app.route('/index')
@app.route('/')
def index():
    return render_template("hello.html")

@app.route('/tim')
def tim():
    return "TIM"

def allowed_file(file):
    return True

@app.route('/upload-data', methods=['GET', 'POST'])
def uploaddata():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaddata', filename=filename))   
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''