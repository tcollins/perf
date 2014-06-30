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
		```ALTER TABLE `rawlog` ADD UNIQUE `rawlog_unique_index`(`created`, `duration`, `method`);```

----------

#### Load performance log data into the app
```sh
curl -F "file=@performance.log" http://localhost:5000/upload-data
```

----------

...
