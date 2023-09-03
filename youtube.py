import googleapiclient.discovery 

from googleapiclient.discovery import build

import pymongo
import json

# MongoDB Atlas connection information
mongo_uri = "mongodb+srv://jeevaganps27244:jikatbcdps@jeevaganps.dpthifo.mongodb.net/?retryWrites=true&w=majority"

# Api key
api_key = "AIzaSyAId80BDxNjfPmXvVVpG-Lo7BoA7Onr-H4"

# Connect to MongoDB Atlas
client = pymongo.MongoClient(mongo_uri)

# Accessing mongo db database
db = client.get_database("youtube_data") 

# Api
youtube = build('youtube',"v3",developerKey=api_key)

# Function to handle errors and return default channel data
def handle_error():
    return {
        "Channel_Info": {
            "Channel_Name": "N/A",
            "Channel_Id": "N/A",
            "Subscription_Count": 0,
            "Channel_Views": 0,
            "Channel_Description": "N/A",
            "Playlist_Id": "N/A"
        }
    }

# Function to get the playlist name
def get_playlist_name(playlist_id):
    try:
        request = youtube.playlists().list(
            part="snippet",
            id=playlist_id
        )
        response = request.execute()
        playlist_name = response["items"][0]["snippet"]["title"]
        return playlist_name
    except:
        # Return "N/A" if playlist name is not available
        return "N/A"  
    
# Retrieve channel data
def get_channel_data(channel):
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            forUsername=channel
        )
        response = request.execute()
        
        channel_data = response.get("items", [])[0]

        channel_info = {
            "Channel_Info": {
                "Channel_Name": channel_data["snippet"]["title"],
                "Channel_Id": channel_data["id"],
                "Subscription_Count": int(channel_data["statistics"]["subscriberCount"]),
                "Channel_Views": int(channel_data["statistics"]["viewCount"]),
                "Channel_Description": channel_data["snippet"]["description"],
                "Playlist_Id": channel_data["id"] + channel_data["statistics"]["viewCount"] , #todo
                "Playlist_Name":channel_data["snippet"]["title"] + " playlist" #todo
            }
        }
        return channel_info
    except:
        pass


# Retrieve video details with comments
def get_video_details(channel_id, max_results=10):
    try:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=max_results,
            order="date"
        )
        response = request.execute()

        video_data = {}
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_data[video_id] = {
                "Video_Id": video_id,
                "Video_Name": "",
                "Video_Description": "",
                "Tags": [],
                "PublishedAt": "",
                "View_Count": 0,
                "Like_Count": 0,
                "Dislike_Count": 0,
                "Favorite_Count": 0,
                "Comment_Count": 0,
                "Duration": "",
                "Thumbnail": "",
                "Caption_Status": "",
                "Comments": {}
            }

        for video_id in video_data.keys():
            request = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            )
            response = request.execute()
            video_info = response["items"][0]
            video_data[video_id]["Video_Name"] = video_info["snippet"]["title"]
            video_data[video_id]["Video_Description"] = video_info["snippet"]["description"]
            video_data[video_id]["Tags"] = video_info["snippet"].get("tags", [])
            video_data[video_id]["PublishedAt"] = video_info["snippet"]["publishedAt"]
            video_data[video_id]["View_Count"] = int(video_info["statistics"].get("viewCount", 0))
            video_data[video_id]["Like_Count"] = int(video_info["statistics"].get("likeCount", 0))
            video_data[video_id]["Dislike_Count"] = int(video_info["statistics"].get("dislikeCount", 0))
            video_data[video_id]["Favorite_Count"] = int(video_info["statistics"].get("favoriteCount", 0))
            video_data[video_id]["Comment_Count"] = int(video_info["statistics"].get("commentCount", 0))
            video_data[video_id]["Duration"] = video_info["contentDetails"]["duration"]
            video_data[video_id]["Thumbnail"] = video_info["snippet"]["thumbnails"]["default"]["url"]
            video_data[video_id]["Caption_Status"] = video_info["contentDetails"].get("caption")

            # Retrieve comments for each video, if available
            if video_data[video_id]["Comment_Count"] > 0:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=6
                )
                response = request.execute()
                for item in response.get("items", []):
                    comment_id = item["id"]
                    comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comment_author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                    comment_published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    video_data[video_id]["Comments"][comment_id] = {
                        "Comment_Id": comment_id,
                        "Comment_Text": comment_text,
                        "Comment_Author": comment_author,
                        "Comment_PublishedAt": comment_published_at
                    }
    except googleapiclient.errors.HttpError as e:
        print(f"Error fetching video data: {str(e)}")
    return video_data
    

def get_all_channel_data(channel_array):
    for channel in channel_array:

        # Get the channel data
        channel_data = get_channel_data(channel)

        # Get video details with comments for the channel
        video_data = get_video_details(channel_data["Channel_Info"]["Channel_Id"])

        # Combine channel and video data
        channel_data["Videos"] = video_data

        # Adding channel Id
        channel_data["Channel_Id"] = channel_data["Channel_Info"]["Channel_Id"]

        # Add channel data to mongo db collection
        set_channel_data_mongodb(channel_data)

# store channel data in mobo db collection
def set_channel_data_mongodb(channel_data):
    collection = db.get_collection("channel_data")

    # Insert the JSON document into the collection
    result = collection.insert_one(channel_data)

    # Check if the insertion was successful
    if result.acknowledged:
        print("JSON document inserted successfully. ObjectId:", result.inserted_id)
    else:
        print("Failed to insert JSON document.")

channel_array =["BBCNews","CNBC","NewsGlitz","ABCNews","SkyNews","CNN","channelnewsasia","aljazeeraenglish","USATODAY","Behindwoodstv"]


get_all_channel_data(channel_array)

# Close the MongoDB connection
client.close()