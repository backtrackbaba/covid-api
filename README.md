# Covid API

# Introduction
This project builds upon the dataset of [John Hopkins University](https://github.com/CSSEGISandData/COVID-19) in CSV form which was converted to JSON Time Series format by [pomber](https://github.com/pomber/covid19).

Our project intends to make that set queryable in a manner in which it could be easily consumed to build public dashboards. 

# Overview
Analyzing the dataset, here are the major points that we came across.

The API's have been mapped to use [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166) standard to query countries instead of names as in the source datasets built upon as it wasn't in a standard format.

The API's consume & return dates as per [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standards in `yyyy-mm-dd` format  The dates have been normalized from the underlying dataset by padding single digits in the date and month section.

# Authentication
There's no authentication required. Anybody and everybody is welcome to use this widely.

# Rate limit
There is no rate limit of any kind but we hope that you use it in a sensible manner and whenever possible cache response for a few hours as the underlying API's are updated ~~thrice a day~~ daily.

# Updation
The datasets are updated ~~thrice a day~~ daily. As of now, we manually trigger the updation of our API's as we don't have any downstream notification's sent on updation. We are also working on having a notification mechanism in place to support all the consumers of the API. PR's are always welcome!

# Documentation
Postman collection has been created along with documentation for you to get started with this project. Docs can be found [here](https://documenter.getpostman.com/view/2568274/SzS8rjbe?version=latest)


# Examples

1) How do I get the global data on any given day?
    
   You could use the [`/api/v1/global/2020-03-15`](https://covidapi.info/api/v1/global/2020-03-15) endpoint

2) How do I get the data for a country in a date-range?

    Ex: To get the data for India between 10th and 19th March 2020, you could use [`/api/v1/country/IND/timeseries/2020-03-10/2020-03-19`](https://covidapi.info/api/v1/country/IND/timeseries/2020-03-10/2020-03-19)

3) How do I get the data for the last record for a country?
    
    Ex: You'll need to get the last date for any country by hitting the [`/api/v1/latest-date`](https://covidapi.info/api/v1/latest-date) endpoint and then use that date to query the country endpoint like this [`/api/v1/country/IND/2020-03-15`](https://covidapi.info/api/v1/country/IND/2020-03-15) 

# Local Setup

### Clone the repo locally
`git clone https://github.com/backtrackbaba/covid-api.git`

### Setup a new Python Environment and source it

Python version 3.6+ would be required to run the project
```
virtualenv -p python3 path/for/environment/covid

source path/for/environment/covid/bin/activate
```

### Set and source the env file
```
cd path/to/cloned/project

# Change the values of env as per your local setup using example.env

source .env
```

### Starting application
```
cd path/to/cloned/project

flask run
```

### Seeding the database
Once the local instance of flask is up and running, you could use the `/protected/update-db` endpoint to start with the seeding of the database

### Updating the database
Same as what you did seeding the database, you'll need to hit the same endpoint to start updating the DB with the latest data

### Debugging

While developing an endpoint, you could remove the cache decorator from the endpoint and enable it once the whole endpoint is up and running. Changes have been made in v2 to ensure this thing is taken care of automatically in local environment.

While hitting any global endpoints which, you might get into `TypeError` which is usually caused when JHU, the data provider changes names of any of the countries in the data or add a name which isn't in the `country_name_to_iso.json` file. You could simply add the same into the file and update the database again


Please open an issue if you get into some other problem and aren't able to figure out why it happened. I'll be glad to discuss any design decisions that you might come across in the code.

# Sources

[Novel Coronavirus (COVID-19) Cases, provided by JHU CSSE](https://github.com/CSSEGISandData/COVID-19)

[JSON time-series of coronavirus cases (confirmed, deaths and recovered) per country - updated daily ](https://github.com/pomber/covid19)

# Contributors

Saiprasad Balasubramanian - [LinkedIn](https://www.linkedin.com/in/saiprasadbala/) - [Github](https://github.com/backtrackbaba)

Harsh Jain - [LinkedIn](https://www.linkedin.com/in/hrkj-18/)

Girisha Navani - [LinkedIn](https://www.linkedin.com/in/girisha-navani-87065215b/)

# Contributing
Contributions are always welcome and encouraged!! This code was whipped out in a very shot span of time for a friend to query on it. There's some refactoring to be done to remove any hacks and build on in a good manner. Ideas are always welcome  

# Roadmap
There's a roadmap in mind to build up more endpoints. As of now there are just two endpoints which with plans to add more. I'll put it out here in the Kanban board as link it with the Issues.

# License
MIT Licensed

