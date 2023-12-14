import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import os

st.title(":blue[In Depth_Analysis of Boston's Parking Spots]")  # title of our new page

st.text("Use the slider to switch between difeerent graphs created from pivot tables\n" \
        "of Boston Parking meter Data. The Pie graph rappresent the percentage of parking\n" \
        "lots that are associated with each vendor. The bar chart is a visual rappresentation\n" \
        "of major streets in Boston (more than 100 parking lots) with the min and max bar\n" \
        "being highlighted. The stacked horizontal bar charts reppresents the 5 major\n" \
        "streets that have at least one MULTI-STALL parking meter and highlights the \n" \
        "breakdown between SINGLE and MULTI-STALL")

filename = "Final_Project_Sumbission/Multipage/pages/Parking_Meters.csv"
indexcol = "OBJECTID"
index_name = "PARKING_ID"
not_needed_columns = ['X', 'Y', 'LOCK_', 'G_SUBZONE', 'G_ZONE', 'G_DISTRICT',
                      'METER_STATE', 'SPACE_STATE', 'NUMBEROFSPACES', 'HAS_SENSOR',
                      'LONGITUDE', 'LATITUDE', 'INSTALLED_ON']  # columns not needed for this page
choices = ["Pie Graph", "Bar Chart", "Stacked Bar Chart"]  # choices for our slider
font_title = {'family': 'garamond',
              'color': 'darkblue',
              'weight': 'normal',
              'size': 16,
              }
font_labels = {'family': 'garamond',
               'color': 'black',
               'weight': 'normal',
               'size': 12,
               }


def read_data_and_rename(index=None, name_of_index=""):  # same function as the page before
    df = pd.read_csv(filename, index_col=index)
    df = df.rename_axis(name_of_index)
    return df


def filter_for_empty_and_useless(df, cols_useless=not_needed_columns):  # same function as the page before
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    total_na_col = df.isnull().sum()
    cols_empty = total_na_col[total_na_col > 50].index.tolist()
    df.drop(columns=cols_empty, inplace=True)
    df.drop(columns=cols_useless, inplace=True)
    return df


def reorder(df):  # same function as the page before
    columns_to_reorder = df[['OBJECTID', 'STREET', 'DIR', 'BLK_NO', 'METER_TYPE', 'BASE_RATE']]
    filter_for_empty_and_useless(df, columns_to_reorder)
    position = 0
    for col in columns_to_reorder:
        df.insert(loc=position, column=col, value=columns_to_reorder[col])
        position += 1
    return df


def min_max(df, column_values):  # function retrieved the maxium and the minimum value from a df's column
    high = df[column_values].max()
    low = df[column_values].min()
    return high, low  # max and min are retrieved


def plotting(pivot_table, value_column,  # plotting function. Main parameters are pivot_table and column values to plot
             type, title,  # type = the type of chart, title = the title for the chart
             y_label=None,  # y_label = label for the y axis if needed
             x_label=None,  # x_label = label for the x acis if needed
             max=None,  # max = maxiumum value of the plotted column if needed
             min=None):  # min = minimum value of the plotted column if needed

    if type == "pie":  # match-case to match the coding needed for each chart type
        pivot_table[value_column].plot(kind=type, figsize=(8, 8),
                                       autopct='%1.1f%%')  # pie chart is plotted with values as a percentage
        plt.title(title, fontdict=font_title)  # title is given
        plt.ylabel(y_label,
                   fontdict=font_labels)  # y_label is given with the default value being none (so it is removed)
    elif type == "bar":  # if a bar chart, then
        plt.figure(figsize=(8, 8))  # size of chart is plotted
        plt.bar(pivot_table.index, pivot_table[value_column],
                color='Blue')  # bar type is plotted with all bars being blue
        if max != None and min != None:  # Used ChatGPT. if max and min are given in the function, then
            plt.bar(pivot_table[pivot_table[value_column] == min].index, min,
                    color='red')  # min value is plotted as red
            plt.bar(pivot_table[pivot_table[value_column] == max].index, max,
                    color='green')  # max vlue is plotted as green
        plt.xticks(rotation=90)  # changes the rotation of the x-axis labels
        plt.title(title, fontdict=font_title)  # plots a title
        plt.xlabel(x_label, fontdict=font_labels)  # plots a x-axis label
        plt.ylabel(y_label, fontdict=font_labels)  # plots a y-axis label
    else:  # if stacked, then
        pivot_table.plot(kind="barh", stacked=True)  # stacked horizontal bar chart is plotted
        plt.title(title, fontdict=font_title)  # title is plotted
        plt.ylabel(y_label, fontdict=font_labels)  # y_label is plotted
        plt.xlabel(x_label, fontdict=font_labels)  # x_label is plotted
    return plt  # the chart is returned


def main():
    chosen = st.select_slider(  # slider code
        'Select a type of graph',  # displayed text
        options=choices)  # choices listed for user

    df = reorder(filter_for_empty_and_useless(
        read_data_and_rename()))  # data frame is created, filtered, and reordered (columns)

    if chosen == "Pie Graph":  # if Pie Graph, then
        pivot_vendors = df.pivot_table(values="OBJECTID", index="VENDOR",
                                       aggfunc="count")  # Pivot Table of the number parking spots for each vendor type will be created
        st.pyplot(plotting(pivot_vendors, "OBJECTID", 'pie',
                           'Major Vendors'))  # everything is plotted and plotted o streamlit

    elif chosen == "Bar Chart":  # if Bar Chart is selected, then
        pivot_streets = df.pivot_table(values="OBJECTID", index="STREET",
                                       aggfunc="count")  # Number of parking lots by street
        pivot_streets = pivot_streets[pivot_streets[
                                          "OBJECTID"] >= 100]  # We are filtering for streets with at least 100 parking lots (since there are a lot of streets)
        pivot_streets = pivot_streets.sort_values(by="OBJECTID",
                                                  ascending=True)  # The major streets (>=100 in parking spots) are sorted in ascending order
        high, low = min_max(pivot_streets,
                            "OBJECTID")  # The street with the highest and the lowest parking spots are retrieved
        st.pyplot(plotting(pivot_streets, "OBJECTID", 'bar', 'Major Streets and amount of Parking Lots',
                           "# of parking spots by Major street",
                           "*A Major Street is defined as having >= 100 parking spots",
                           max=high,
                           min=low,
                           ))  # Pivot table is plotted as a bar chart

    else:  # if Stacked Bar Chart, then
            pivot_meter = df.pivot_table(columns = "METER_TYPE",
                                         index = "STREET",
                                         aggfunc="size", # I used here Chatgpt
                                         fill_value=0) # pivot table displays the number of parking spots per street by meter type
            pivot_meter = pivot_meter[pivot_meter["MULTI-SPACE STALL"]>0] # we are only considering streets with at least a multi-space for our analysis
            pivot_meter["COMBO"] = pivot_meter["MULTI-SPACE STALL"] + pivot_meter["SINGLE-SPACE"] # creating a new column combining the parking spots to a total
            pivot_meter = pivot_meter.sort_values(by = "COMBO", ascending = False) # we are sorting the total in descending order
            pivot_meter = pivot_meter[:5] # retrieving the 5 major streets (by size) with multipace-stalls on them
            pivot_meter = filter_for_empty_and_useless(pivot_meter,"COMBO")
            st.pyplot(plotting(pivot_meter, None,
                               'stacked',
                               '5 Largest Streets by Parking Lot Type',
                               y_label= "Street Name",
                               x_label= '(only streets with at least 1 MULTI_SPACE are considered)'
                               )) # plotting the horizontal and stacked bar chart

main()


