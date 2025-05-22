#!/usr/bin/env python
# coding: utf-8

# # Exploring YouTube Video Trends and Predictive Insights
# 
# **Author:** Alinzon Simon  
# **Course:** Adv. Programming Techniques  
# **School:** School of Professional Studies  
# **Date:** May 2025
# 

# # Abstract
# The YouTube recommendation engine significantly influences content visibility and user engagement, contributing to a dynamic, data-driven media landscape. Analyzing trending videos provides valuable insights into user engagement patterns across different regions. This study investigates the popularity of video categories among the top 50 trending videos in multiple countries, examining how regional preferences shape content trends. Additionally, it explores the correlation between video categories and user engagement metrics, specifically the number of likes and views a video receives.
#             
# To further deepen the engagement analysis, this study evaluates the feasibility of predicting video popularity, measured by likes and views, based on features such as description content, category, and region. By leveraging machine learning techniques, the research aims to develop predictive models that identify key drivers of virality, incorporating statistical analysis and natural language processing (NLP).
#             
# Finally, sentiment analysis is applied to video descriptions to evaluate how emotional tone, particularly expressions of joy and happiness, influences user interaction. By mapping sentiment to engagement metrics like likes, comments, and views, this research aims to uncover whether emotionally charged descriptions lead to higher engagement levels.The findings from this study contribute to a broader understanding of digital media trends and user behavior, offering insights for content creators, marketers, and platform developers seeking to optimize engagement strategies.

# # Introduction
# 
# With the rise of digital content consumption, YouTube has become a dominant platform shaping media trends across the globe. The dynamics of trending videos offer valuable insights into user preferences and engagement patterns, influenced by factors such as video category, regional audience behavior, and emotional sentiment. 
# First, we investigate the most popular YouTube video categories among the top 50 trending videos in different countries, analyzing how regional preferences influence content trends. Second, we assess the correlation between video categories and the number of likes they receive, identifying patterns in audience engagement.
# Additionally, we explore the feasibility of predicting video popularity—measured through likes and views based on attributes like description content, category, and geographic region. Using machine learning techniques, this study seeks to identify key factors driving engagement. 
# Finally, we examine the role of emotions and sentiments embedded within video descriptions to determine their impact on user interactions, specifically whether positive emotional tones like joy and happiness contribute to higher levels of likes and comments.            

# # Project Overview
# ## Objective
# 
# This project explores the dynamics of YouTube’s trending video ecosystem by analyzing the top 50 trending videos across multiple countries. The goal is to understand content trends, user engagement patterns, and the emotional impact of video descriptions. Through statistical analysis and machine learning, this study provides actionable insights into what drives video popularity and viewer interaction.
# 
# Its primary objectives include:
# - Understanding regional preferences in content categories
# - Examining user engagement patterns (views, likes, comments)
# - Developing predictive models for video popularity
# - Assessing the emotional tone of video descriptions and its impact on engagement
# 
# ## Dataset Description
# 
# - Video Metadata: title, description, publishedat, video_id, channel_title
# - Categorical: category_name, region_name, livebroadcastcontent
# - Engagement Metrics: view_count, like_count, comment_count, favoritecount
# 
# ## Research Questions
# 1. What are the most popular YouTube video categories across different countries in the top 50 trending videos, and how do regional preferences vary for these trending videos?
# 
#    **Hypothesis:** The popularity of video categories significantly differs across regions, with some categories (eg. music, entertainment) being universally popular and others (eg. news, sports) reflecting regional preferences.
# 
# 2. How does the category of a YouTube video correlate with the number of likes it receives?
# 
#     **Hypothesis:** Certain categories, such as entertainment and music, receive consistently higher like counts than informational categories.
# 
# 3. Can we predict the number of likes or views a YouTube video will receive based on its description, category, or region?
# 
#    **Hypothesis:** Video metadata (category, region) and description content can be used to build models that effectively predict likes and views, with region and category being strong predictors.
# 
# 4. How do emotions and sentiments in video descriptions relate to engagement metrics, such as likes, comments, and views? Specifically, do descriptions with emotional tones like joy and happiness result in a higher number of likes and comments?
# 
#     **Hypothesis:** Descriptions expressing positive emotions (e.g., joy, excitement) correlate with higher user engagement, especially in the form of likes and comments.
# 
# 

# # Data Wrangling
# ## 1. Data Collection
# In this section, I wanted to apply the concepts I learned in the course, so I decided to create my own classes, define my own functions, and use lists and dictionaries.

# The credentials were saved in a .env file for security reasons and imported into the session to begin collecting the data. For this step a function called load_env_variables was created to load the environment variables from .env file.

# In[4]:


def load_env_variables():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    env_variables= {}
    env_variables["API"] = os.getenv("API_KEY")
    env_variables["ENV"] = os.getenv("ENVIRONMENT")
    env_variables["MongoClient"] = os.getenv("MONGODB_URL")
    env_variables["DB_NAME"] = os.getenv("DB_NAME")
    return env_variables


# I'm planning to call the API and save the data into MongoDB so I will define a function.

# In[5]:


def connect_to_mongo(mongo_url,db_name, collection_name):
    from pymongo import MongoClient
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[collection_name]
    return collection


# Now, I will create three functions. One to get the available categories per region, another one to get the full name of the regions and the last one to get the trending videos.

# In[13]:


def get_video_category(api_key,region_code='US'):
    import requests
    base_url = 'https://www.googleapis.com/youtube/v3/videoCategories'
    url = f'{base_url}?part=snippet&regionCode={region_code}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        categories = response.json().get('items', [])
        category_dict = {
            cat['id']: {
                'id': cat['id'],
                'title': cat['snippet']['title'],
                'region_code': region_code
            }
            for cat in categories
        }
        return category_dict

def get_available_regions(api_key):
    import requests
    base_url = 'https://www.googleapis.com/youtube/v3/i18nRegions'
    url = f'{base_url}?part=snippet&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        regions = []
        all_regions = response.json().get('items', [])
        for item in all_regions:
            regions_details = {
                'id': item['id'],
                'name': item['snippet']['name'],
                'gl': item['snippet']['gl'],
            }
            regions.append(regions_details)
        return regions
    return []

def get_youtube_trending_videos(api_key, region_code='US', max_results=10):
    from googleapiclient.discovery import build
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        request = youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            regionCode=region_code,
            maxResults=max_results
        )
        response = request.execute()

        videos = []
        for item in response.get('items', []):
            video_details = {
                'title': item['snippet']['title'],
                'publishedAt': item['snippet']['publishedAt'],
                'description': item['snippet']['description'],
                'video_id': item['id'],
                'channel_title': item['snippet']['channelTitle'],
                'categoryId': item['snippet']['categoryId'],
                'liveBroadcastContent': item['snippet']['liveBroadcastContent'],
                'view_count': item['statistics'].get('viewCount', 'N/A'),
                'like_count': item['statistics'].get('likeCount', 'N/A'),
                'comment_count': item['statistics'].get('commentCount', 'N/A'),
                'favoriteCount': item['statistics'].get('favoriteCount', 'N/A'),
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
                'region_code': region_code,
            }
            videos.append(video_details)

        return videos

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# In the next step, I will call all the functions I created so I can import the data into MongoDB. Three different Collections were created in MongoDB.
# 
# - Youtube Trending Videos

# In[ ]:


api_key = load_env_variables().get('API')
env  = load_env_variables().get('ENV')
MongoClient = load_env_variables().get('MongoClient')
db_name = 'YouTubeTrending'
collection_name = 'Videos'
client = connect_to_mongo(MongoClient, db_name, collection_name)
client.create_index([('video_id', ASCENDING)], unique=True)
trending_videos_response = get_youtube_trending_videos(api_key, max_results=1000)
client.insert_many(trending_videos_response, ordered=False)


# - Videos Regions

# In[ ]:


collection_name3 = 'Videos_Regions'
client3 = connect_to_mongo(MongoClient, db_name, collection_name3)
regions_list = get_available_regions(api_key)
client3.insert_many(regions_list)


# - Videos Categories
#   
# This function requires a region code as an input, so I created a CSV file containing that information for later import into a DataFrame. Using a *for* loop, the function was executed for each value in the dataset.

# In[ ]:


collection_name2 = 'Videos_Categories'
client2 = connect_to_mongo(MongoClient, db_name, collection_name2)
file_path = 'data/YouTubeTrending.Videos_Regions.csv'
csv_data = load_csv_file(file_path)

for(index, row) in csv_data.iterrows():
    region_code =row['id']
    print(f"Current Region: {region_code}")
    category_dict = get_video_category(api_key, region_code=region_code)
    if category_dict:
        client2.insert_many(list(category_dict.values()))
    else:
        print(f"No categories found for region: {region_code}")


