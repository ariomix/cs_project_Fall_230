import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import os


st.title(":blue[Street and Parking Spots Info]") # title of new page
st.text("Use the searchbar to filter for a particular street that you have in mind!\n"\
        "Based on your query, we will give you all the parking spots available and \n"\
        "any relevant info for each one!")
filename = "Final_Project_Sumbission/Multipage/pages/Parking_Meters.csv" # our file
indexcol = "OBJECTID" # our preferred index column if we choose to use it (for this page we will)
index_name = "PARKING_SPOT_#" # our new name that we will give to the index
not_needed_columns = ['X','Y','LOCK_','G_SUBZONE','G_ZONE','G_DISTRICT',
                   'METER_STATE', 'SPACE_STATE','NUMBEROFSPACES','HAS_SENSOR',
                      'LONGITUDE', 'LATITUDE','INSTALLED_ON'] # useless columns that we do not need for the purposes of this page

def read_data_and_rename(index=None, name_of_index = ""): # same as the home page
    df = pd.read_csv(filename, index_col=index)
    df = df.rename_axis(name_of_index)
    return df
def filter_for_empty_and_useless(df,cols_useless = not_needed_columns): # the function cleans our df and elimnates columns (will be used again in the future)
    df.dropna(axis = 1, how = 'all', inplace = True) # Dropped columns with no values whatsoever (i.e., all Nulls)
    df.dropna(axis=0, how='all', inplace=True) # Dropped rows with no values whatsoever
    total_na_col = df.isnull().sum() # used ChatGPT. Sums the number of missing values for each column
    cols_empty = total_na_col[total_na_col > 50].index.tolist() # returns a list of names of all the columns with more than 50 variables missing
    df.drop(columns = cols_empty, inplace= True) # Drops the columns with more than 50 variables missing
    df.drop(columns= cols_useless, inplace=True) # Drops useless columns that we do not need (default values is not_needed columns)
    return df # Returns a clean df and will be used in the future to drop other columns that we do not need
def streets_in_searched_txt(streetname): # function used to filter street rows based on user's text (the parameter for the function is a dataframe)
    condition = False # This will be the default value. If the condition is false the street gets elimnated
    slicing = len(txt) # we are comparing the string of the street value up to the LENGTH of the text inputted by the user
    if txt.lower() in streetname[:slicing].lower(): # if we do not do this, streets that have the text in the middle of their names willbe retrieved
        condition = True # if the text and the street match then the condition is true
    return condition # returns the condition
def reorder(df): # function reorders the columns of our df
    columns_to_reorder = df[['STREET','DIR','BLK_NO','METER_TYPE','BASE_RATE']] # filtering the df for column we want to reorder columns to reorder
    filter_for_empty_and_useless(df,columns_to_reorder) # we are dropping the columns and reinserting them again
    position = 0 # position we like to reinsert them
    for col in columns_to_reorder: # for loop to insert columns one by one. Col is equal to the title of the column
        df.insert(loc = position, column = col, value = columns_to_reorder[col]) # inserting the columns with their respective value
        position += 1 # we add one so that the next column goes right after and not "behind it"
    return df
def sort_and_fix(df): # function used to fix the index when the search is inputted
    sorted_df = df.sort_values(by = "STREET", ascending = True) # sorting the df by ascending
    df_no_index = sorted_df.reset_index(drop=True) # dropping the index due to numbers being incorrect
    df_rename_index = df_no_index.rename_axis('PARKING_SPOT_#') # Renaming he index as Parking_Spot
    df_rename_index.index = df_rename_index.index.map(lambda x: x+1) # fixing the index so that the value does not start with 0
    df_sorted_and_fixed = df_rename_index
    return df_sorted_and_fixed # returns a sorted and fixed (meaning the index) df


txt = st.text_input("To search for a street, please enter the street name here:","") # textbox
df = filter_for_empty_and_useless(read_data_and_rename(indexcol,index_name)) # data frame is created, filtered, and cleaned
df = reorder(df) # dataframe's columns are reordered

if txt != "": # when the user inputs a txt, then the search will be processed
    filtered_df = df[df["STREET"].apply(streets_in_searched_txt)] # applies the streets_in_searched function to the values of STREET
    sorted_filtered_df = sort_and_fix(filtered_df) # the filtered data frame will have the Parking Spot # allover the place so we sort it and fix it
    st.write(f"Your search resulted in {len(sorted_filtered_df)} match(es).")  # number of rows retrieved from search
    st.dataframe(sorted_filtered_df) # filtered and sorted data frame is presented to user
else: # if no text has been inputted
    st.dataframe(df) # default dataframe (cleaned and reordered) is presented.





