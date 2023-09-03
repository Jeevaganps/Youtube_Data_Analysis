import pandas as pd
import mysql.connector

# MySQL database connections
mysql_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='jika27244tbcd',
    database='youtube_data'
)

# Create a cursor object
mysql_cursor = mysql_connection.cursor()

# 1) What are the names of all the videos and their corresponding channels?
def sql_q1():
    mysql_cursor.execute("""SELECT V.Video_Name, C.Channel_Name
    FROM Video V
    INNER JOIN Playlist P ON V.Playlist_Id = P.Playlist_Id
    INNER JOIN Channel C ON P.Channel_Id = C.Channel_Id;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df

# 2) Which channels have the most number of videos, and how many videos do they have ?
def sql_q2():
    mysql_cursor.execute("""SELECT C.Channel_Name, COUNT(V.Video_Id) AS Video_Count
    FROM Channel C
    INNER JOIN Playlist P ON C.Channel_Id = P.Channel_Id
    INNER JOIN Video V ON P.Playlist_Id = V.Playlist_Id
    GROUP BY C.Channel_Name
    ORDER BY Video_Count DESC
    LIMIT 1;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    x=mysql_cursor.column_names[0]
    y=mysql_cursor.column_names[1]
    color=mysql_cursor.column_names[0]
    
    return df,x,y,color

# 3) What are the top 10 most viewed videos and their respective channels?
def sql_q3():
    mysql_cursor.execute("""SELECT V.Video_Name, C.Channel_Name, V.View_Count
    FROM Video V
    INNER JOIN Playlist P ON V.Playlist_Id = P.Playlist_Id
    INNER JOIN Channel C ON P.Channel_Id = C.Channel_Id
    ORDER BY V.View_Count DESC
    LIMIT 10;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    x=mysql_cursor.column_names[2]
    y=mysql_cursor.column_names[1]
    color=mysql_cursor.column_names[0]

    return df,x,y,color

# 4) How many comments were made on each video, and what are their corresponding video names?
def sql_q4():
    mysql_cursor.execute("""SELECT Video_Name, Comment_Count
    FROM Video;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df

# 5) Which videos have the highest number of likes, and what are their corresponding channel names?
def sql_q5():
    mysql_cursor.execute("""SELECT V.Video_Name, C.Channel_Name, V.Like_Count
    FROM Video V
    INNER JOIN Playlist P ON V.Playlist_Id = P.Playlist_Id
    INNER JOIN Channel C ON P.Channel_Id = C.Channel_Id
    WHERE V.Like_Count = (SELECT MAX(Like_Count) FROM Video);
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df

# 6) What is the total number of likes and dislikes for each video, and what are their corresponding video names?
def sql_q6():
    mysql_cursor.execute("""SELECT V.Video_Name, SUM(V.Like_Count) AS Total_Likes, SUM(V.Dislike_Count) AS Total_Dislikes
    FROM Video V
    GROUP BY V.Video_Name;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df

# 7) What is the total number of views for each channel, and what are their corresponding channel names?
def sql_q7():
    mysql_cursor.execute("""SELECT C.Channel_Name, SUM(V.View_Count) AS Total_Views
    FROM Channel C
    INNER JOIN Playlist P ON C.Channel_Id = P.Channel_Id
    INNER JOIN Video V ON P.Playlist_Id = V.Playlist_Id
    GROUP BY C.Channel_Name;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df

# 8) What are the names of all the channels that have published videos in the year 2022?
def sql_q8():
    mysql_cursor.execute("""SELECT DISTINCT C.Channel_Name
    FROM Channel C
    INNER JOIN Playlist P ON C.Channel_Id = P.Channel_Id
    INNER JOIN Video V ON P.Playlist_Id = V.Playlist_Id
    WHERE YEAR(V.PublishedAt) = 2022;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df

# 9) What is the average duration of all videos in each channel, and what are their corresponding channel names?
def sql_q9():
    mysql_cursor.execute("""SELECT C.Channel_Name, AVG(V.Duration) AS Average_Duration
    FROM Channel C
    INNER JOIN Playlist P ON C.Channel_Id = P.Channel_Id
    INNER JOIN Video V ON P.Playlist_Id = V.Playlist_Id
    GROUP BY C.Channel_Name;
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df

# 10) Which videos have the highest number of comments, and what are their corresponding channel names?
def sql_q10():
    mysql_cursor.execute("""SELECT V.Video_Name, C.Channel_Name, V.Comment_Count
    FROM Video V
    INNER JOIN Playlist P ON V.Playlist_Id = P.Playlist_Id
    INNER JOIN Channel C ON P.Channel_Id = C.Channel_Id
    WHERE V.Comment_Count = (SELECT MAX(Comment_Count) FROM Video);
    """)

    df = pd.DataFrame(mysql_cursor.fetchall(),columns=mysql_cursor.column_names)

    return df