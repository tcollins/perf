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
    
    #apps = models.DailySummary.query(models.DailySummary.app.distinct()).all();
    #apps = models.db.session.query(models.DailySummary.app.distinct()).all()
    apps = models.findAllAppNames()
    #admin = User.query.filter_by(username='admin').first()
    
    app.logger.info(apps)
    
    return render_template("index.html", title="PERF", apps=apps)

@app.route('/tim')
def tim():
    app.logger.info('Tim')
    ##dataLoader.loadFromFilePath('/home/tcollins/dev/temp/test-performance-short.log');
    ##models.create_initial_db_schema();
    
    ##aggregator = models.DataAggregator();
    #aggregator.aggregate();            
    return "TIM"

def allowed_file(file):
    return True

@app.route('/api/')
def api():
    return render_template("api.html", title="PERF - API Documentation") 

@app.route('/api/upload-data', methods=['POST'])
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
            
            return "Data Upload Complete!" 
       
    
@app.route('/api/aggregate')
def apiAggregate():        
    aggregator = models.DataAggregator();
    aggregator.aggregate();            
    return "Aggregation Complete!"