# ## 2. Data Cleansing
# The goal of this step is to improve data quality, enabling better decision-making and increasing the efficiency of data analysis.
# 
# ### 2.1. Load the Data
# To explore the data, I created a Python class called *DBConnector*, which contains predefined methods that I will use to insert, extract, and update records in MongoDB. As mentioned previously, the data was extracted by calling the YouTube API, loaded into MongoDB to avoid multiple API calls, and then retrieved into a dataframe for further exploration.        

# In[6]:


class DBConnector:
    def __init__(self, mongo_url, db_name, collection_name):
        from pymongo import MongoClient
        self.client = MongoClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_one(self, data):
        return self.collection.insert_one(data)

    def insert_many(self, data):
        return self.collection.insert_many(data)

    def find(self, query):
        return self.collection.find(query)

    def find_all(self):
        return self.collection.find()

    def update_one(self, query, update):
        return self.collection.update_one(query, update)

    def delete_one(self, query):
        return self.collection.delete_one(query)


# Now, I will import the credentials, followed by importing Pandas to begin working with the DataFrames.

# In[7]:


env_variables = load_env_variables()
mongo_url = env_variables["MongoClient"]
db_name = env_variables["DB_NAME"]
collection_videos = "Videos"
collection_categories = "Videos_Categories"
collection_regions = "Videos_Regions"


# In[8]:


import pandas as pd


# #### 2.1.1 Importing Videos data from MongoDB
# 
# Videos collection from MongoDB will be imported into a list, then transformed into a dataframe for data cleansing.

# In[9]:


db_connector = DBConnector(mongo_url, db_name, collection_videos)
videos =list(db_connector.find_all())
df_videos = pd.DataFrame(videos)
print(f"Total records in {collection_videos} collection: {len(df_videos)}")


# In[10]:


print( df_videos.iloc[:, [1,2,5,7,8,9,10,13]].head(5))


# #### 2.1.2 Import Category data from MongoDB
# Videos_Categories collection from MongoDB will be imported into a list, then transformed into a dataframe for data cleansing.

# In[11]:


db_connector2 = DBConnector(mongo_url, db_name, collection_categories)
categories = list(db_connector2.find_all())
df_categories = pd.DataFrame(categories)
print(f"Total records in {collection_categories} collection: {len(df_categories)}")


# In[12]:


print(df_categories.iloc[:, [1,2,3]].head(5))


# #### 2.1.3 Import Region data from MongoDB
# Videos_Regions collection from MongoDB will be imported into a list, then transformed into a dataframe for data cleansing.

# In[13]:


db_connector3 = DBConnector(mongo_url, db_name, collection_regions)
regions = list(db_connector3.find_all())
df_regions = pd.DataFrame(regions)
print(f"Total records in {collection_regions} collection: {len(df_regions)}")
print(df_regions.iloc[:, :].head(5))


# Now that the data is loaded in some data frames I will proceed to generate the plots

# ### 2.2. Understand the Data

# Before manipulating the data, it's essential to understand the structure and columns we'll be working with. In this case, we have three DataFrames: **df_videos**, **df_categories**, and **df_regions**.
# 
# #### 2.2.1 df_videos DataFrame
# 
# In order to understand the structure of this DataFrame we will use info() method

# In[14]:


print(df_videos.info())


# As a result of the previous step, we identified several columns with incorrect data types: **categoryID**, **view_count**, **like_count**, **comment_count**, and **favoriteCount**.

# In[15]:


print(df_videos.head())


# #### 2.2.2 df_categories DataFrame
# 
# For this DataFrame we will also use info().

# In[16]:


print(df_categories.info())


# We can identify incorrect data types for the **id** column, which is especially important if we intend to use this column for join operations.

# In[17]:


print(df_categories.head())


# #### 2.2.2 df_regions DataFrame
# 
# Same as the other DataFrames we will also use info().

# In[18]:


print(df_regions.info())


# In this case, we will update 'id' to 'region_code' to ensure name consistency across all data frames.

# In[19]:


print(df_regions.head())


# ### 2.3. Fix Data Types and column Names
# 
# - df_videos
#  
#   We will fix the data types and column names for categoryID, view_count, like_count, comment_count, and favoriteCount. For the count columns any NA value will be replaced with 0.

# In[20]:


df_videos.rename(columns={'categoryId': 'category_id'}, inplace=True)


# In[21]:


df_videos['category_id'] = df_videos['category_id'].astype(int)


# In[22]:


df_videos['view_count'] = pd.to_numeric(df_videos['view_count'], errors='coerce')
df_videos['view_count'] = df_videos['view_count'].fillna(0).astype(int)


# In[23]:


df_videos['like_count'] = pd.to_numeric(df_videos['like_count'], errors='coerce')
df_videos['like_count'] = df_videos['like_count'].fillna(0).astype(int)


