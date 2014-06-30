# imports
import os
from flask import request, render_template, url_for, redirect
from werkzeug import secure_filename
from pprint import pprint

from app import app, models

# Front page
@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tim')
def tim():
    app.logger.info('Tim')
    ##dataLoader.loadFromFilePath('/home/tcollins/dev/temp/test-performance-short.log');
    ##models.create_initial_db_schema();
    return "TIM"

def allowed_file(file):
    return True

@app.route('/upload-data', methods=['GET', 'POST'])
def uploaddata():
    if request.method == 'POST':
        file = request.files['file']        
        ##pprint(vars(request))        
        appname = request.form['appname']        
        if file and allowed_file(file):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            dataLoader = models.DataLoader(appname);
            dataLoader.loadFromFilePath(filepath);
            
            return redirect(url_for('uploaddata'))  
        
    return render_template("upload-data.html")    
       