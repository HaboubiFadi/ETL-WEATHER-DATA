import requests
import sys

import pandas as pd
from datetime import datetime  
from datetime import timedelta  
from requirements import city




import os
import pathlib
# get if element exist in liste ,
# this function could be replaced with a more optimized version 
def get_element_index_liste(key,liste):
    for i in liste:
        if i==key:
            return True 
    return False
#This function filter a dictionary from the unnecessary features (variables)
def get_required_features(dictionary,features_liste):
    
    new_dict={key:value for (key,value) in dictionary.items() if get_element_index_liste(key,features_liste)==True} 
    return new_dict

# this Function is to keep only text in the 'condition' feature (condition feature is a dictionary)
def filter_condition(new_dict):
    new_dict['condition']=new_dict['condition']['text']
    return new_dict


# filter json_data leaving only the necessary features we require and insert it into a pandas.DataFrame()
def current_data_pd_per_request(data,filter_liste_feature,pd_dataframe):
    new_dict=get_required_features(data,filter_liste_feature)
    if 'condition' in filter_liste_feature:
            new_dict=filter_condition(new_dict)
    pd_dataframe.loc[len(pd_dataframe)]=list(new_dict.values())
    return pd_dataframe
    
    
    
# extract and Transform the data(json) and create pandas.DataFrame() variable 

def create_current_data_pd_total(location_df,begin=datetime.now(),city='London'):
    filter_liste_feature=['last_updated','temp_c','condition','humidity'] # filter_variable (only keep those features)
    historical='http://api.weatherapi.com/v1/current.json'
    df=pd.DataFrame(columns=filter_liste_feature)
    
    
    cle='1d0031473f204204ba005152232406'
    param={'key': cle ,'q':city}
    r=requests.get(historical,params=param)
    data=day_data=r.json()["current"] # get the current data from the requeted data(json)
    df=current_data_pd_per_request(data,filter_liste_feature,df) # filter current_data
    
    
    filter_location=['name','country','lat','lon'] # filter for location (keep only necessary features for the location variable)
    location=r.json()['location']
    location=get_required_features(location,filter_location)

    location_df.loc[len(location_df)]=list(location.values())+[df.iloc[len(df)-1]['last_updated']]

    

    return df,location_df

# use the created pandas.Dataframe() in the 'create_current_data_pd_total' function to save it into a '.csv' file 
def save_current_pd_csv(directory='current'):
   
    

    location_df=pd.DataFrame(columns=['name','country','lat','lon','last_update_day'])
    if get_element_index_liste(directory,os.listdir())==False: # create the necessary directory if it doesn't exist alerady
        path=pathlib.Path().resolve()
        path = os.path.join(path, directory)
        os.mkdir(path)
    for c in city:
        print(c)
        df,location_df=create_current_data_pd_total(location_df,city=c)
        name='./'+directory+'/'+location_df.iloc[-1]['name']+ '.csv'
        df.to_csv(name, sep='\t', index=False,header=True) # save the pd.DataFrame into csv files 



