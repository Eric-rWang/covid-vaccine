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
  "id": "0d3bac54-0988-4d61-a1e2-d971e4c282e8",
  "time": "2021-05-06 10:22:10.991988-05:00",
  "status": "submitted",
  "task": "load_data",
  "job_input": "none",
  "pod_ip": "not_set"
}
```

Basic CRUD opperations can be performed with the following commands.

### Create a data entry
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

### Read the data
```
$ curl -X GET <flask_ip>:5000/view_data
```
Returns vaccine data stored in the database.

### Update the data
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

## Setup



