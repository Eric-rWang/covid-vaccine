# Fully Vaccinated People In The United States
## Table of Contents
* [Background](#background)
* [Functions](#functions)
* [Setup](#setup)

## Background
Covid-19 devastated the entire world putting many people's lives on hold. Though the current situtation in United States sees Covid-19 retreating as vaccines become more readily available, the pandemic still rages on in other parts of the world. As of May 4, 2021 32 percent of the United State's population has been fully vaccinated and going forward, maintaining the steady increase in those getting vaccinated is key to preventing future outbreaks. This app utilizes data from "Our World In Data" to provide users with data on the number of fully vaccinated people in the United States starting Janurary 14, 2021. 

[Our World In Data (Vaccine Data)](https://ourworldindata.org/covid-vaccinations)

## Functions
This app carries with it a variety of functions which are to be used within kubernetes pods. 
Before running any of the other commands, the data must be loaded into the database (this step is only needed once, when the app is first started). 
To do so run the following command.
```
$ curl -X GET <flask_ip>:5000/load_data
{
  "id": <jid>,
  "time": <time>,
  "status": "submitted",
  "task": "load_data",
  "job_input": "none",
  "pod_ip": "not_set"
}
```

### CRUD Operations 
Basic CRUD operations can be performed with the following commands.

Create a data entry
```
$ curl -X POST -H "content-type: application/json" -d '{"location": <location>, "date": <date>, "vaccinated": <vaccinated>}' <flask_ip>:5000/create_data
{
  "result": [
    {
      "location": <location>,
      "date": <date>,
      "fully vaccinated": <vaccinated>,
      "message": "data point added"
    }
  ]
} 
```

Read data
```
$ curl -X GET <flask_ip>:5000/view_data
Returns vaccine data stored in the database.
```

Update data point
```
$ curl -X POST -H "content-type: application/json" -d '{"location": <location>, "date": <date>, "vaccinated": <vaccinated>}' <flask_ip>:5000/update_data
{
  "result": [
    {
      "location": <location>,
      "date": <date>,
      "vaccinated": <vaccinated>,
      "message": "data point updated"
    }
  ]
}
``` 

Delete data point
```
$ curl -X POST -H "content-type: application/json" -d '{"date": <date>}' <flask_ip>:5000/delete_data
{
  "result": [
    {
      "location": <location>,
      "date": <date>,
      "fully vaccinated": <vaccinated>,
      "message": "data point deleted"
    }
  ]
}
```

### Basic Operations
Retrieving all jobs
```
$ curl -X GET <flask_ip>:5000/jobs
# returns all the jobs with job information.
# use to check status of job.
```

Once an analysis operation is performed, the result can be obtained by running
```
$ curl -X POST -H "content-type: application/json" -d '{"jid": <jid>}' <flask_ip>:5000/view_results
# will return json of result.
```

### Analysis Operations
Graphing data
```
$ curl -X GET <flask_ip>:5000/graph_data
{
  "id": <jid>,
  "time": <time>,
  "status": "submitted",
  "task": "graph_data",
  "job_input": "none",
  "pod_ip": "not_set"
}
```
To download and view the graph.png
```
$ curl -X GET <flask_ip>:5000/download/<jid> > output.png
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 19839    0 19839    0     0   668k      0 --:--:-- --:--:-- --:--:--  668k
$ ls
<jid>.png
```

Estimate number of fully vaccinated people
This operation takes the date inputed by the user and using a curve fitted to the data points, it estimates the number of fully vaccinated people.
```
$ curl -X POST -H "content-type: application/json" -d '{"date": <date>}' <flask_ip>:5000/estimate
{
  "id": <jid>,
  "time": <time>,
  "status": "submitted",
  "task": "estimate_vaccinated",
  "job_input": <date>,
  "pod_ip": "not_set"
}
```
Retrieving the result can be done by curling the view_results route.
```
$ curl -X POST -H "content-type: application/json" -d '{"jid": <jid>}' <flask_ip>:5000/view_results
{
  "result": [
    {
      "jid": <jid>,
      "location": <location>,
      "date": <date>,
      "fully vaccinated estimate": <fully vaccinated estimate>
    }
  ]
}
```

## Setup

























