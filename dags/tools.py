
import pandas as pd
from forcast_day import Forcast_day

from hist_day import Hist_day
from location import Location
import requests
import sys
from datetime import datetime,timedelta,date
import os
import pathlib

from requirements import city    


#This function filter a dictionary from the unnecessary features (variables)
def get_required_features(dictionary,features_liste):
    
    new_dict={key:value for (key,value) in dictionary.items() if get_element_index_liste(key,features_liste)==True} 
    return new_dict

# this Function is to keep only text in the 'condition' feature (condition feature is a dictionary)
def filter_condition(new_dict):
    new_dict['condition']=new_dict['condition']['text']
    return new_dict

def get_element_index_liste(key,liste):
    for i in liste:
        if i==key:
            return True 
    return False

# function for initiating location with all historical data (day) and forecast data (day)
def fill_location_data(location):
    file_name_hist='./city_hist/'+location.name+'.csv'
    file_name_forc='./forcast/'+location.name+'.csv'

    hist_days=[]
    forc_data=[]
    df_hist=pd.read_csv(file_name_hist,sep='\t')
    df_forc=pd.read_csv(file_name_forc,sep='\t')
    for i in range(len(df_hist)):
        hist_days.append(Hist_day(df_hist.iloc[i])) 
    for i in range(len(df_forc)):
        forc_data.append(Forcast_day(df_forc.iloc[i]))     

    location.hist_days=hist_days
    location.forcast_days=forc_data   
   
    return location   
# function for initiating all locations with respective data

def location_fill_liste():
    df=pd.read_csv('locations.csv',sep='\t')
    locs=[]
    for i in range(len(df)):
        loc=Location(df.iloc[i])
        loc=fill_location_data(loc)
        locs.append(loc)
    return locs    


import os
# This function delete all .csv file we used to fill the database

def clear_memory(dir='./city_hist'):
    
    file_liste= os.listdir(dir)
    for file in file_liste:
        os.remove(os.path.join(dir,file))  
       
    return 0    

def trigger_database(locations):
    information=[]
    for loc in locations:
        information.append([loc.name,loc.last_update_day])      # append location (name,last_update_time) we exctract from database 
    return information




def convert_date_to_datetime(date):
    return datetime(date.year,date.month,date.day)


# This function load location information as an argument from previous source 
# information is a list containt [*(name_location,last_updated_date)] 
# and send requestes to get updated data per location  between (last_updated_date and yestearday date)
def extract_updated_data(information):
    Date=datetime.now()-timedelta(days=1) 
    df_location=pd.DataFrame(columns=['name','last_update_day'])
    filter_liste_feature=['date','maxtemp_c','mintemp_c','avgtemp_c','avghumidity','condition']  
    historical='http://api.weatherapi.com/v1/history.json'
    df=pd.DataFrame(columns=filter_liste_feature)
    cle='1d0031473f204204ba005152232406'
    directory='city_hist_updated'
    if get_element_index_liste(directory,os.listdir())==False: 
        path=pathlib.Path().resolve() # Get the current directory path we are working on
        path = os.path.join(path, directory) # Join path and directory for example ('./Desktop'+ '/videos')
        os.mkdir(path) # Create the file if it not already created   
    for location in information:
        print("im here",location[1].year)
        if convert_date_to_datetime(location[1])<Date:
            param={'key': cle ,'q':location[0],'dt':str(location[1]),'end_dt':str(Date)}
            r=requests.get(historical,params=param)
            data=day_data=r.json()["forecast"]['forecastday']
            df_dataframe=Hist_day_per_request_updated(data,filter_liste_feature)
            name='./city_hist_updated/'+location[0]+ '.csv'

            df_location.loc[len(df_location)]=[location[0],df_dataframe.iloc[-1]['date']]
            df_dataframe=df_dataframe.drop(df_dataframe.index[0])
            df_dataframe.to_csv(name, sep='\t', index=False,header=True)
            
        df_location.to_csv('updated_locations.csv', sep='\t', index=False,header=True)





# filter updaded data leaving only the necessary features we require and insert it into a pandas.DataFrame()
    

def Hist_day_per_request_updated(data,filter_liste_feature):
    
    pd_dataframe=pd.DataFrame(columns=filter_liste_feature)
    for day in data:
        new_dict={}
        date=day['date']
        day_data=day['day']
        new_dict=get_required_features(day_data,filter_liste_feature)
        if 'condition' in filter_liste_feature:
            new_dict=filter_condition(new_dict)
        
        pd_dataframe.loc[len(pd_dataframe)]=[date]+list(new_dict.values())

    return pd_dataframe



