import pandas as pd
import os
import zipfile
import numpy as np


def psrc_trip_data():
    households_df = pd.read_excel('C:/Users/tdjor/OneDrive/Documents/Grad School Classes/SoftwareDesign/uwseds-group-transit-and-social-science/Data/2014-pr3-hhsurvey-households.xlsx')
    persons_df = pd.read_excel('C:/Users/tdjor/OneDrive/Documents/Grad School Classes/SoftwareDesign/uwseds-group-transit-and-social-science/Data/2014-pr3-hhsurvey-persons.xlsx')
    trips_df = pd.read_excel('C:/Users/tdjor/OneDrive/Documents/Grad School Classes/SoftwareDesign/uwseds-group-transit-and-social-science/Data/2014-pr3-hhsurvey-trips.xlsx')

    sea_trips_df = trips_df.loc[(trips_df['ocity']== 'SEATTLE') & (trips_df['dcity'] == 'SEATTLE')]
    sea_households_df = households_df.loc[households_df['hhid'].isin(sea_trips_df['hhid'])]
    sea_person_df = persons_df.loc[persons_df['personid'].isin(sea_trips_df['personID'])]

    trips_households_df = sea_trips_df.merge(sea_households_df, left_on = 'hhid', right_on = 'hhid', how = 'inner')
    all_df = trips_households_df.merge(sea_person_df, left_on ='personID', right_on='personid', how = 'inner')

    df = all_df[['ozip', 'dzip']]
    trip_freq = df.groupby(['ozip'])['dzip'].value_counts().to_frame()
    sub = trip_freq.query('dzip > 50')
    sub.to_csv('trip_freq.csv')
    trip_freq2 = pd.read_csv('C:/Users/tdjor/OneDrive/Documents/Grad School Classes/SoftwareDesign/uwseds-group-transit-and-social-science/Data/trip_freq_latlong.csv')

    freq_trip0 = trip_freq2.query('ozip == 98101').reset_index()
    freq_trip0 = freq_trip0[['olat','olon','dlat','dlon']]
    t0_ys = [freq_trip0.loc[0]['olat'],freq_trip0.loc[1]['dlat'],
             freq_trip0.loc[0]['olat'],freq_trip0.loc[2]['dlat'],
             freq_trip0.loc[0]['olat'],freq_trip0.loc[3]['dlat'],
             freq_trip0.loc[0]['olat'],freq_trip0.loc[4]['dlat']]
    t0_xs = [freq_trip0.loc[0]['olon'],freq_trip0.loc[1]['dlon'],
             freq_trip0.loc[0]['olon'],freq_trip0.loc[2]['dlon'],
             freq_trip0.loc[0]['olon'],freq_trip0.loc[3]['dlon'],
             freq_trip0.loc[0]['olon'],freq_trip0.loc[4]['dlon']]

    freq_trip1 = trip_freq2.query('ozip == 98102').reset_index()
    freq_trip1 = freq_trip1[['olat','olon','dlat','dlon']]
    t1_ys = [freq_trip1.loc[0]['olat'],freq_trip1.loc[1]['dlat']]
    t1_xs = [freq_trip1.loc[0]['olon'],freq_trip1.loc[1]['dlon']]

    freq_trip2 = trip_freq2.query('ozip == 98103').reset_index()
    freq_trip2 = freq_trip2[['olat','olon','dlat','dlon']]
    t2_ys = [freq_trip2.loc[0]['olat'],freq_trip2.loc[1]['dlat'],
             freq_trip2.loc[0]['olat'],freq_trip2.loc[2]['dlat'],
             freq_trip2.loc[0]['olat'],freq_trip2.loc[3]['dlat'],
             freq_trip2.loc[0]['olat'],freq_trip2.loc[4]['dlat']]
    t2_xs = [freq_trip2.loc[0]['olon'],freq_trip2.loc[1]['dlon'],
             freq_trip2.loc[0]['olon'],freq_trip2.loc[2]['dlon'],
             freq_trip2.loc[0]['olon'],freq_trip2.loc[3]['dlon'],
             freq_trip2.loc[0]['olon'],freq_trip2.loc[4]['dlon']]

    freq_trip3 = trip_freq2.query('ozip == 98104').reset_index()
    freq_trip3 = freq_trip3[['olat','olon','dlat','dlon']]
    t3_ys = [freq_trip3.loc[0]['olat'],freq_trip3.loc[1]['dlat'],
            freq_trip3.loc[0]['olat'],freq_trip3.loc[2]['dlat']]
    t3_xs = [freq_trip3.loc[0]['olon'],freq_trip3.loc[1]['dlon'],
             freq_trip3.loc[0]['olon'],freq_trip3.loc[2]['dlon']]

    freq_trip4 = trip_freq2.query('ozip == 98105').reset_index()
    freq_trip4 = freq_trip4[['olat','olon','dlat','dlon']]
    t4_ys = [freq_trip4.loc[0]['olat'],freq_trip4.loc[1]['dlat'],
             freq_trip4.loc[0]['olat'],freq_trip4.loc[2]['dlat'],
             freq_trip4.loc[0]['olat'],freq_trip4.loc[3]['dlat']]
    t4_xs = [freq_trip4.loc[0]['olon'],freq_trip4.loc[1]['dlon'],
             freq_trip4.loc[0]['olon'],freq_trip4.loc[2]['dlon'],
             freq_trip4.loc[0]['olon'],freq_trip4.loc[3]['dlon']]

    freq_trip5 = trip_freq2.query('ozip == 98106').reset_index()
    freq_trip5 = freq_trip5[['olat','olon','dlat','dlon']]
    t5_ys = [freq_trip5.loc[0]['olat'],freq_trip5.loc[0]['dlat']]
    t5_xs = [freq_trip5.loc[0]['olon'],freq_trip5.loc[0]['dlon']]

    freq_trip6 = trip_freq2.query('ozip == 98107').reset_index()
    freq_trip6 = freq_trip6[['olat','olon','dlat','dlon']]
    t6_ys = [freq_trip6.loc[0]['olat'],freq_trip6.loc[1]['dlat'],
             freq_trip6.loc[0]['olat'],freq_trip6.loc[2]['dlat'],
             freq_trip6.loc[0]['olat'],freq_trip6.loc[3]['dlat']]
    t6_xs = [freq_trip6.loc[0]['olon'],freq_trip6.loc[1]['dlon'],
             freq_trip6.loc[0]['olon'],freq_trip6.loc[2]['dlon'],
             freq_trip6.loc[0]['olon'],freq_trip6.loc[3]['dlon']]

    freq_trip7 = trip_freq2.query('ozip == 98108').reset_index()
    freq_trip7 = freq_trip7[['olat','olon','dlat','dlon']]
    t7_ys = [freq_trip7.loc[0]['olat'],freq_trip7.loc[0]['dlat']]
    t7_xs = [freq_trip7.loc[0]['olon'],freq_trip7.loc[0]['dlon']]

    freq_trip8 = trip_freq2.query('ozip == 98109').reset_index()
    freq_trip8 = freq_trip8[['olat','olon','dlat','dlon']]
    t8_ys = [freq_trip8.loc[0]['olat'],freq_trip8.loc[1]['dlat'],
             freq_trip8.loc[0]['olat'],freq_trip8.loc[2]['dlat'],
             freq_trip8.loc[0]['olat'],freq_trip8.loc[3]['dlat'],
             freq_trip8.loc[0]['olat'],freq_trip8.loc[4]['dlat']]
    t8_xs = [freq_trip8.loc[0]['olon'],freq_trip8.loc[1]['dlon'],
             freq_trip8.loc[0]['olon'],freq_trip8.loc[2]['dlon'],
             freq_trip8.loc[0]['olon'],freq_trip8.loc[3]['dlon'],
             freq_trip8.loc[0]['olon'],freq_trip8.loc[4]['dlon']]

    freq_trip9 = trip_freq2.query('ozip == 98112').reset_index()
    freq_trip9 = freq_trip9[['olat','olon','dlat','dlon']]
    t9_ys = [freq_trip9.loc[0]['olat'],freq_trip9.loc[1]['dlat'],
             freq_trip9.loc[0]['olat'],freq_trip9.loc[2]['dlat']]
    t9_xs = [freq_trip9.loc[0]['olon'],freq_trip9.loc[1]['dlon'],
             freq_trip9.loc[0]['olon'],freq_trip9.loc[2]['dlon']]

    freq_trip10 = trip_freq2.query('ozip == 98115').reset_index()
    freq_trip10 = freq_trip10[['olat','olon','dlat','dlon']]
    t10_ys = [freq_trip10.loc[0]['olat'],freq_trip10.loc[1]['dlat'],
              freq_trip10.loc[0]['olat'],freq_trip10.loc[2]['dlat'],
              freq_trip10.loc[0]['olat'],freq_trip10.loc[3]['dlat']]
    t10_xs = [freq_trip10.loc[0]['olon'],freq_trip10.loc[1]['dlon'],
              freq_trip10.loc[0]['olon'],freq_trip10.loc[2]['dlon'],
              freq_trip10.loc[0]['olon'],freq_trip10.loc[3]['dlon']]

    freq_trip11 = trip_freq2.query('ozip == 98116').reset_index()
    freq_trip11 = freq_trip11[['olat','olon','dlat','dlon']]
    t11_ys = [freq_trip11.loc[0]['olat'],freq_trip11.loc[0]['dlat']]
    t11_xs = [freq_trip11.loc[0]['olon'],freq_trip11.loc[0]['dlon']]

    freq_trip12 = trip_freq2.query('ozip == 98117').reset_index()
    freq_trip12 = freq_trip12[['olat','olon','dlat','dlon']]
    t12_ys = [freq_trip12.loc[0]['olat'],freq_trip12.loc[1]['dlat'],
              freq_trip12.loc[0]['olat'],freq_trip12.loc[2]['dlat']]
    t12_xs = [freq_trip12.loc[0]['olon'],freq_trip12.loc[1]['dlon'],
              freq_trip12.loc[0]['olon'],freq_trip12.loc[2]['dlon']]

    freq_trip13 = trip_freq2.query('ozip == 98118').reset_index()
    freq_trip13 = freq_trip13[['olat','olon','dlat','dlon']]
    t13_ys = [freq_trip13.loc[0]['olat'],freq_trip13.loc[0]['dlat']]
    t13_xs = [freq_trip13.loc[0]['olon'],freq_trip13.loc[0]['dlon']]

    freq_trip14 = trip_freq2.query('ozip == 98119').reset_index()
    freq_trip14 = freq_trip14[['olat','olon','dlat','dlon']]
    t14_ys = [freq_trip14.loc[0]['olat'],freq_trip14.loc[1]['dlat']]
    t14_xs = [freq_trip14.loc[0]['olon'],freq_trip14.loc[1]['dlon']]

    freq_trip15 = trip_freq2.query('ozip == 98121').reset_index()
    freq_trip15 = freq_trip15[['olat','olon','dlat','dlon']]
    t15_ys = [freq_trip15.loc[0]['olat'],freq_trip15.loc[1]['dlat'],
              freq_trip15.loc[0]['olat'],freq_trip15.loc[2]['dlat']]
    t15_xs = [freq_trip15.loc[0]['olon'],freq_trip15.loc[1]['dlon'],
              freq_trip15.loc[0]['olon'],freq_trip15.loc[2]['dlon']]

    freq_trip16 = trip_freq2.query('ozip == 98122').reset_index()
    freq_trip16 = freq_trip16[['olat','olon','dlat','dlon']]
    t16_ys = [freq_trip16.loc[0]['olat'],freq_trip16.loc[1]['dlat'],
              freq_trip16.loc[0]['olat'],freq_trip16.loc[2]['dlat'],
              freq_trip16.loc[0]['olat'],freq_trip16.loc[3]['dlat'],
              freq_trip16.loc[0]['olat'],freq_trip16.loc[4]['dlat'],
              freq_trip16.loc[0]['olat'],freq_trip16.loc[5]['dlat']]
    t16_xs = [freq_trip16.loc[0]['olon'],freq_trip16.loc[1]['dlon'],
              freq_trip16.loc[0]['olon'],freq_trip16.loc[2]['dlon'],
              freq_trip16.loc[0]['olon'],freq_trip16.loc[3]['dlon'],
              freq_trip16.loc[0]['olon'],freq_trip16.loc[4]['dlon'],
              freq_trip16.loc[0]['olon'],freq_trip16.loc[5]['dlon']]

    freq_trip17 = trip_freq2.query('ozip == 98125').reset_index()
    freq_trip17 = freq_trip17[['olat','olon','dlat','dlon']]
    t17_ys = [freq_trip17.loc[0]['olat'],freq_trip17.loc[1]['dlat']]
    t17_xs = [freq_trip17.loc[0]['olon'],freq_trip17.loc[1]['dlon']]

    freq_trip18 = trip_freq2.query('ozip == 98126').reset_index()
    freq_trip18 = freq_trip18[['olat','olon','dlat','dlon']]
    t18_ys = [freq_trip18.loc[0]['olat'],freq_trip18.loc[1]['dlat']]
    t18_xs = [freq_trip18.loc[0]['olon'],freq_trip18.loc[1]['dlon']]

    freq_trip19 = trip_freq2.query('ozip == 98133').reset_index()
    freq_trip19 = freq_trip19[['olat','olon','dlat','dlon']]
    t19_ys = [freq_trip19.loc[0]['olat'],freq_trip19.loc[0]['dlat']]
    t19_xs = [freq_trip19.loc[0]['olon'],freq_trip19.loc[0]['dlon']]

    freq_trip20 = trip_freq2.query('ozip == 98136').reset_index()
    freq_trip20 = freq_trip20[['olat','olon','dlat','dlon']]
    t20_ys = [freq_trip20.loc[0]['olat'],freq_trip20.loc[0]['dlat']]
    t20_xs = [freq_trip20.loc[0]['olon'],freq_trip20.loc[0]['dlon']]

    freq_trip21 = trip_freq2.query('ozip == 98144').reset_index()
    freq_trip21 = freq_trip21[['olat','olon','dlat','dlon']]
    t21_ys = [freq_trip21.loc[0]['olat'],freq_trip21.loc[1]['dlat']]
    t21_xs = [freq_trip21.loc[0]['olon'],freq_trip21.loc[1]['dlon']]

    freq_trip22 = trip_freq2.query('ozip == 98195').reset_index()
    freq_trip22 = freq_trip22[['olat','olon','dlat','dlon']]
    t22_ys = [freq_trip22.loc[0]['olat'],freq_trip22.loc[0]['dlat']]
    t22_xs = [freq_trip22.loc[0]['olon'],freq_trip22.loc[0]['dlon']]

    freq_trip23 = trip_freq2.query('ozip == 98199').reset_index()
    freq_trip23 = freq_trip23[['olat','olon','dlat','dlon']]
    t23_ys = [freq_trip23.loc[0]['olat'],freq_trip23.loc[0]['dlat']]
    t23_xs = [freq_trip23.loc[0]['olon'],freq_trip23.loc[0]['dlon']]

    used_zips = ['98101','98102','98103','98104','98105','98106','98107',
            '98108','98109','98112','98115','98116','98117','98118',
             '98119','98121','98122','98125','98126','98133','98136',
             '98144','98195','98199']
