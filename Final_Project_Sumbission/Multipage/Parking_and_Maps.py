"""
Name: Mario CS230:
Section 2 Data:
Which data set you used URL: Link to your web application on Streamlit Cloud (if posted)
Description: Essentially, the first page of the program, analyzes on a map the Parking spots that are
            present in a specific block (the user can also change the map style).
            The second page, the user can search a specific street and see the number of parking spots that their search
            results in. The parking spots that are listed also include additional information for each one of them.
            The third page is an in depth analysis of the data set. The user can slide between different charts analyzing
            different elements of the datasets. A pie chart for the major parking lot vendors, a bar chart for the number
            of parking spots in each major street, and a stacked horizontal chart for the number of parking spots per street
            by meter-type.

            I have used SOME Chatgpt in order to figure out the syntax of styling certain plots, recall some of the syntax
            covered in this course, and other minor purposes. This sumbission is of my own work.
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import os
st.set_page_config(page_title="Blocks and Maps", page_icon= None) # Setting up the MultiPage
st.title(":blue[Maps, Blocks, and Parking Spots!]") # Title for home page
st.text("Use the dropdown lists below to see current available parking spots in a particular block!\n"\
        "You can also select your preferred map!")
st.sidebar.success("Select a page above.") # Indicate user that he can select different pages

filename = "Final_Project_Sumbission/Multipage/Parking_Meters.csv" # our file
indexcol = "OBJECTID" # our preferred index if we wish to use it
map_style = {'Satellite Streets':'mapbox://styles/mapbox/satellite-streets-v12',
             'Dark Map' : 'mapbox://styles/mapbox/dark-v11',
             'Navigation Day': 'mapbox://styles/mapbox/navigation-day-v1',
             'Navigation Night': 'mapbox://styles/mapbox/navigation-night-v1',
             } # Dict used to store different map styles

def read_data_and_rename(index=None, name_of_index = ""): # function to read the csv and rename it
    df = pd.read_csv(filename, index_col=index) # reading our file (with an index if given)
    df = df.rename_axis(name_of_index) # renames the index (default value is """)
    return df # returns the Pandas data frame ready to go and get analyzed
def longitude_and_latitude(df, style = 'mapbox://styles/mapbox/dark-v11'): # function to map our parking spots
    columns = ["LATITUDE", "LONGITUDE","BLK_NO"] # columns needed to mark parking spots in a specific bloc
    dfLatAndLong = df.loc[:,columns] # a new data frame with only the columns we need
    dfLatAndLong = dfLatAndLong.dropna(subset = columns) # drops null/Na values within these columns
    view_Parking = pdk.ViewState(
        latitude = dfLatAndLong["LATITUDE"].mean(), # centers the view
        longitude = dfLatAndLong["LONGITUDE"].mean(), # centers the view
        zoom=14,
        pitch=0)
    layer1 = pdk.Layer('ScatterplotLayer', # Scatterplot style uses dots
                       data=dfLatAndLong, # our filtered data frame
                       get_position = '[LONGITUDE, LATITUDE]', # position of the parking spots within that block
                       get_radius = 20, # size of marker
                       get_color= [255,165,0], # color of marker
                       pickable = True, # marker is clickable/selectable
                       get_line_color = [0, 0, 0, 255], # color of the border of the marker
                       get_line_width = 5, # width of the border
                       stroked = True, # True to indicate that we would like a border for our markers
                       )
    st.pydeck_chart(pdk.Deck(
        map_style= map_style[style], # our map style is chosen based on what the user selected (style acts as a key)
        initial_view_state= view_Parking, # map
        layers=layer1, # markers
    ))


def main():
    dfParking = read_data_and_rename() # creating our data frame
    drop_down_block = st.selectbox("Filter parking spots in Boston based on a block number:", # Text for dropdown selection
                                   dfParking['BLK_NO'].unique() # possible options that the user can choose (all the unique block values)
                                   )
    filtered_parking = dfParking[dfParking['BLK_NO'] == drop_down_block] # filtering the rows based on the BLK_NO chosen by the user
    drop_down_map = st.selectbox("Select a map style:", # Drop down text
                                 map_style.keys())  # Values that the user can select are the keys to the apis of the map
    longitude_and_latitude(filtered_parking, drop_down_map) # function to plot our map (filtered df by block and chosen map style)

main()

