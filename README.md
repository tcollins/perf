**Perf**
=========
## Performance Log Aggregator and Reporting Dashboard for performance logs. ##

> ### A Flask/Python app ###


----------

## Install ##


### prerequisites packages ###
```sh
git python2.7 mysql-server mysql-client libmysqlclient-dev python-mysqldb python-dev
```


### create a virutalenv in the project dir   ###
```sh
<working dir>$ virtualenv env
```


### activate virtualenv   ###
```sh
<working dir>$ . env/bin/activate
```

		
### install required python packages  ###
```sh
<working dir>$ pip install -r requirements.txt
```


### create "perf" mysql database and run the create schema script ### 
```sh
<working dir>$ mysql -u root -p perf < perf-schema.sql
```

### modify "config.py" as needed ###
```sh
UPLOAD_FOLDER = '/home/tcollins/dev/perf/.data-uploads'

SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/perf'
SQLALCHEMY_ECHO = True
```

----------

## Run ###

```sh
<working dir>$ python run.py
```

----------

## Load performance log data into the app ##

```sh
curl -F "appname=AppNameGoesHere" -F "file=@performance.log" http://localhost:5000/api/upload-data
```

## Trigger the data aggregator to update ##
```sh
curl http://localhost:5000/api/aggregate
```

----------