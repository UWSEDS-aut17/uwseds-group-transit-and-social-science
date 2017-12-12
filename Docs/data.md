# Requirements

Traffic data:
-Traffic on routes
-Travel time
-Rush hour delays


Public transit data:
-Buses and Link routes

Passengers trips data:
-Origins and destinations of the trips by starting zip code

Passengers socioeconomic data:
-Income
-Education
-Home neighborhood

# Sources
List all data sets we are planning to use:

https://www.psrc.org/household-travel-survey-program

This data set has census tracked transit data. That tells us the mode of
transit, the socio-economic status of the traveler, the distance and location of
travel, and mode of transportation.

https://stackoverflow.com/questions/4600656/access-googles-traffic-data-through-a-web-service

This link is a stackoverflow on how to get access to traffic data from Google
maps. This will be beneficial in determining high traffic areas in Seattle and
how those change with time of day, etc.

https://www.soundtransit.org/Developer-resources/Data-downloads

This link contains General Transit Feed Specifications for Sound Transit that
is used to make the one bus away app. It contains bus routes, schedules, etc.
This will give us a way to visualize the current public bus system and overlay
it with a map of high transit locations throughout Seattle.

All of these data sets are open for use.

# Evaluation
Analyze data choices

| Requirements\Data    | Census Tracked Data | Stackoverflow | General Public Data |
|:--------------------:|:-------------------:|:-------------:|:--------------------:|
| Traffic Data         | Provide general traffic data | Provide mapping of traffic | Provide connection between general public and traffic |
| Public transit data  | This public transit data contains public transit data | Provide mapping for public transit | Provide connection of how general public use public transit |
| Passengers trip data | Provide the route/time of a passenger | Provide mapping for passenger trip |Provide connection between general public and passenger trip data |
| Socioeconomic         | Provide socioeconomic data | Provide mapping between passengers and socioeconomic behavior | Provide connection between general public and socioeconomic behavior |
