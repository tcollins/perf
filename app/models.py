from app import app 

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
                app.logger.info(line)  
        