# In[24]:


df_videos['comment_count'] = pd.to_numeric(df_videos['comment_count'], errors='coerce')
df_videos['comment_count'] = df_videos['comment_count'].fillna(0).astype(int)


# In[25]:


df_videos['favoriteCount'] = pd.to_numeric(df_videos['favoriteCount'], errors='coerce')
df_videos['favoriteCount'] = df_videos['favoriteCount'].fillna(0).astype(int)


# In[26]:


print(df_videos.info())


# - df_categories
#  
#   We will fix the data types and column names for id.

# In[27]:


df_categories.rename(columns={'id': 'category_id'}, inplace=True)


# In[28]:


df_categories['category_id'] = df_videos['category_id'].astype(int)


# In[29]:


print(df_categories.info())


# - df_regions
# 
# Column rename for id to region_code and name to region_name

# In[30]:


df_regions.rename(columns={'id': 'region_code'}, inplace=True)
df_regions.rename(columns={'name': 'region_name'}, inplace=True)


# In[31]:


print(df_regions.info())


# For df_videos, df_categories and df_regions, I will use lowercase for all the columns and replace space with underscore.

# In[32]:


df_videos.columns = df_videos.columns.str.lower().str.replace(' ', '_')
df_categories.columns = df_categories.columns.str.lower().str.replace(' ', '_')
df_regions.columns = df_regions.columns.str.lower().str.replace(' ', '_')


# ### 2.4. Remove Missing values and duplicate rows

# #### 2.4.1 Remove rows with null values 

# In[33]:


df_videos = df_videos.dropna(how='all')
df_categories = df_categories.dropna(how='all')
df_regions = df_regions.dropna(how='all')


# #### 2.4.1 Remove duplicate rows

# In[34]:


df_videos = df_videos.drop_duplicates()
df_categories = df_categories.drop_duplicates()
df_regions = df_regions.drop_duplicates()


# Now I will generate a final DataFrame with the clean data.

# In[35]:


UT_Videos_df = pd.merge(df_videos, df_categories[['category_id','region_code','title']], on=['category_id','region_code'],how="left",suffixes=('', '_category'))
UT_Videos_df = UT_Videos_df.rename(columns={'title_category': 'category_name'})
UT_Videos_df = pd.merge(UT_Videos_df, df_regions[['region_code','region_name']], on=['region_code'],how="left")


# In[36]:


print(UT_Videos_df.columns)


# ## 3. Exploratory Data Analysis

# 
# 
# ### Top 10 Trending Categories by Total View Count
# 
# This chart shows the top 10 YouTube video categories based on total views. From the bars, we can see that the Comedy category has the highest total views across all regions, reaching approximately 32.77 billion views. It is followed closely by Shorts videos. Interestingly, the News & Politics category also appears in the top 10, highlighting significant viewer interest in current events.

# In[37]:


import plotly.express as px
top_categories = (
    UT_Videos_df.groupby('category_name')['view_count']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig = px.bar(
    top_categories,
    x='category_name',
    y='view_count',
    title='Top 10 Trending Categories by Total View Count',
    labels={'category_name': 'Category', 'view_count': 'Total Views'},
    color_discrete_sequence=['#FF0000']  # YouTube Red
)
fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828')  # YouTube Dark Gray
)
fig.show()


# ### Top 10 Trending Categories by View Count, Like Count and Comment Count
# 
# This grouped bar chart compares the top 10 most viewed YouTube video categories based on three key metrics: Total views (red), Total Likes (Dark Gray) and Total Comments (Rosy Brown). Comedy is the dominant category, with over 32.7 billion views, making it the most-watched and one of the most liked and commented categories.
# 

# In[41]:


import plotly.graph_objects as go
category_summary = (
    UT_Videos_df.groupby('category_name')[['view_count', 'like_count','comment_count']]
    .sum()
    .sort_values(by='view_count', ascending=False)
    .head(10)
    .reset_index()
)
fig = go.Figure()
fig.add_trace(go.Bar(
    x=category_summary['category_name'],
    y=category_summary['view_count'],
    name='Total Views',
    marker_color='#FF0000' ,
    text=category_summary['view_count'],
    textposition='outside'
))
fig.add_trace(go.Bar(
    x=category_summary['category_name'],
    y=category_summary['like_count'],
    name='Total Likes',
    marker_color='#282828',
    text=category_summary['like_count'],
    textposition='outside'
))
fig.add_trace(go.Bar(
    x=category_summary['category_name'],
    y=category_summary['comment_count'],
    name='Total Comments',
    marker_color='rosybrown' ,
    text=category_summary['comment_count'],
    textposition='outside'
))
fig.update_layout(
    title='Top 10 Trending Categories by View Count, Like Count and Comment Count',
    xaxis_title='Category',
    yaxis_title='Count',
    barmode='group',
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828'),
    legend=dict(title=None)
)
fig.show()


