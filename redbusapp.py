#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Importing libraries
import pandas as pd
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px

# Function to load route names from CSV
def load_route_names(file_path):
    df = pd.read_csv(file_path)
    return df["Route_name"].tolist()

# Loading bus route names
lists_k = load_route_names("df_k.csv")  # Kerala bus
lists_A = load_route_names("df_a.csv")  # Andhra bus
lists_T = load_route_names("df_T.csv")  # Telangana bus
lists_g = load_route_names("df_G.csv")  # Goa bus
lists_R = load_route_names("df_R.csv")  # Rajasthan bus
lists_Ch = load_route_names("df_ch.csv")  # South Bengal bus
lists_H = load_route_names("df_H.csv")  # Haryana bus
lists_AS = load_route_names("df_AS.csv")  # Assam bus
lists_UP = load_route_names("df_UP.csv")  # UP bus
lists_WB = load_route_names("df_WB.csv")  # West Bengal bus

#setting up streamlit page
slt.set_page_config(layout="wide")

web=option_menu(menu_title="🚌OnlineBus",
                options=["Home","📍States and Routes"],
                icons=["house","info-circle"],
                orientation="horizontal"
                )

if web=="Home":
    slt.image("t_500x300.jpg",width=200)
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    slt.subheader(":blue[Domain:]  Transportation")
    slt.subheader(":blue[Ojective:] ")
    slt.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
    slt.subheader(":blue[Overview:]") 
    slt.markdown("Selenium: Selenium is a tool used for automating web browsers. It is commonly used for web scraping, which involves extracting data from websites. Selenium allows you to simulate human interactions with a web page, such as clicking buttons, filling out forms, and navigating through pages, to collect the desired data...")
    slt.markdown('''Pandas: Use the powerful Pandas library to transform the dataset from CSV format into a structured dataframe.
                    Pandas helps data manipulation, cleaning, and preprocessing, ensuring that data was ready for analysis.''')
    slt.markdown('''MySQL: With help of SQL to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                    and the data was efficiently inserted into relevant tables for storage and retrieval.''')
    slt.markdown("Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.")
    slt.subheader(":blue[Skill-take:]")
    slt.markdown("Selenium, Python, Pandas, MySQL,mysql-connector-python, Streamlit.")
    slt.subheader(":blue[Developed-by:]  Bharath Roshan")


# States and Routes page setting
if web == "📍States and Routes":
    S = slt.selectbox("Lists of States", ["Kerala", "Adhra Pradesh", "Telugana", "Goa", "Rajastan", 
                                          "South Bengal", "Haryana", "Assam", "Uttar Pradesh", "West Bengal"])
    
    col1, col2 = slt.columns(2)
    with col1:
        select_type = slt.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = slt.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    TIME = slt.time_input("Select the time")

    # Function to filter bus fare based on state and route
    def type_and_fare(bus_type, fare_range, route_name):
        conn = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            user="uPQBsEr6GMWbPMw.root",
            password="TswbstDDSQN3zOLj",
            database="RED_BUS_DETAILS"
        )
        my_cursor = conn.cursor()
        
        # Define fare range based on selection
        fare_min, fare_max = {
            "50-1000": (50, 1000),
            "1000-2000": (1000, 2000),
            "2000 and above": (2000, 100000)
        }[fare_range]
        
        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{route_name}"
            AND {bus_type_condition} AND Start_time >= '{TIME}'
            ORDER BY Price DESC, Start_time
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    # State-specific route handling
    state_route_map = {
        "Kerala": lists_k,
        "Adhra Pradesh": lists_A,
        "Telugana": lists_T,
        "Goa": lists_g,
        "Rajastan": lists_R,
        "Chandigarh": lists_Ch,
        "Haryana": lists_H,
        "Assam": lists_AS,
        "Uttar Pradesh": lists_UP,
        "West Bengal": lists_WB,
    }

    if S in state_route_map:
        route_list = state_route_map[S]
        selected_route = slt.selectbox("List of routes", route_list)
        df_result = type_and_fare(select_type, select_fare, selected_route)
        slt.dataframe(df_result)


# In[ ]:




