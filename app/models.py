from app import app, db 
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from pprint import pprint

def create_initial_db_schema():
    db.create_all()
    

############################################################
## Rawlog
##
## 06/27/14 21:27:18,733|SERVICE|9|findTabletBySlug|com.digitalassent.adserver.services.AdServerService
## 
class Rawlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable = False)
    duration = db.Column(db.Integer, nullable = False)    
    app = db.Column(db.String(40), nullable = False, index=True) ## DocScores
    method = db.Column(db.String(200), nullable = False, index=True) ## com...AdServerService.findTabletBySlug
    
    ##def __init__(self, username, email):
    ##    self.username = username
    ##    self.email = email

    def __repr__(self):
        return '<Rawlog {} [{}] {}>'.format(self.created, self.duration, self.method)

############################################################
## DailySummary
## 
class DailySummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formattedcreated = db.Column(db.DateTime, nullable = False, index=True)    
    app = db.Column(db.String(40), nullable = False, index=True) ## DocScores
    method = db.Column(db.String(200), nullable = False, index=True) ## com...AdServerService.findTabletBySlug
    callcount = db.Column(db.Integer, nullable = False, index=True)    
    totalduration = db.Column(db.Integer, nullable = False)    
    avgduration = db.Column(db.Integer, nullable = False, index=True)    
    minduration = db.Column(db.Integer, nullable = False)    
    maxduration = db.Column(db.Integer, nullable = False)   
    stdev = db.Column(db.Float, nullable = False)   
    
    def __repr__(self):
        return '<DailySummary {} {}.{} - {},{}>'.format(self.formattedcreated, self.app, self.method, self.callcount, self.avgduration)    
    
############################################################
## DataLoader
class DataLoader():
    appname = "Default"    

    def __init__(self, appname):
        if appname:           
            self.appname = appname
        
    def loadFromFilePath(self, filepath):        
        app.logger.info('loadFromFilePath')
        app.logger.info(filepath)
        with open(filepath) as f:
            for line in f:
                self.loadLine(line)
    
    def loadLine(self, line):        
        # split the pipe delimited line into an array
        arr = line.split('|')
        
        rawlog = Rawlog()
        rawlog.created = datetime.strptime(arr[0], '%m/%d/%y %H:%M:%S,%f') # 06/27/14 21:27:18,733 
        rawlog.duration = int(arr[2])
        rawlog.method = "{}.{}".format(arr[4].strip(), arr[3].strip())
        rawlog.app = self.appname
        
        #app.logger.info(rawlog)
        # insert the rawlog, if it's a duplicate the database's unique composite key will reject it
        try:
            db.session.add(rawlog)
            db.session.commit()
        except IntegrityError: 
            db.session.rollback()
            
                        
############################################################
## DataAggregator
class DataAggregator():
    maxcreatedday = '2010-01-01 00:00:00'
    maxcreatedmonth = '2010-01-00 00:00:00'
    
    ## init ############################################ 
    def __init__(self):
        self.maxcreatedday = '2010-01-01 00:00:00'
    
    ## aggregate ############################################ 
    def aggregate(self):        
        app.logger.info('aggregate')
        
        self.findStartDate()
        self.deleteDaily()
        self.aggregateDaily()
        
        
    ## findStartDate ############################################     
    def findStartDate(self):
        startDateSQL = "SELECT max(formattedcreated) maxcreated FROM daily_summary;"
        result = db.session.execute(startDateSQL)
        
        for row in result:
            maxcreated = row['maxcreated']
            if (maxcreated is not None): 
                self.maxcreatedday = maxcreated + timedelta(days=-5)
              
            
    ## deleteDaily ############################################         
    def deleteDaily(self):
        deleteDailySQL = "delete FROM daily_summary where formattedcreated > :maxcreated"    
        db.session.execute(deleteDailySQL, {'maxcreated':self.maxcreatedday})
        db.session.commit()
        
        
    ## aggregateDaily ############################################             
    def aggregateDaily(self):
        dailyAggSQL = "SELECT DATE_FORMAT(created, '%Y-%m-%d 00:00:00') formattedcreated, app, method, count(duration) callcount, sum(duration) totalduration, round(avg(duration)) avgduration, min(duration) minduration,  max(duration) maxduration, std(duration) stdev FROM rawlog where created > :maxcreated group by app, method, formattedcreated"
        result = db.session.execute(dailyAggSQL, {'maxcreated':self.maxcreatedday})                
        
        for row in result:
            daily = DailySummary()
            daily.formattedcreated = row['formattedcreated']
            daily.app = row['app']
            daily.method = row['method']
            daily.callcount = row['callcount']
            daily.totalduration = row['totalduration']
            daily.avgduration = row['avgduration']            
            daily.minduration = row['minduration']
            daily.maxduration = row['maxduration']
            daily.stdev = row['stdev']                       
           
            try:
                db.session.add(daily)
                db.session.commit()
            except IntegrityError: 
                db.session.rollback()
            
        