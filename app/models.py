from app import app, db 
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
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
    
    def formattedMethod(self):
        return formatMethodName(self.method)

    
############################################################
## MonthlySummary
## 
class MonthlySummary(db.Model):
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
        return '<MonthlySummary {} {}.{} - {},{}>'.format(self.formattedcreated, self.app, self.method, self.callcount, self.avgduration)    
    
    def formattedMethod(self):
        return formatMethodName(self.method)
        
    
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
        
        self.findMaxCreateDay()
        self.findMaxCreateMonth()
        
        ##app.logger.info(self.maxcreatedday)
        ##app.logger.info(self.maxcreatedmonth)
        
        self.deleteDaily()
        self.aggregateDaily()
        
        self.deleteMonthly()
        self.aggregateMonthly()
        
        
    ## findMaxCreateDay ############################################     
    def findMaxCreateDay(self):
        startDateSQL = "SELECT max(formattedcreated) maxcreated FROM daily_summary;"
        result = db.session.execute(startDateSQL)
        
        for row in result:
            maxcreated = row['maxcreated']
            if (maxcreated is not None): 
                self.maxcreatedday = maxcreated + timedelta(days=-5)
                ##self.maxcreatedmonth = maxcreated + relativedelta( months = -1 )
                ##self.maxcreatedmonth = self.maxcreatedmonth.replace(day=1)
    
    
    ## findMaxCreateMonth ############################################     
    def findMaxCreateMonth(self):
        sql = "SELECT max(formattedcreated) maxcreated FROM monthly_summary;"
        result = db.session.execute(sql)
        
        for row in result:
            maxcreated = row['maxcreated']
            if (maxcreated is not None):                 
                self.maxcreatedmonth = maxcreated + relativedelta( months = -1 )
                self.maxcreatedmonth = self.maxcreatedmonth.replace(day=1)
                
            
    ## deleteDaily ############################################         
    def deleteDaily(self):
        deleteDailySQL = "delete FROM daily_summary where formattedcreated > :maxcreated"    
        db.session.execute(deleteDailySQL, {'maxcreated':self.maxcreatedday})
        db.session.commit()
        
    ## deleteMonthly ############################################         
    def deleteMonthly(self):
        deleteMonthlySQL = "delete FROM monthly_summary where formattedcreated > :maxcreated"    
        db.session.execute(deleteMonthlySQL, {'maxcreated':self.maxcreatedmonth})
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
            
    ## aggregateMonthly ############################################             
    def aggregateMonthly(self):
        monthlyAggSQL = "SELECT DATE_FORMAT(created, '%Y-%m-01 00:00:00') formattedcreated, app, method, count(duration) callcount, sum(duration) totalduration, round(avg(duration)) avgduration, min(duration) minduration, max(duration) maxduration, std(duration) stdev FROM rawlog where created > :maxcreated group by app, method, formattedcreated"
        
        result = db.session.execute(monthlyAggSQL, {'maxcreated':self.maxcreatedmonth})                
        
        for row in result:
            monthly = MonthlySummary()
            monthly.formattedcreated = row['formattedcreated']
            monthly.app = row['app']
            monthly.method = row['method']
            monthly.callcount = row['callcount']
            monthly.totalduration = row['totalduration']
            monthly.avgduration = row['avgduration']            
            monthly.minduration = row['minduration']
            monthly.maxduration = row['maxduration']
            monthly.stdev = row['stdev']                       
           
            try:
                db.session.add(monthly)
                db.session.commit()
            except IntegrityError: 
                db.session.rollback()            

############################################################
## Helper methods                
def formatMethodName(methodname):
        arr = methodname.split('.')
        l = len(arr)        
        return '{}.{}'.format(arr[l-2],arr[l-1])                
                
############################################################
## Query methods

def findAllAppNames():    
    arr = []
    
    apps = db.session.query(MonthlySummary.app.distinct()).order_by(MonthlySummary.app).all()
    for appname in apps:       
        arr.append(appname[0])        
    
    return arr;

def findMonthlySummaryByAppAndMonth(appname, date, orderStr):     
    
    date = date.replace(day=1)
    date = date.replace(hour=0,minute=0,second=0,microsecond=0)
    
    allowedOrderBy = ['callcount', 'totalduration', 'avgduration', 'minduration', 'maxduration', 'stdev']
    order = 'callcount'
    if any(orderStr in s for s in allowedOrderBy):
        order = orderStr
    
    records = MonthlySummary.query.filter_by(app=appname,formattedcreated=date).order_by(order + ' desc').all()
    return records

def findTimeBucketDateForMethod(appname, methodname):
    ## TODO add date range to method args and query

    sql = "select count(*) from rawlog where app = :appname and method = :methodname and duration >= :durmin and duration <=:durmax"
  
    #0-9
    #10-29
    #30-49
    #50-99
    #100-199
    #200-299
    #300-499
    #500-699
    #700-999
    #1000-1999
    #2000+
    
    buckets = [
        {"min":0,"max":9},
        {"min":10,"max":29},
        {"min":30,"max":49},
        {"min":50,"max":99},
        {"min":100,"max":199}
    ]
    
    for bucket in buckets:        
        result = db.session.execute(sql, {'appname':appname, 'methodname':methodname, 'durmin':bucket["min"], 'durmax':bucket["max"]})         
        bucket["cnt"] = int(result.fetchone()[0])
        
    
    app.logger.info(buckets)
    
    return buckets
    
    
#def findDailySummaryByAppAndDay(appname, day):        
#    records = DailySummary.query.filter_by(app=appname).all()
#    return records

