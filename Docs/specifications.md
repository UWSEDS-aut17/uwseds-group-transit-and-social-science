# Problem Statement
How well does Seattle public transit meet the needs of Seattle residents?

# User Profile
* User computational environments:
    - The user will use the webpage to view the interactive mapping
    - The user will have general understanding of the transit system
    - The user will run the code on command line "python transit_tracker.py"
* User's knowledge of the problem statement:
    - The user will have less knowledge of the relationship between
      socioeconomic behavior and transit system

# Elements of Problem Statement

What are current transit trends within Seattle?
* What are high trend areas of travel by zip code?
* How do transit trends depend on socioeconomic factors?

Does the public transportation system align with the current transit trends?
* Are there dead zones in which public transit doesn't travel?
* Can Seattle public transit be improved to better meet the needs of Seattle
  residents?
* Are there transit routes that are not heavily used that can be removed to
  optimize route & time?

# Use Cases

* Point-and-Click interactive map on a webpage
    - After user types 'python transit_tracker.py' the software will download
      and process the data, and output 4 plots to an html and saves that html
      file to the local disk
    - The user can start their analysis immediately, or access the data through
      the generated html file later on
    - User first clicks on a zip code (via checkbox) on the bus route map to
      define a specific area that they are interested in analyzing, or can hover
      over the map to view zip codes and then decide which to analyze
    - User then clicks the same zip code in a checkbox related to the PSRC
      travel survey data to show the trends of trips taken from individuals
      from that home zip code
    - From here, the user can continue to interact and change zip code locations
      on these maps, as well as include multiple zip codes to view changes or
      differences between regions of interest
* Zip code-based data grouping and visualization
    - The user can use the dropdown menu for the data grouping plots (bar
      charts) and choose the same zip code(s) as above to analyze the
      socioeconomic data available from the PSRC survey for that region
* Save Figures Individually
    - These plots can all be saved to the local disk from a single save button
      that the user can find and click at the top of the html
