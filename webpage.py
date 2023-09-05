import streamlit as st
from streamlit_option_menu import option_menu

import plotly.express as px
import pandas as pd
from pymongo import MongoClient
import mysql.connector


from sqlQuery import sql_q1, sql_q2, sql_q3, sql_q4, sql_q5, sql_q6, sql_q7, sql_q8, sql_q9, sql_q10

from createSqlTable import sql_create_tables

# MongoDB Atlas connection information
mongo_uri = "mongodb+srv://jeevaganps27244:jikatbcdps@jeevaganps.dpthifo.mongodb.net/?retryWrites=true&w=majority"

# MySQL database connections
mysql_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='jika27244tbcd',
    database='youtube_data'
)

# Create a cursor object
mysql_cursor = mysql_connection.cursor()

# Connect to MongoDB Atlas
client = MongoClient(mongo_uri)

# Accessing database and collection
db = client.get_database("youtube_data") 
collection = db.get_collection("channel_data")

sql_create_tables()


def set_sql_channel_table(Channel_Data):
    
    Channel_Info = Channel_Data["Channel_Info"]

    # Insert data into MySQL database
    insert_query = "INSERT INTO Channel (Channel_Id, Channel_Name, Subscription_Count, Channel_Views, Channel_Description) VALUES (%s, %s, %s, %s, %s);"

    data = (Channel_Info["Channel_Id"], Channel_Info["Channel_Name"], Channel_Info["Subscription_Count"],Channel_Info["Channel_Views"],Channel_Info["Channel_Description"])

    mysql_cursor.execute(insert_query, data)
    mysql_connection.commit()
        
def set_sql_playlist_table(Channel_Data):
    
    Channel_Info = Channel_Data["Channel_Info"]

    # Insert data into MySQL database
    insert_query = "INSERT INTO Playlist (Playlist_Id, Channel_Id, Playlist_Name) VALUES (%s, %s, %s);"

    data = (Channel_Info["Playlist_Id"],Channel_Info["Channel_Id"],Channel_Info["Playlist_Name"])

    mysql_cursor.execute(insert_query, data)
    mysql_connection.commit()    

def set_sql_video_table(Channel_Data):

    Channel_Info = Channel_Data["Channel_Info"]
    
    Video_Info = Channel_Data["Videos"]

    for eachVideo in Video_Info.values():
        # Insert data into MySQL database
        insert_query = "INSERT INTO Video (Video_Id ,Playlist_Id ,Video_Name ,Video_Description ,PublishedAt ,View_Count ,Like_Count ,Dislike_Count ,Favorite_Count ,Comment_Count ,Duration ,Thumbnail ,Caption_Status) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s);"

        data = (eachVideo["Video_Id"],Channel_Info["Playlist_Id"],eachVideo["Video_Name"],eachVideo["Video_Description"],eachVideo["PublishedAt"],eachVideo["View_Count"],eachVideo["Like_Count"],eachVideo["Dislike_Count"],eachVideo["Favorite_Count"],eachVideo["Comment_Count"],eachVideo["Duration"],eachVideo["Thumbnail"],eachVideo["Caption_Status"])

        mysql_cursor.execute(insert_query, data)
        mysql_connection.commit() 

def set_sql_comment_table(Channel_Data):
    
    Video_Info = Channel_Data["Videos"]

    for eachVideo in Video_Info.values():
        
        Video_Comments = eachVideo["Comments"]

        for eachComments in Video_Comments.values():
            # Insert data into MySQL database
            insert_query = "INSERT INTO Comment (Comment_Id,Video_Id ,Comment_Text,Comment_Author,Comment_PublishedAt) VALUES (%s, %s, %s,%s, %s);"

            data = (eachComments["Comment_Id"],eachVideo["Video_Id"],eachComments["Comment_Text"],eachComments["Comment_Author"],eachComments["Comment_PublishedAt"])

            mysql_cursor.execute(insert_query, data)
            mysql_connection.commit() 

       
    


# Use Streamlit's session state to track the currently selected tab and channel ID
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "About"
if 'Channel_Id_Input' not in st.session_state:
    st.session_state.Channel_Id_Input = ""

# Sidebar navigation
selected_tab = st.sidebar.radio("Navigation", ["About", "Channel Data", "Data Migration", "Data Analysis"])

