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

  - Map of routes and stops
    - What it does
      - This component will be used to visualize current transit trend data in King
      County so that it can be compared with PSRC survey data.
      It will serve as the base metric for all of our analysis by understanding what
      areas are over-or-underserved with the current implementations.
    - Name
      - gtfs_utils.py
    - Inputs
      - OneBusAway DataFrames for stops, trips, shapes, and routes. Columns involve
      specific IDs that relate to that specific DF, and also correlate to the other
      DFs for reference.
      - Map with zip code outlines for visualization.
    - Outputs
      - An interactive map that will be updated based on the inputs from the user.
    - How it works
      - Get all route, stop, trip, and shape data from the OneBusAway DataFrames.
      - Create a map with zip code differentiation that can be used to overlay the
      bus data.
      - Add the OneBusAway data and group by the location of interest
      - With grouping in pandas we should be able to interactively update the map
      based on the user inputs.

  - Visualization of the socioeconomic data through graph and heatmap
    - What it does
      - Visualization of the socioeconomic data through graph and heatmap. The user will be able to easily view the socioeconomic behavior by regions
    - Name
      - SocioVis.py
    - Inputs
      - The user will either click on the region or type in the zipcode. 
    - Outputs
      - Once a region is clicked, a small table/box will appear next to the region with the socioeconomic information. The outputs will include household income, age, marriage status, highest education, number of family members, employment status, etc
    - How it works
      - The map of the Kings county will be divided into regions and the user can click on the regions that will pop up a table/box of socioeconomic behaviors. 
      - Group the socioeconomic behavior by regions