# ### Total Views by Region
# 
# This horizontal bar chart displays the total number of YouTube views per region, sorted in descending order. Each bar represents one region, with the bar length corresponding to the total view count. 
# - Bangladesh leads all regions with the highest total view count, with more than 15 billion views.
# - Other top performing regions include Malta, Pakistan, Malaysia, and Zimbabwe, each generating over 10 billion views.

# In[38]:


import plotly.express as px
top_regions = (
    UT_Videos_df.groupby('region_name')['view_count']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    top_regions,
    x='region_name',
    y='view_count',
    title='Total Views by Region',
    labels={'region_name': 'Region', 'view_count': 'Total Views'},
    color_discrete_sequence=['#FF0000']
)
fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828')
)
fig.show()


# ### Top 10 Regions by View Count (Stacked by Category)
# 
# This stacked bar chart displays the total YouTube video view counts for the top 10 regions, segmented by the top 10 video categories. Each bar represents a region, and the height corresponds to the total number of views. The bars are colored by category, allowing for a visual comparison of categories performance within each region.
# 
# - Malaysia has the highest total views among all regions shown, with strong contributions from Shorts, Comedy, Music, and Trailers categories.
# 
# - Bangladesh follows closely, where Family, Gaming, and Documentary dominate the view count.
# 
# - Comedy and Shorts consistently appear across multiple regions, indicating broad global appeal.
# 
# - The presence of News & Politics in multiple regions, including Bangladesh, Slovenia, Vietnam, Malaysia, Pakistan, and Israel, highlights the regional interest in current events.

# In[39]:


import plotly.express as px

region_category_views = (    UT_Videos_df.groupby(['region_name', 'category_name'])['view_count']
    .sum()
    .reset_index()
)
region_totals = (
    region_category_views.groupby('region_name')['view_count']
    .sum()
    .sort_values(ascending=False)
)
top_10_regions = region_totals.head(10).index.tolist()
category_totals = (
    region_category_views.groupby('category_name')['view_count']
    .sum()
    .sort_values(ascending=False)
)
top_categories = category_totals.head(10).index.tolist()

filtered_data = region_category_views[
    (region_category_views['region_name'].isin(top_10_regions)) &
    (region_category_views['category_name'].isin(top_categories))
]
fig = px.bar(
    filtered_data,
    x='region_name',
    y='view_count',
    color='category_name',
    barmode='stack',
    title='Top 10 Regions by View Count (Top 10 Categories Only)',
    labels={
        'region_name': 'Region',
        'view_count': 'Total Views',
        'category_name': 'Category'
    }
)

fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828'),
    legend_title_text='Category'
)

fig.show()


# ### Views vs Likes Colored by Category
# 
# This scatter plot illustrates the relationship between likes and views across YouTube videos, with each dot representing a video. The dots are colored by video category. There is a clear positive correlation between likes and views videos with higher likes generally have more views. The distribution of categories across the chart suggests that engagement is not confined to a single type of content.

# In[40]:


fig = px.scatter(
    UT_Videos_df,
    x='like_count',
    y='view_count',
    color='category_name',
    title='Views vs Likes Colored by Category',
    labels={'like_count': 'Likes', 'view_count': 'Views', 'category_name': 'Category'},
    hover_data=['title', 'channel_title']
)
fig.show()


