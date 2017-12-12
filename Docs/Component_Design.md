# Component Design

* Component list
  - Database of public transportation routes
  - Database of socioeconomic factors and trips
  - Map of routes and travel trends
  - Visualization of socioeconomic data through bar charts

* Component specifications
  - Database of public transportation routes
    - What it does
       - Takes a zip code and creates dataframes that contain what bus routes
         serve that zip code and shows the path of the bus route
    - Name
       - Processing and plotting run in transittrackers.py
    - Inputs
       - Routes from KCM for Seattle specific routes
       - Zip Codes in Seattle
    - Outputs
       - Dataframes of bus route paths


  - Database of socioeconomic factors and trips
    - What it does
        - Present socioeconomic information and trip trends for a zip code,
          selected by the user.
    - Name
        - Processing and plotting run in transittrackers.py
    - Inputs
        - Data from PSRC travel survey
        - Zip Codes in Seattle
    - Outputs
        - Dataframes of travel trends from each zip code, and grouped
          socieoeconomic data by zip code.		  

  - Map of routes and travel trends
    - What it does
      - This component will be used to visualize current transit trend data in
        Seattle so that it can be compared with PSRC survey data.
        It will serve as the base metric for all of our analysis by
        understanding what areas are over-or-underserved with the current
        implementations.
    - Name
      - Processing and plotting run in transitrackers.py
    - Inputs
      - OneBusAway DataFrames for route shapes and routes. Columns involve
      specific IDs that relate to that specific DF, and also correlate to the
      other DFs for reference.
      - Map with zip code outlines for visualization.
    - Outputs
      - An interactive map that will be updated based on the zip code choices
        from the user.
    - How it works
      - Get all route, stop, trip, and shape data from the OneBusAway
      - Create a map with zip code differentiation that can be used to compare
        to the bus data.
      - Add the OneBusAway data and group by the location of interest

  - Visualization of the socioeconomic data through bar charts
    - What it does
      - Visualization of the socioeconomic data through bar graphs
      The user will be able to easily view the socioeconomic factors by regions
    - Name
      - Processing and plotting run in transittrackers.py
    - Inputs
      - The user will click on the zip code
    - Outputs
      - The outputs will include age and highest education dataframes
    - How it works
      - Selection box used to choose zip code and a plot will pop up
      - Group the socioeconomic behavior by zip code
