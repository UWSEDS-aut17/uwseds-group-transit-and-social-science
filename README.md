# Improving Public Transportation
<img src="/Images/transittrackers.png" alt="Drawing" height="48" width="48"/>

Our group is primarily concerned with the issues of transportation in the city
of Seattle. With the city growing at an alarming rate, there are inevitably
more and more people on the roads traveling each day. We look at the Puget
Sound Regional Council's (PSRC's) Travel Survey results from 2014 to understand the
travel modes and trends of Seattle residents. Data can be found here:
https://www.psrc.org/household-travel-survey-program

The insights from the PSRC Travel Survey will be cross-referenced with Seattle
public transit data to understand how well the current systems accommodate the
needs of Seattle residents. Four plots are generated, and can all be updated
by zip code selection to group data for the user. An example of the first two
plots are shown in figures 1 and 2, below. The user can visualize bus routes
that serve a specific zip code and the PSRC travel trends from individuals
traveling in the 98133 zip code.

<img src="/Images/routes.png" alt="Drawing" height="60" width="60"/>

Figure 1.

<img src="/Images/trends.png" alt="Drawing" height="72" width="72"/>

Figure 2.

The socioeconomic data is going to be visualized by using the bokeh vbar plot
to show the overall counts of age demographics and education levels by the
chosen zip code. Figures 3 and 4 show examples of these charts for the 98133
zip code.

<img src="/Images/age.png" alt="Drawing" height="84" width="84"/>

Figure 3.

<img src="/Images/edu.png" alt="Drawing" height="96" width="96"/>

Figure 4.

The user runs the analysis by typing in the command line:
"python transittracker.py"
This will output four plots to an html where the user can interact with two
maps and two bar charts for personalized analysis of the data. Running this
code will give an html file saved to the user's local machine, so that they
only have to run the analysis one time and can return to analysis whenever
they would like. From this html, the user can save the plots as separate photos
throughout their analysis whenever they desire.

By better understanding how well the current public transportation system
aligns with the needs of the city, we can then make suggestions as to how it
might be improved. This may involve additional bus lines being added, new
link stations erected in the future, etc. Just as well, we are interested in
how socioeconomic status determines trends of transportation throughout Seattle
and how well served their area is.