# # Data Analysis
# 
# This section explores YouTube trending video data, leveraging visual exploration, correlation analysis, and feature-driven insights to investigate key research questions. It incorporates univariate and multivariate analyses to reveal trends in regional preferences, engagement dynamics, and the emotional tone of video descriptions.
# 
# ## Q1: Regional Preferences in Video Categories
# 
# **Objective:** Identify the most popular video categories in each region based on likes and views.
# 
# The popularity of video categories significantly differs across regions, with some categories being universally popular and others reflecting regional preferences.
# 
# ### Top Video Categories by Region - View Count
# 
# **Globally dominant Categories**
# - Action/Adventure
# 
# Leads in 21 countries including: India, United Kingdom, Mexico, Brazil, Greece, Morocco, and Thailand
# This indicates widespread appeal across Europe, South Asia, Latin America, and North Africa.
# 
# - Anime/Animation
# 
# Tops the chart in 16 countries: Chile, Cambodia, Saudi Arabia, Sri Lanka, Venezuela
# High popularity in Asia, Middle East, and Latin America.
# 
# - Autos & Vehicles
# 
# Most viewed in 8 countries:France, Japan, Kenya, Czechia
# Appealing in Europe, Africa, and Asia.
# 
# - Entertainment
# 
# Most popular in: Azerbaijan, Egypt, North Macedonia, Peru, Turkey, Zimbabwe
# Maintains broad appeal, particularly in Middle East and South America.
# 
# 
# **Regional Popular**
# 
# - Film & Animation
# 
# Only top in Bangladesh and Vietnam. This suggests localized cultural engagement.
# 
# - Drama
# 
# Each dominates in just a few regions. Estonia, Hungary, Indonesia, Ireland, Laos, Moldova and Spain.
# 
# - Documentary: Iraq, Lebanon, Uganda, etc.
# 
# Preserve history, traditions, and events, offering insight into past decisions
# 
# - Science & Technology
# 
# Tops in : Germany and Russia
# Reflects high tech engagement regions.
# 
# - Music
# 
# Surprisingly leads in only Finland
# Suggests that while music is globally liked, it may not consistently rank in top trending by average views across different regions.

# In[18]:


import pandas as pd
import plotly.express as px
UT_Videos_df = pd.read_csv('data/YouTubeTrending.Videos.csv')

top_categories = UT_Videos_df.groupby(['region_name', 'category_name'])['view_count'].mean().reset_index()
top_categories = top_categories.loc[top_categories.groupby('region_name')['view_count'].idxmax()]
top_categories = top_categories.sort_values(by='region_name')


fig = px.bar(top_categories, x='region_name', y='view_count', color='category_name',
             title='Top Categories by Region (Average View Count)',
             labels={'region_name': 'Region', 'view_count': 'Average View Count', 'category_name':'Category'},
             color_discrete_sequence=px.colors.qualitative.Plotly)

fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828'),
    legend_title_text='Category'
)
fig.show()


# In[24]:


categories = top_categories.groupby(['category_name'])['region_name'].unique().reset_index()
categories['region_name'] = categories['region_name'].apply(lambda x: ', '.join(x))
categories = categories.sort_values(by='category_name')
categories.columns = ['Category', 'Countries']
print(categories.to_string(index=False))


# 
# ### Top Video Categories by Region - Likes Count
# 
# **Globally dominant Categories**
# 
# - Action/Adventure
# 
# Most liked in 23 countries: Argentina, Greece, Croatia, South Korea, United States, Thailand, Malaysia, Mexico, Colombia, Kazakhstan
# This category is a consistent leader in both *views and likes*, indicating strong entertainment appeal.
# 
# - Anime/Animation
# 
# Tops likes in 16 countries: Cambodia, France, El Salvador, South Africa, Iceland, Saudi Arabia, Ukraine
# Strong presence in animation-loving cultures across Asia, Europe, and Africa.
# 
# - Autos & Vehicles
# 
# Countries:  Brazil, Canada, Costa Rica, Czechia, Denmark, Ghana, Japan, Nigeria, Senegal, Uruguay
# Indicates strong interest in car culture in certain regions.
# 
# **Regional Popular**
# 
# - Entertainment
# 
# Azerbaijan, Germany, Jamaica, Peru, Turkey, Zimbabwe
# Consistent favorite, particularly in Middle East and South America
# 
# - Gaming
# 
# Most liked in:  Dominican Republic, Libya, Portugal
# 
# - Education
# 
# United Arab Emirates, Vietnam
# 
# - Documentary
# 
# Bosnia and Herzegovina, Georgia, Hong Kong, Iraq, Kenya, Lebanon, Morocco, Pakistan, Serbia, Uganda
# 
# - Drama
# 
# Ecuador, Indonesia, Laos, Moldova, Nepal, Venezuela
# 
# 
# - 

# In[22]:


import pandas as pd
import plotly.express as px

top_categories2 = UT_Videos_df.groupby(['region_name', 'category_name'])['like_count'].mean().reset_index()
top_categories2 = top_categories2.loc[top_categories2.groupby('region_name')['like_count'].idxmax()]
top_categories2 = top_categories2.sort_values(by='region_name')


fig = px.bar(top_categories2, x='region_name', y='like_count', color='category_name',
             title='Top Categories by Region (Average Likes Count)',
             labels={'region_name': 'Region', 'like_count': 'Average Likes Count','category_name':'Category'},
             color_discrete_sequence=px.colors.qualitative.Plotly)

fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828'),
    legend_title_text='Category'
)
fig.show()


# In[26]:


categories2 = top_categories2.groupby(['category_name'])['region_name'].unique().reset_index()
categories2['region_name'] = categories2['region_name'].apply(lambda x: ', '.join(x))
categories2 = categories2.sort_values(by='category_name')
categories2.columns = ['Category', 'Countries']
print(categories2.to_string(index=False))


# ### Conclusion Q1
# 
# Action/Adventure is the most popular category worldwide, with high views and likes. Anime/Animation and Autos & Vehicles engage audiences across multiple regions, while Entertainment is especially popular in the Middle East and Latin America. 
# Regional preferences matter like Documentary, Drama, and Education succeed in certain areas because of local interests and values.

# ## Q2: How Does the Category of a YouTube Video Correlate with the Number of Likes It Receives?
# 
# **Objective:** Assessing how a video's category affects likes, revealing its impact on audience engagement.
# 
# ### ANOVA (Analysis of Variance)
# 
# - Null Hypothesis (H₀): All categories have the same average number of likes.
# - Alternative Hypothesis (H₁): At least one category has a significantly different average number of likes.
# 

# In[29]:


from scipy.stats import f_oneway

groups = [group['like_count'].dropna() for name, group in UT_Videos_df.groupby('category_name')]

f_statistic, p_value = f_oneway(*groups)

print("F-statistic:", f_statistic)
print("p-value:", p_value)


# Due to the p-value result of 0.0831, which is higher than 0.005, I failed to reject the null hypothesis. 
# This means that , based on the current dataset, there is **no strong statistical evidence** that the number of likes differs accross video categories.
# 
# ### Correlation Analysis
# 
# In this section, we explore the relationship between video categories (a categorical variable) and like count (a numerical metric) using correlation techniques adapted for categorical data. Pearson’s correlation needs numbers, but category_name is categorical, so we can't use it directly. Instead, we apply encoding to convert categories into a format for correlation analysis.
# 
# #### Method: One-Hot Encoding + Correlation
# 
# - One-Hot Encoding:creates binary columns (1=true and 0=false)
# - Pearson  Correlation: measures linear association
# 
# 

# In[31]:


encoded = pd.get_dummies(UT_Videos_df['category_name'])
encoded['like_count'] = UT_Videos_df['like_count']

correlation_matrix = encoded.corr()
category_like_corr = correlation_matrix['like_count'].sort_values(ascending=False)

print(category_like_corr)


# Gaming, Comedy, Shorts, Music, and News & Politics are positively associated with higher like counts, although the correlation strength is weak (all values are below 0.02). This indicates that category alone has limited predictive power for the number of likes. However, these categories are slightly more likely to receive higher engagement in terms of likes compared to others.

# ### Conclusion Q2
# 
# Based on the statistical analysis conducted, there is no strong evidence to suggest that the number of likes significantly differs across video categories. The ANOVA test returned a p-value of 0.0831, which is higher than the 0.05 significance threshold. As a result, we fail to reject the null hypothesis, indicating that any observed differences in average likes across categories are not statistically significant within the current dataset.
# 
# However, the correlation analysis revealed that Gaming, Comedy, Shorts, Music, and News & Politics categories are positively associated with higher like counts. While the correlation values are weak (all below 0.02), these categories appear slightly more likely to receive higher user engagement. 
# 
# This suggests that category alone has limited predictive power for like count, and that other factors such as content title, description, or others play a more influential role in determining user engagement.

# ## Q3: Can we predict the number of likes or views a YouTube video will receive based on its description, category, or region?
# 
# **Objective**: To build a machine learning model that predict metrics (likes and  views) using *description*, *category_name* and *region_name*
# 
# I decided to Random Forest because I'm working with categorical variables and text features.
# 

# - The data has to be prepare in case I still have some empty values and to also invlude stop_words as english

# In[45]:


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_description = vectorizer.fit_transform(UT_Videos_df['description'].fillna(''))


# - Convert categorical variables into dummies variables and then I will combine them

# In[46]:


from scipy.sparse import hstack
X_category = pd.get_dummies(UT_Videos_df['category_name'])
X_region = pd.get_dummies(UT_Videos_df['region_name'])
X_combined = hstack([X_description, X_category.values, X_region.values])


# - Log transformation to compress outliers

# In[47]:


import numpy as np
y_likes = np.log1p(UT_Videos_df['like_count'])
y_views = np.log1p(UT_Videos_df['view_count'])


