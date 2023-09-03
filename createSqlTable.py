import mysql.connector

# Create SQL table for Channel, Playlist, Video and Comments
def sql_create_tables():
    # MySQL database connections
    mysql_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='jika27244tbcd',
        database='youtube_data'
    )

    # Create a cursor object
    mysql_cursor = mysql_connection.cursor()

    # Creates Channel Table
    create_channel_table_query = "CREATE TABLE IF NOT EXISTS Channel ( Channel_Id VARCHAR(255),Channel_Name VARCHAR(255),Subscription_Count INT,Channel_Views VARCHAR(255),Channel_Description TEXT,PRIMARY KEY (Channel_Id));"
    mysql_cursor.execute(create_channel_table_query)
    mysql_connection.commit()

    # Creates Playlist Table
    create_playlist_table_query = "CREATE TABLE IF NOT EXISTS Playlist (Playlist_Id VARCHAR(255),Channel_Id VARCHAR(255), Playlist_Name VARCHAR(255),PRIMARY KEY (Playlist_Id),FOREIGN KEY (Channel_Id) REFERENCES Channel(Channel_Id));"
    mysql_cursor.execute(create_playlist_table_query)
    mysql_connection.commit()

    # Creates Video Table
    create_video_table_query = "CREATE TABLE IF NOT EXISTS Video (Video_Id VARCHAR(255),Playlist_Id VARCHAR(255),Video_Name VARCHAR(255),Video_Description TEXT,PublishedAt TEXT,View_Count INT,Like_Count INT,Dislike_Count INT,Favorite_Count INT,Comment_Count INT,Duration TEXT,Thumbnail VARCHAR(255),Caption_Status VARCHAR(255),PRIMARY KEY (Video_Id),FOREIGN KEY (Playlist_Id) REFERENCES Playlist(Playlist_Id));"
    mysql_cursor.execute(create_video_table_query)
    mysql_connection.commit()

    # Creates Comment Table
    create_comment_table_query = "CREATE TABLE IF NOT EXISTS Comment (Comment_Id VARCHAR(255),Video_Id VARCHAR(255),Comment_Text TEXT,Comment_Author VARCHAR(255),Comment_PublishedAt TEXt,PRIMARY KEY (Comment_Id),FOREIGN KEY (Video_Id) REFERENCES Video(Video_Id));"
    mysql_cursor.execute(create_comment_table_query)
    mysql_connection.commit()



