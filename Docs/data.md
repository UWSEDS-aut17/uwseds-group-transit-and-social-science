# Requirements

Traffic data:
-Traffic on routes
-Travel time
-Rush hour delays


Public transit data: 
-Buses and Link routes
-Buses and Link stops location
-Fares

Passengers trips data:
-Origins and destinations of the trips
-Mode of trip
-Purpose of trip
-Time of trip

Passengers socioeconomic data:
-Income
-Education
-Number of family members
-Home neighborhood
-Ethnicity

# Sources
List all data sets we are planning to use:

https://www.psrc.org/household-travel-survey-program

This data set has census tracked tansit data. That tells us the mode of transit, the socio-economic status of 
the traveller, the distance and location of travel, and mode of transportation.

https://stackoverflow.com/questions/4600656/access-googles-traffic-data-through-a-web-service

This link is a stackoverflow on how to get access to traffic data from Google maps. This will be benefitial in 
determining high traffic areas in Seattle and how those change with time of day, etc.

https://www.soundtransit.org/Developer-resources/Data-downloads

This link contains General Transit Feed Specifications for Sound Transit that is used to make the one bus 
away app. It contains bus routes, schedules, etc. This will give us a way to visualize the current public bus 
system and overlay it with a map of high transit locations throughout Seattle.

All of these data set are open for use. 

# Evaluation
Analyze data choices

| Requirements\Data    | Census Tracked Data | Stackoverflow | Gerneral Public Data |
|:--------------------:|:-------------------:|:-------------:|:--------------------:|
| Traffic Data         | Provide general traffic data | Provide mapping of traffic | Provide connection between general public and traaffic | 
| Public transit data  | This public transit data contains public transit data | Provide mapping for public transit | Provide connetion of how general public use public transit |
| Passengers trip data | Provide the route/time of a passenger | Provide maping for passnger trip |Provide coneection between general public and passenger trip data |
| Socioeconmic         | Provide socioeconomic data | Provide mapping between passengers and socioeconmic behavior | Provide connection between general public and socioeconmic behavior |