# Import the necessary packages, define the test set percentage, initialize the model, fit it to the training data, generate predictions, and evaluate the model using R² score, mean absolute error (MAE), and root mean squared error (RMSE).

# In[48]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np



# In[49]:


X_train, X_test, y_train, y_test = train_test_split(X_combined, y_likes, test_size=0.2, random_state=42)


# In[50]:


model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)


# In[51]:


y_pred = model.predict(X_test)


# In[52]:


print("R² Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))


# ### Conclusion Q3
# R² = 0.78 demonstrates strong predictive power, showing that it effectively captures 78% of engagement patterns based on description, category, and region.
# 

# ## Q4: How do emotions and sentiments in video descriptions relate to engagement metrics, such as likes, comments, and views? Specifically, do descriptions with emotional tones like joy and happiness result in a higher number of likes and comments?
# 
# **Objective**: To demostrative if positive emotions (e.g., joy, excitement) correlate with higher user engagement, especially in the form of likes and comments.
# 
# Description column will be cleanned from URLs, converted to lower case and punctuation will be removed

# In[54]:


UT_Videos_df['description_cleaned'] = UT_Videos_df['description'].fillna('').str.lower()


# ### Sentimental Analysis
# 
# The description will get a polarity score as *Positive* (>0.1), *Neutral*(-0.1 - 0.1) or *Negative* (<-0.1).

# In[75]:


from textblob import TextBlob

def label_sentiment(score):
    if score > 0.1:
        return 'Positive'
    elif score < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

UT_Videos_df['sentiment_score'] = UT_Videos_df['description_cleaned'].apply(lambda x: TextBlob(x).sentiment.polarity)

UT_Videos_df['sentiment_label'] = UT_Videos_df['sentiment_score'].apply(label_sentiment)

q4_summary = UT_Videos_df.groupby('sentiment_label')[['like_count', 'comment_count', 'view_count']].mean().reset_index()


# In[76]:


print(q4_summary)


# In[78]:


import pandas as pd
import matplotlib.pyplot as plt

fig, axs = plt.subplots(3, 1, figsize=(10, 12), constrained_layout=True)

axs[0].bar(q4_summary['sentiment_label'], q4_summary['like_count'], color='skyblue')
axs[0].set_title('Average Likes by Sentiment')
axs[0].set_ylabel('Average Likes')

axs[1].bar(q4_summary['sentiment_label'], q4_summary['comment_count'], color='lightgreen')
axs[1].set_title('Average Comments by Sentiment')
axs[1].set_ylabel('Average Comments')

axs[2].bar(q4_summary['sentiment_label'], q4_summary['view_count'], color='salmon')
axs[2].set_title('Average Views by Sentiment')
axs[2].set_ylabel('Average Views')

plt.suptitle('Engagement Metrics by Sentiment in Video Descriptions', fontsize=16)

plt.show()


# ### Conclusion Q4
# 
# This results provides a clear evidence that Videos with positive emotional tones have the highest average likes, comments, and views. This supports the hypothesis "Positive emotions in descriptions are associated with higher engagement".

# # Conclusion
# 

# This study investigated the patterns and drivers of engagement in YouTube’s top 50 trending videos across multiple countries, focusing on category popularity, engagement metrics, predictive modeling, and emotional tone in video descriptions.
# 
# Regional Preferences in Video Categories: the analysis confirmed that video category popularity significantly varies by region. *Action/Adventure* emerged as the most popular category globally, while *Anime/Animation* and *Autos & Vehicles* were also widely favored across diverse regions.
# 
# Correlation Between Category and Likes: although descriptive statistics suggested higher engagement for categories like Gaming, Comedy, Shorts, and Music, the ANOVA test yielded a p-value of 0.0831, indicating that differences in like counts across categories are not statistically significant.
# 
# Predicting Likes and Views: Machine learning models, particularly Random Forest Regression, demonstrated strong predictive power, achieving an R² score of 0.78. This means that 78% of the variation in likes and views can be explained by description content, region, and category.
# 
# Sentiment and Emotional Tone in Descriptions: Sentiment analysis revealed that videos with positive emotional tone (e.g., joy, excitement) had the highest average likes, comments, and views.
# 
# Across all research questions, the findings highlight the complex and multi-dimensional nature of user engagement on YouTube. While category and region shape content visibility and interest, emotional tone and metadata such as video descriptions contribute meaningfully to how audiences respond. 
# 
# These insights help shape content, marketing, and platform algorithms, making media more targeted, culturally relevant, and emotionally engaging.

# In[ ]:




