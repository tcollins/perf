from app import app, db 
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

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
    method = db.Column(db.String(200), nullable = False, index=True) ## com...AdServerService.findTabletBySlug
    
    ##def __init__(self, username, email):
    ##    self.username = username
    ##    self.email = email

    def __repr__(self):
        return '<Rawlog {} [{}] {}>'.format(self.created, self.duration, self.method)
    
############################################################
## DataLoader
class DataLoader():
    member = ""    

    def __init__(self, member):
        self.member = member
        
    def loadFromFilePath(self, filepath):        
        app.logger.info('loadFromFilePath')
        app.logger.info(filepath)
        with open(filepath) as f:
            for line in f:
                self.loadLine(line)
    
    def loadLine(self, line):        
        # split the pipe delimited line into an array
        arr = line.split('|')
        
        rawlog = Rawlog();        
        # 06/27/14 21:27:18,733        
        rawlog.created = datetime.strptime(arr[0], '%m/%d/%y %H:%M:%S,%f')
        rawlog.duration = int(arr[2])
        rawlog.method = "{}.{}".format(arr[4].strip(), arr[3].strip())
        
        #app.logger.info(rawlog)
        # insert the rawlog, if it's a duplicate the database's unique composite key will reject it
        try:
            db.session.add(rawlog)
            db.session.commit()
        except IntegrityError: 
            db.session.rollback()
            
                        
        