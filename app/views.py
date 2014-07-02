# imports
import os
from flask import request, render_template, url_for, redirect
from werkzeug import secure_filename
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pprint import pprint

from app import app, models

# Front page
@app.route('/')
def index():  
    apps = models.findAllAppNames()        
    app.logger.info('t i m')    
    return render_template("index.html", title="PERF", apps=apps)


@app.route('/dashboard/<appname>')
def dashboard(appname):    
    
    title="PERF - " + appname + " Dashboard"
    now = datetime.now()    
    
    dateParam = request.args.get('d')
    try:
        date = datetime.strptime(dateParam, '%m-%Y')
    except:
        date = now
   
    orderParam = request.args.get('o', 'callcount')    
    summaryData = models.findMonthlySummaryByAppAndMonth(appname, date, orderParam)
        
    dateInfo = {
        "friendly": date.strftime('%B %Y'),
        "curParam": date.strftime('%m-%Y'),
        "prevParam": (date + relativedelta( months = -1 )).strftime('%m-%Y'),
        "nextParam": (date + relativedelta( months = +1 )).strftime('%m-%Y')
    }
    
    urlPrefix = "/dashboard/"+appname+"?d=" + dateInfo["curParam"]
    
    return render_template("dashboard.html", title=title, appname=appname, summaryData=summaryData, dateInfo=dateInfo, urlPrefix=urlPrefix)

@app.route('/method/<appname>/<methodname>')
def method(appname, methodname): 
    formattedMethod = models.formatMethodName(methodname)
    title="PERF - " + appname + " - " + formattedMethod        
    
    timeBucketData = models.findTimeBucketDateForMethod(appname, methodname)
    
    return render_template("method.html", title=title, appname=appname, methodname=methodname, formattedMethod=formattedMethod)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


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
