# Component Design

* Component list
  - Database of public transportation routes and stops by location
  - Database of socioeconomic and trips by location
  - Map of routes and stops
  - Visualization of socioeconomic data through graph and heatmap

* Component specifications
  - Database of public transportation routes and stops by location
    - What it does
       - Takes a location from the map and creates dataframes that contains what buses routes and stops
         are closest and the path of the bus route
    - Name
       - gtfs_utils.py
    - Inputs
       - Census tracked location as specified by click on map
    - Outputs
       - Dataframes of bus route paths, stop locations and information about bus stop frequency
    - Pseudo code
       - get_busdata(census_track_id)
         using latitutde and longitude data, find bus route ids within that census track
         use bus route ids to determine stop locations (lat, long)
         use bus route ids to determine bus route path (lat, long)
         group all lat and long data into a dataframe that is the output


  - b
    - What it does
      - insert here
    - Name
      - insert here
    - Inputs
      - insert here
    - Outputs
      - insert here
    - Pseudo code
      - insert here

  - c
    - What it does
      - insert here
    - Name
      - insert here
    - Inputs
      - insert here
    - Outputs
      - insert here
    - Pseudo code
      - insert here

  - d
    - What it does
      - insert here
    - Name
      - insert here
    - Inputs
      - insert here
    - Outputs
      - insert here
    - Pseudo code
      - insert here

