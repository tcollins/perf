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
		```ALTER TABLE `rawlog` ADD UNIQUE `rawlog_unique_index`(`created`, `duration`, `app`, `method`);```

----------

#### Load performance log data into the app
```sh
curl -F "appname=AppNameGoesHere" -F "file=@performance.log" http://localhost:5000/upload-data
```

----------


```
SELECT DATE_FORMAT(created, '%Y-%m-%d 00:00:00') formattedcreated, app, method,
count(duration) callcount,  sum(duration) totalduration,
round(avg(duration)) avgduration, min(duration) minduration, max(duration) maxduration, std(duration) stdev
FROM rawlog
group by app, method, formattedcreated
```