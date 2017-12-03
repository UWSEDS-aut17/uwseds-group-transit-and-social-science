#    Python script to process King County GTFS data
import pandas as pd
import os
import zipfile

#    Reading data and making pandas dataframes
#    from PSRC xlsx files
def get_data ():
    households_df = pd.read_excel('C:/Users/ricoshea8/CSE583/Project/uwseds-group-transit-and-social-science/Data/2014-pr3-hhsurvey-households.xlsx')
    persons_df = pd.read_excel('C:/Users/ricoshea8/CSE583/Project/uwseds-group-transit-and-social-science/Data/2014-pr3-hhsurvey-persons.xlsx')
    trips_df = pd.read_excel('C:/Users/ricoshea8/CSE583/Project/uwseds-group-transit-and-social-science/Data/2014-pr3-hhsurvey-trips.xlsx')

#   Extract trips with origin and destination in King County
def extract_trips ():
    king_trips_df = trips_df.loc[(trips_df['ozip'] == 1) & (trips_df['dzip'] == 1)]
    king_households_df = households_df.loc[households_df['hhid'].isin( king_trips_df['hhid'])]
    king_persons_df = persons_df.loc[persons_df['personid'].isin( king_trips_df['personID'])]


#   Function to merge 3 datasets

def merge_data ():
    trips_households_df = king_trips_df.merge(king_households_df, left_on='hhid', right_on='hhid', how='inner')
    all_df = trips_households_df.merge(king_persons_df, left_on='personID', right_on='personid', how='inner')

#   Drop not needed columns
def drop_columns ():
    df = all_df[['recordID','hhid_x','personID','tripID','ocity','ozip','dcity','dzip', 'time_start_mam',
 'time_start_hhmm',
 'time_start_past',
 'time_end_mam',
 'time_end_hhmm',
 'time_end_past',
 'trip_dur_reported',
 'gdist',
 'gtime', 'o_purpose',
 'd_purpose', 'transitsystem1',
 'transitsystem2',
 'transitsystem3',
 'transitsystem4',
 'transitline1',
 'transitline2',
 'transitline3',
 'transitline4', 'triptype', 'hhsize',
 'numadults',
 'numworkers',
 'lifecycle',
 'hh_income_detailed', 'h_city',
 'h_zip', 'age',
 'relationship',
 'gender',
 'employment',
 'worker',
 'student',
 'education',
 'smartphone',
 'transit_freq'
 ]]
    return(df)


def make_useful():
    output_file = "zipplots.html"
    p = figure(plot_width=400, plot_height=400)

    #Count number of zip origins and destinations for heat mapping
    ozip_counts = df['ozip'].value_counts()
    dzip_counts = df['dzip'].value_counts()

    #Get range of income between 0 and 100,000 for heat mapping
    income_range_counts = df.groupby(pd.cut(df['hh_income_detailed'], np.arange(0,200000,20000))).count()

    socio = pd.DataFrame(columns=['h_zip','hh_income_detailed','zone'])
    #Run through and do manual count for incomes in specific h_zips, assign zone
    for i in len(df['tripID']):
        if df.loc['hh_income_detailed',i] >=0 and df.loc['hh_income_detailed',i] < 20000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '1']]
        elif df.loc['hh_income_detailed',i] >=20000 and df.loc['hh_income_detailed',i] < 40000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '2']]
        elif df.loc['hh_income_detailed',i] >=40000 and df.loc['hh_income_detailed',i] < 60000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '3']]
        elif df.loc['hh_income_detailed',i] >=60000 and df.loc['hh_income_detailed',i] < 80000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '4']]
        elif df.loc['hh_income_detailed',i] >=80000 and df.loc['hh_income_detailed',i] < 100000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '5']]
        elif df.loc['hh_income_detailed',i] >=100000 and df.loc['hh_income_detailed',i] < 120000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '6']]
        elif df.loc['hh_income_detailed',i] >=120000 and df.loc['hh_income_detailed',i] < 140000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '7']]
        elif df.loc['hh_income_detailed',i] >=140000 and df.loc['hh_income_detailed',i] < 160000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '8']]
        elif df.loc['hh_income_detailed',i] >=160000 and df.loc['hh_income_detailed',i] < 180000:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '9']]
        else:
            socio.loc[i] = [df.loc['h_zip',i], df.loc['hh_income_detailed',i], '10']]
        return socio

    #Run through zip columns and plot differently based on origin, destination,
    #and home zips. Visualization will then be specific for each
    for i in len(df['tripID']):
        #Should we group these by hour traveled maybe?? To compare to buses
        if df.loc['ozip',i] == df.loc['h_zip',i] and df.loc['dzip',i] == df.loc['h_zip',i]:
            #These are presumably short trips, no bus needed
            p.circle(df.loc['ozip',i], df.loc['dzip',i], fill_color="blue", size=8)
        elif df.loc['ozip',i] == df.loc['h_zip',i]:
            #These refer to how well served their home zip is for trips out
            p.circle(df.loc['ozip',i], df.loc['dzip',i], fill_color="white", size=8)
        elif df.loc['dzip',i] == df.loc['h_zip',i]:
            #These refer to how well served their home zip is for trips in
            p.circle(df.loc['ozip',i], df.loc['dzip',i], fill_color="black", size=8)
        else:
            #These are trips they're taking throughout their day, as a
            #reflection of their work/life community's service via metro
            p.circle(df.loc['ozip',i], df.loc['dzip',i], fill_color="red", size=8)
    return p
