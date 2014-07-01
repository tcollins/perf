**Perf**
=========
#### Performance Log Aggregator and Reporting Dashboard for performance logs. 

A Flask/Python app


----------

#### Install

- prerequisites packages  
		```git python2.7 mysql-server mysql-client libmysqlclient-dev python-mysqldb python-dev```
        
- create a virutalenv in the project dir  
		```<working dir>$ virtualenv env```
		
- activate virtualenv  
		```<working dir>$ . env/bin/activate```
		
- install required python packages  
		```<working dir>$ pip install -r requirements.txt```

- create "perf" mysql database and run the create schema script  
		```<working dir>$ mysql -u root -p perf < perf-schema.sql```

- modify "config.py" as needed

----------

#### Run

```<working dir>$ python run.py```

----------

#### Load performance log data into the app
```sh
curl -F "appname=AppNameGoesHere" -F "file=@performance.log" http://localhost:5000/api/upload-data
```

#### Trigger the data aggregator to update
```sh
curl http://localhost:5000/api/aggregate
```

----------

