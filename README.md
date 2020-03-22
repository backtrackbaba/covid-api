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
There is no rate limit of any kind but we hope that you use it in a sensible manner and whenever possible cache response for a few hours as the underlying API's are updated thrice a day.

# Updation
The datasets are updated thrice a day. As of now, we manually trigger the updation of our API's as we don't have any downstream notification's sent on updation. We are also working on having a notification mechanism in place to support all the consumers of the API. PR's are always welcome!

# Documentation
Postman collection has been created along with documentation for you to get started with this project. Docs can be found [here](https://documenter.getpostman.com/view/2568274/SzS8rjbe?version=latest)

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

