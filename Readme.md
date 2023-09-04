# YouTube Data Harvesting and Warehousing Project

## Project Title: YouTube Data Harvesting and Warehousing using SQL, MongoDB, and Streamlit

### Skills Learned:
- Python scripting
- Data collection
- MongoDB
- Streamlit
- API integration
- Data management using MongoDB (Atlas) and SQL

### Domain: Social Media (YouTube)

### Tools Used:
1. Python
2. MongoDB
3. MySQL
4. Google Client Library
5. Pandas
6. Plotly


### Project Description:

This project focuses on collecting data from YouTube using the YouTube API and storing it in MongoDB. The data is then migrated to a SQL database for efficient querying and visualization through a Streamlit application.

1. **Data Collection (YouTube Data Harvesting):**
   - Utilize Python scripting to interact with the YouTube API and retrieve data such as videos, channels, comments, and more.
   - Store the retrieved data in a structured format (e.g., JSON or CSV).

2. **MongoDB Setup:**
   - Set up a MongoDB instance.
   - Create a MongoDB database and collection(s) to store the collected YouTube data.
   - Use the PyMongo library to interact with MongoDB.
   - Write scripts to insert and manage data in MongoDB.

3. **SQL Database Setup:**
   - Design a SQL database schema that aligns with the structure of the collected data.
   - Employ a Python library like SQLAlchemy to interact with the SQL database.
   - Develop scripts to insert, update, and query data in the SQL database.

4. **Streamlit Dashboard Development:**
   - Create a Streamlit application to provide a user-friendly interface for accessing and analyzing YouTube data.
   - Utilize visualization libraries like Plotly or Matplotlib to generate charts and graphs.
   - Connect the Streamlit app to both the SQL and MongoDB databases to retrieve and display data.

### Project Setup:

1. **Development Environment Setup:**
   - Install Python and necessary libraries (pymongo, requests, pandas, streamlit, etc.).
   - Install MongoDB and your choice of SQL database (e.g., MySQL, PostgreSQL).

2. **Obtain YouTube API Access:**
   - Navigate to the Google Developer Console.
   - Create a project and enable the YouTube Data API.
   - Generate API credentials to obtain an API key for accessing YouTube data.

### How to Run the Project:

1. Clone this repository to your local machine.

2. Set up your development environment with the required Python libraries, MongoDB, and SQL database.

3. Obtain a YouTube API key from the Google Developer Console.

4. Configure your API key in the project's configuration files or environment variables.

5. Run the Python scripts for data extraction, MongoDB data storage, SQL database setup, and Streamlit app development.

6. Access the Streamlit application to explore and interact with the YouTube data.

### command to run the project:

Streamlit run webpage.py