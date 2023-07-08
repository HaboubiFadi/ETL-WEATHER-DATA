import requests
import sys

import pandas as pd
from datetime import datetime  
from datetime import timedelta  
from requirements import city

def get_element_index_liste(key,liste):
    for i in liste:
        if i==key:
            return True 
    return False
#This function filter a dictionary from the unnecessary features (variables)
def get_required_features(dictionary,features_liste):
    
    new_dict={key:value for (key,value) in dictionary.items() if get_element_index_liste(key,features_liste)==True} 
    return new_dict

filter_liste_feature=['maxtemp_c','mintemp_c','avgtemp_c','avghumidity','condition']  
# this Function is to keep only text in the 'condition' feature (condition feature is a dictionary)
def filter_condition(new_dict):
    new_dict['condition']=new_dict['condition']['text']
    return new_dict


# filter json_data leaving only the necessary features we require

def forcast_data_pd_per_request(data,filter_liste_feature,pd_dataframe):
    for day in data:
        new_dict={}
        date=day['date']
        day_data=day['day']
        new_dict=get_required_features(day_data,filter_liste_feature)
        if 'condition' in filter_liste_feature:
            new_dict=filter_condition(new_dict)
        
        pd_dataframe.loc[len(pd_dataframe)]=[date]+list(new_dict.values())

    return pd_dataframe
# extract and Transform the data(json) and create pandas.DataFrame() variable 

def create_forcast_data_pd_total(location_df,begin=datetime.now(),city='London'):
    filter_liste_feature=['date','maxtemp_c','mintemp_c','avgtemp_c','avghumidity','condition']  
    historical='http://api.weatherapi.com/v1/forecast.json'
    df=pd.DataFrame(columns=filter_liste_feature)
    
    
    cle='1d0031473f204204ba005152232406'
    param={'key': cle ,'q':city,'Days':14}
    r=requests.get(historical,params=param)
    data=day_data=r.json()["forecast"]['forecastday']
    df=forcast_data_pd_per_request(data,filter_liste_feature,df)
    
    
    filter_location=['name','country','lat','lon']
    location=r.json()['location']
    location=get_required_features(location,filter_location)
    # delete replication from df
    df=df.drop_duplicates(subset=['date'])
    # drop rows where lastrow['date']>yesterday date 
    location_df.loc[len(location_df)]=list(location.values())+[df.iloc[len(df)-1]['date']]


    

    return df,location_df



"""df=create_hist_day_data_pd_total()
print(df.tail(),df.shape)

df=df.drop_duplicates(subset=['date'])
print(df.tail(),df.shape)"""
import os
import pathlib
# use the created pandas.Dataframe() in the 'create_current_data_pd_total' function to save it into a '.csv' file 

def save_forcastas_pd_csv(directory='forcast'):

    location_df=pd.DataFrame(columns=['name','country','lat','lon','last_update_day'])
    if get_element_index_liste(directory,os.listdir())==False: 
        path=pathlib.Path().resolve()
        path = os.path.join(path, directory)
        os.mkdir(path)
    for c in city:
        df,location_df=create_forcast_data_pd_total(location_df,city=c)
        name='./'+directory+'/'+location_df.iloc[-1]['name']+ '.csv'
        df.to_csv(name, sep='\t', index=False,header=True)