if selected_tab == "About":
    st.session_state.selected_tab = "About"
    st.header("About My Project")
    

    # Streamlit app title and description
    st.title("YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit")
    st.write("This project involves collecting data from YouTube, storing it in MongoDB, migrating it to SQL, and visualizing the data.")

    # Project Explanation
    st.header("Explanation about project:")
    st.write("1. This proiect Collects the data from youtube using youtube api and get stored the data in mongodb and migrate through sol and visualised")
    st.write("2. The streamit Application allows the users to access and analyze data from multiple YouTube channels ")
    st.write("3. This apolication allows the user to give a YouTube channel ID as input and retrivies the relevant data. Able to collect data for multiple YouTube channels and store them in a database just clicking a button")
    st.write("4. By Selecting a channel, we could migrate the data from MongoDB Database to mySQL, to retrieve the relevant youtube Channel information like video comments, likes.")



    st.write("Overall, the approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing it in a MongoDB data lake, migrating it to a SQL data warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.")

    # Project steps
    st.header("Project Steps:")
    st.write("1. **Set Up Your Development Environment:**")
    st.write("   - Install Python and necessary libraries like pymongo, requests, pandas, streamlit, etc.")
    st.write("   - Install MongoDB and a SQL database (e.g., MySQL, PostgreSQL).")

    st.write("2. **Get YouTube API Access:**")
    st.write("   - Go to the Google Developer Console.")
    st.write("   - Create a project and enable the YouTube Data API.")
    st.write("   - Create API credentials to obtain an API key.")

    st.write("3. **Data Extraction (YouTube Data Harvesting):**")
    st.write("   - Write a Python script to use the YouTube API and fetch data (videos, channels, comments, etc.) based on your requirements.")
    st.write("   - Store the retrieved data in a structured format (e.g., JSON or CSV).")

    st.write("4. **MongoDB Setup:**")
    st.write("   - Set up a MongoDB instance.")
    st.write("   - Create a MongoDB database and collection(s) to store your data.")
    st.write("   - Use the PyMongo library to interact with MongoDB.")
    st.write("   - Write scripts to insert the transformed data into MongoDB.")

    st.write("5. **SQL Database Setup:**")
    st.write("   - Create a SQL database schema that matches the structure of your transformed data.")
    st.write("   - Use a Python library like SQLAlchemy to interact with the SQL database.")
    st.write("   - Write scripts to insert the transformed data into the SQL database.")

    st.write("6. **Streamlit Dashboard Development:**")
    st.write("   - Create a Streamlit application to visualize and interact with your data.")
    st.write("   - Use libraries like Plotly or Matplotlib to create charts and graphs.")
    st.write("   - Connect your Streamlit app to both SQL and MongoDB databases to fetch and display data.")


elif selected_tab == "Channel Data":
    st.session_state.selected_tab = "Channel Data"
    st.header("Channel Data")
    # Retrieve data from MongoDB
    mongo_data = collection.find()
    Channel_Data = list(mongo_data)

    channel_list = []

    serial_no = 1

    for eachChannel in Channel_Data:
        channel_info = eachChannel["Channel_Info"]

        channel = {
            "Serial_No":serial_no,
            "Channel_Id":channel_info["Channel_Id"],
            "Channel_Name":channel_info["Channel_Name"],
            "Channel_Description":channel_info["Channel_Description"],
        }

        serial_no = serial_no + 1

        channel_list.append(channel)

    # Display the data as a table
    st.dataframe(channel_list)

elif selected_tab == "Data Migration":
    st.session_state.selected_tab = "Data Migration"
    st.header("Data Migration")
    Channel_Id_Input = st.text_input("Enter Channel ID:", st.session_state.Channel_Id_Input)
    st.session_state.Channel_Id_Input = Channel_Id_Input  # Update session state
    
    # Move the button outside the conditional statement
    migrate_button = st.button("Migrate Data to MySQL")
    
    if migrate_button and Channel_Id_Input:
        # Retrieve data for the specified channel from MongoDB
        Channel_Data = collection.find_one({"Channel_Id" : Channel_Id_Input })
        
        if Channel_Data:
            # Adds the data to channel table
            set_sql_channel_table(Channel_Data)

            # Adds the data to playlist table
            set_sql_playlist_table(Channel_Data)

            # Adds the data to video table
            set_sql_video_table(Channel_Data)

            # Adds the data to comment table
            set_sql_comment_table(Channel_Data)

            st.success(f"Data for Channel ID {Channel_Id_Input} migrated successfully to MySQL.")
        else:
            st.warning(f"No data found for Channel ID {Channel_Id_Input} in MongoDB.")

elif selected_tab == "Data Analysis":
    st.session_state.selected_tab = "Data Analysis"
    st.header("Frequently Asked Questions")

    st.write("## :orange[Select any question to get Insights]")

    questions = st.selectbox('Questions',
    ['Click the question that you would like to query',
    '1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])
    
    if questions == '1. What are the names of all the videos and their corresponding channels?':
        df = sql_q1()

        st.write(df)
        
    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        df = sql_q2()

        st.write(df[0])

        st.write("### :green[Number of videos in each channel :]")
        
        fig = px.bar(df[0],
                     x=df[1],
                     y=df[2],
                     orientation='v',
                     color=df[3]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        df = sql_q3()

        st.write(df[0])

        st.write("### :green[Top 10 most viewed videos :]")

        fig = px.bar(df[0],
                     x=df[1],
                     y=df[2],
                     orientation='h',
                     color=df[3]
                    )
        
        st.plotly_chart(fig,use_container_width=True)

    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        df = sql_q4()

        st.write(df)

    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        df = sql_q5()

        st.write(df)

    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        df = sql_q6()

        st.write(df)
    
    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        df = sql_q7()

        st.write(df)

    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        df = sql_q8()

        st.write(df)  

    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        df = sql_q9()

        st.write(df)

    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        df = sql_q10()

        st.write(df)
    

# Run the Streamlit app



