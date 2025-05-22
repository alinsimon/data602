#In this part I will create a dictionary to load the environment variables from the .env file
from pymongo import ASCENDING

def load_env_variables():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    env_variables= {}
    env_variables["API"] = os.getenv("API_KEY")
    env_variables["ENV"] = os.getenv("ENVIRONMENT")
    env_variables["MongoClient"] = os.getenv("MONGODB_URL")
    return env_variables

def connect_to_mongo(mongo_url,db_name, collection_name):
    from pymongo import MongoClient
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[collection_name]
    return collection

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

def load_csv_file(file_path):
    import pandas as pd
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Main function:
if __name__ == "__main__":
    api_key = load_env_variables().get('API')
    env  = load_env_variables().get('ENV')
    MongoClient = load_env_variables().get('MongoClient')
    db_name = 'YouTubeTrending'
    collection_name = 'Videos'
    client = connect_to_mongo(MongoClient, db_name, collection_name)
    #client.create_index([('video_id', ASCENDING)], unique=True)
    #trending_videos_response = get_youtube_trending_videos(api_key, region_code='US', max_results=1000)
    #client.insert_many(trending_videos_response, ordered=False)

    collection_name2 = 'Videos_Categories'
    client2 = connect_to_mongo(MongoClient, db_name, collection_name2)
    #category_dict = get_video_category(api_key, region_code='US')
    #client2.insert_many(list(category_dict.values()))

    collection_name3 = 'Videos_Regions'
    client3 = connect_to_mongo(MongoClient, db_name, collection_name3)
    regions_list = get_available_regions(api_key)
    #client3.insert_many(regions_list)

    # Load CSV file
    file_path = 'data/YouTubeTrending.Videos_Regions.csv'
    csv_data = load_csv_file(file_path)
    for(index, row) in csv_data.iterrows():
        region_code =row['id']
        print(f"Current Region: {region_code}")
 #      trending_videos_response = get_youtube_trending_videos(api_key, region_code=region_code, max_results=1000)
 #      if trending_videos_response:
 #        client.insert_many(trending_videos_response, ordered=False)
 #      else:
 #          print(f"No data found for region: {region_code}")

#Now I want to also get the categories based on the region code
    for(index, row) in csv_data.iterrows():
        region_code =row['id']
        print(f"Current Region: {region_code}")
        category_dict = get_video_category(api_key, region_code=region_code)
        if category_dict:
            client2.insert_many(list(category_dict.values()))
        else:
            print(f"No categories found for region: {region_code}")

