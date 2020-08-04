# Introduction

![](https://github.com/Manvityagi/Atlan-Challenge---Long-Running-Task-Manager/blob/master/images/start.PNG)

**Task State Manager** is an implementation of an upload/download system in which the functionality of pausing/resuming/terminating the task at hand is poosible.

## ❓ Problem Statement

- We want to offer an implementation through which the user can stop the long-running task at any given point in time, and can choose to resume or terminate it. This will ensure that the resources like compute/memory/storage/time are used efficiently at our end, and do not go into processing tasks that have already been stopped (and then to roll back the work done post the stop-action)

## 🚧 Technology Stack

- **Framework** - Django Rest Framework
- **Database** - PostgreSQL
- **Python** - version 3.8.2

# 💡 Approach

### Upload

- A dummy CSV file is read using pandas and added row by row to a table in database.
  #### Pause
  Number of lines read are constantly being recorded, when paused an Interrupt Exception is raised which stops the upload.
  #### Resume
  The upload start funtion is called again but this time the CSV file is read from the checkpoint that we stored earlier.
  ### Terminate
  In this situation, the application needed to get back to the work done before this wrong upload started, so I dropped this particular table.
  ### Progress
  Some basic maths is being used to calculate the percentage of upload completed.

### Download/Export

- A database tabke from the server can be exported as a CSV file.
  #### Pause
  Number of lines read are constantly being recorded, when paused an Interrupt Exception is raised which stops the export.
  #### Resume
  The download start funtion is called again but this time the database table is read from the checkpoint that we stored earlier.
  ### Terminate
  In this situation, the application needed to get back to the work done before this wrong upload started, so I removed the exported CSV file.
  ### Progress
  Some basic maths is being used to calculate the percentage of download completed.

## 🔨 Features

- `Upload a CSV File` A dummy CSV file can be uploaded to the server.
- `Download/Export` Any database table can be exported as a CSV file.
  Following features are available in both upload/downlaod.
- `Pause` Pauses the upload/downlaod.
- `Resume` Resumes the upload/downlaod.
- `Terminate` Terminates/Rollbacks the upload/downlaod.

## 🔨 API Endpoints

| REQUEST METHODS |      ENDPOINTS      |                                       DESCRIPTION |
| :-------------- | :-----------------: | ------------------------------------------------: |
| POST            |    /upload/start    |                      Start uploading the CSV File |
| POST            |    /upload/pause    |                                  Pause the upload |
| POST            |   /upload/resume    |                                 Resume the upload |
| POST            |  /upload/terminate  |                              Terminate the upload |
| GET             |  /upload/progress   |               Get the percntage upload completion |
| POST            |   /download/start   | Start downloading/exporting from DB into CSV file |
| POST            |   /download/pause   |                                Pause the download |
| POST            |  /download/resume   |                               Resume the download |
| POST            | /download/terminate |                            Terminate the download |
| GET             | /download/progress  |             Get the percntage download completion |

## [VIEW API DOCUMENTATION](https://documenter.getpostman.com/view/6209199/T1DwbYtX?version=latest)

## ⬇️ Installation and Run with docker

```
# clone the repository to your local machine
$ git clone https://github.com/Manvityagi/Atlan-Challenge---Long-Running-Task-Manager.git

# navigate to the project's directory and install all the relevant dev-dependencies
$ cd Atlan-Challenge---Long-Running-Task-Manager && pip install requirements.txt

# Run
$ docker-compose up -d --build

# Then Run
$ docker-compose exec web python ./runningTask/manage.py migrate
```

## ⬇️ Installation on local host

```
# clone the repository to your local machine
$ git clone https://github.com/Manvityagi/Atlan-Challenge---Long-Running-Task-Manager.git

# navigate to the project's directory and install all the relevant dev-dependencies
$ cd Atlan-Challenge---Long-Running-Task-Manager && pip install

# Start application
$ python manage.py runserver

# Visit http://127.0.0.1:8000/ in your browser
```

## Demo Images

![](https://github.com/Manvityagi/Atlan-Challenge---Long-Running-Task-Manager/blob/master/images/demo%60.PNG)
![](https://github.com/Manvityagi/Atlan-Challenge---Long-Running-Task-Manager/blob/master/images/demo2.PNG)
![](https://github.com/Manvityagi/Atlan-Challenge---Long-Running-Task-Manager/blob/master/images/demo3.PNG)
