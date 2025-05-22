import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# I will create a class connector to connect to MongoDB
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

def create_table(df):
    from tabulate import tabulate
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

def generate_histogram(data, title='Histogram', xlabel='Value', ylabel='Frequency'):
    import matplotlib.pyplot as plt
    plt.hist(data, bins=10, color='#FF0000', edgecolor='#282828')
    plt.title(title, color='#282828')
    plt.xlabel(xlabel, color='#282828')
    plt.ylabel(ylabel, color='#282828')
    plt.gcf().set_facecolor('#F9F9F9')
    plt.xticks(rotation=45)
    plt.show()

def generate_barplot(datax,datay, title='Bar Plot', xlabel='Category', ylabel='Value'):
    import matplotlib.pyplot as plt_v
    plt_v.figure(figsize=(10, 6))
    plt_v.bar(datax, datay, color='#FF0000', edgecolor='#282828')
    plt_v.title(title, color='#282828')
    plt_v.xlabel(xlabel, color='#282828')
    plt_v.ylabel(ylabel, color='#282828')
    plt_v.gcf().set_facecolor('#F9F9F9')
    plt_v.xticks(rotation=90)
    return plt_v.show()


def create_youtube_table(table_data, column_labels, bbox_position=[0.0, -0.4, 1.0, 0.3], fontsize=12):
    """
    Create a table with YouTube-inspired colors and formatting.

    Parameters:
    - table_data: Data to populate in the table (list of lists or 2D array).
    - column_labels: List of column labels.
    - bbox_position: Position of the table in the plot (default below the plot).
    - fontsize: Font size for the table text (default is 12).
    """
    # Create the table in the plot
    table = plt.table(cellText=table_data,
                      colLabels=column_labels,
                      cellLoc='center', loc='bottom',
                      bbox=bbox_position)

    # Apply YouTube color scheme and style
    table.auto_set_font_size(False)  # Disable automatic font size
    table.set_fontsize(fontsize)  # Set custom font size
    table.scale(1.2, 1.2)  # Scale table size (width, height)

    for (i, j), cell in table.get_celld().items():
        if i == 0:  # Header row
            cell.set_text_props(weight='bold', color='white')  # Bold and white text for header
            cell.set_facecolor('#FF0000')  # YouTube red for header
        else:  # Data rows
            cell.set_text_props(color='black')  # Black text for data rows
            cell.set_facecolor('#F5F5F5')  # Light gray for data rows
        cell.set_edgecolor('black')  # Black border color for cells
        cell.set_fontsize(10)  # Set font size for cell text

    return table


# Main function:
if __name__ == "__main__":
    env_variables = load_env_variables()
    mongo_url = env_variables["MongoClient"]
    db_name = env_variables["DB_NAME"]
    collection_videos = "Videos"
    collection_categories = "Videos_Categories"
    collection_regions = "Videos_Regions"

#Import Video data from MongoDB
    db_connector = DBConnector(mongo_url, db_name, collection_videos)
    videos =list(db_connector.find_all())
    df_videos = pd.DataFrame(videos)
    print(f"Total records in {collection_videos} collection: {len(df_videos)}")
    print( df_videos.iloc[:, [1,2,5,7,8,9,10,13]].head(5))

#Import Category data from MongoDB
    db_connector2 = DBConnector(mongo_url, db_name, collection_categories)
    categories = list(db_connector2.find_all())
    df_categories = pd.DataFrame(categories)
    print(f"Total records in {collection_categories} collection: {len(df_categories)}")
    print(df_categories.iloc[:, [1,2,3]].head(5))

#Import Region data from MongoDB
    db_connector3 = DBConnector(mongo_url, db_name, collection_regions)
    regions = list(db_connector3.find_all())
    df_regions = pd.DataFrame(regions)
    print(f"Total records in {collection_regions} collection: {len(df_regions)}")
    print(df_regions.iloc[:, :].head(5))

#Now I want to merge the videos and categories dataframes on category_id , first I will update the column name
    df_categories.rename(columns={'id': 'category_id'}, inplace=True)
    df_videos.rename(columns={'categoryId': 'category_id'}, inplace=True)
    UT_Videos_df = pd.merge(df_videos, df_categories[['category_id','region_code','title']]
                            , on=['category_id','region_code'],how="left",suffixes=('', '_category'))
    UT_Videos_df = UT_Videos_df.rename(columns={'title_category': 'category_name'})
    print(len(UT_Videos_df))
    print(UT_Videos_df.columns)
    print(UT_Videos_df.iloc[:, [1,2,5,7,8,9,10,13]].head(5))

#Now I want to merge the videos and regions dataframes on region_code
    df_regions.rename(columns={'gl': 'region_code'}, inplace=True)
    UT_Videos_df = pd.merge(UT_Videos_df, df_regions[['region_code','name']], on=['region_code'],how="left")
    UT_Videos_df = UT_Videos_df.rename(columns={'name': 'region_name'})

    print(len(UT_Videos_df))
    print(UT_Videos_df.columns)
    print(UT_Videos_df.iloc[:, [1,2,5,7,8,9,10,13]].head(5))

create_table(UT_Videos_df.iloc[:, [1,2,5,7,8,9,10,13]].head(5))
### **Data Type**
#UT_Videos_df.info()
#convert to int64
UT_Videos_df['view_count'] = pd.to_numeric(UT_Videos_df['view_count'], errors='coerce').fillna(0).astype('int64')
UT_Videos_df['like_count'] = pd.to_numeric(UT_Videos_df['like_count'], errors='coerce').fillna(0).astype('int64')
UT_Videos_df['comment_count'] = pd.to_numeric(UT_Videos_df['comment_count'], errors='coerce').fillna(0).astype('int64')
UT_Videos_df['favoriteCount'] = pd.to_numeric(UT_Videos_df['favoriteCount'], errors='coerce').fillna(0).astype('int64')
#I will remove favoriteCount column because it doesnt have any data
UT_Videos_df = UT_Videos_df.drop(columns=['favoriteCount'])
#UT_Videos_df.info()

######### GROUP BY CATEGORY AND REGION ############c

category_by_country = UT_Videos_df.groupby(['region_name', 'category_name']).size().unstack(fill_value=0)
#GET THE TOP 5 COUNTRY with more comments
import matplotlib.pyplot as plt2
import pandas as pd
region_comment_counts = UT_Videos_df.groupby('region_name')['comment_count'].sum()
top5_countries = region_comment_counts.nlargest(5)
category_by_country_filtered = category_by_country.loc[top5_countries.index]

category_by_country_filtered.plot(kind='bar', stacked=True, figsize=(12, 7))
plt2.title('Category Popularity Across the Top 5 Countries with More Comments')
plt2.xlabel('Country')
plt2.ylabel('Number of Videos')
plt2.xticks(rotation=0)
plt2.legend(title='Categories', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add a table below the plot
table_data = top5_countries.reset_index()[['region_name', 'comment_count']].values
column_labels = top5_countries.reset_index()[['region_name', 'comment_count']].columns
# Create table
create_youtube_table(table_data, column_labels)
plt2.tight_layout()
#plt2.show()

#GET THE TOP 5 COUNTRY with more views
import matplotlib.pyplot as plt
region_view_count = UT_Videos_df.groupby('region_name')['view_count'].sum()
top5_countries = region_view_count.nlargest(5)
category_by_country_filtered = category_by_country.loc[top5_countries.index]

category_by_country_filtered.plot(kind='bar', stacked=True, figsize=(12, 7))
plt.title('Category Popularity Across the Top 5 Countries with More Views')
plt.xlabel('Country')
plt.ylabel('Number of Videos')
plt.xticks(rotation=0)
plt.legend(title='Categories', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add a table below the plot
table_data = top5_countries.reset_index()[['region_name', 'view_count']].values
column_labels = top5_countries.reset_index()[['region_name', 'view_count']].columns
# Create table
create_youtube_table(table_data, column_labels)
plt.tight_layout()
#plt.show()


#GET THE TOP 5 COUNTRY with more likes
import matplotlib.pyplot as plt1
region_like_counts = UT_Videos_df.groupby('region_name')['like_count'].sum()
top5_countries2 = region_like_counts.nlargest(5)
category_by_country_filtered = category_by_country.loc[top5_countries2.index]

category_by_country_filtered.plot(kind='bar', stacked=True, figsize=(12, 7))
plt1.title('Category Popularity Across the Top 5 Countries with More Likes')
plt1.xlabel('Country')
plt1.ylabel('Number of Videos')
plt1.xticks(rotation=0)
plt1.legend(title='Categories', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add a table below the plot
table_data = top5_countries2.reset_index()[['region_name', 'like_count']].values
column_labels = top5_countries2.reset_index()[['region_name', 'like_count']].columns
# Create table
create_youtube_table(table_data, column_labels)
plt1.tight_layout()
#plt1.show()


################# The most popular YouTube video categories ############
#Summary of the most popular YouTube video categories using describe()
UT_Videos_df_summary_category = UT_Videos_df.groupby(['category_name']).describe()
#This is important to see the category name
UT_Videos_df_summary_category = UT_Videos_df_summary_category.reset_index()
import plotly.graph_objects as go
fig = go.Figure(data=[go.Table(
    header=dict(values=list(UT_Videos_df_summary_category.columns[0:9]),
                fill_color='#FF0000',
                align='left',
                font=dict(color='white', size=12,weight='bold'),
                line = dict(color='black', width=2)
                ),
    cells=dict(values=[UT_Videos_df_summary_category['category_name'],UT_Videos_df_summary_category['view_count']['count'], UT_Videos_df_summary_category['view_count']['mean'], UT_Videos_df_summary_category['view_count']['std'], UT_Videos_df_summary_category['view_count']['min'], UT_Videos_df_summary_category['view_count']['max'], UT_Videos_df_summary_category['view_count']['25%'], UT_Videos_df_summary_category['view_count']['50%'], UT_Videos_df_summary_category['view_count']['75%']],
               fill_color='white',
               align='left',
               font=dict(color='black', size=11),
               height=30,
               line = dict(color='black', width=2)))
])

fig.update_layout(
    title="Summary Statistics of the Top 50 Most Popular YouTube Videos by Category - Views Counts",
    title_x=0.5,  # Centers the title horizontally
    title_font=dict(size=20, color='black', family='Arial')  # Customize title font
)
fig.show()


fig2 = go.Figure(data=[go.Table(
    header=dict(values=list(UT_Videos_df_summary_category.columns[[0,9,10,11,12,13,14,15,16]]),
                fill_color='#FF0000',
                align='left',
                font=dict(color='white', size=12,weight='bold'),
                line = dict(color='black', width=2)
                ),
    cells=dict(values=[UT_Videos_df_summary_category['category_name'],UT_Videos_df_summary_category['like_count']['count'], UT_Videos_df_summary_category['like_count']['mean'], UT_Videos_df_summary_category['like_count']['std'], UT_Videos_df_summary_category['like_count']['min'], UT_Videos_df_summary_category['like_count']['max'], UT_Videos_df_summary_category['like_count']['25%'], UT_Videos_df_summary_category['like_count']['50%'], UT_Videos_df_summary_category['like_count']['75%']],
               fill_color='white',
               align='left',
               font=dict(color='black', size=11),
               height=30,
               line = dict(color='black', width=2)))
])

fig2.update_layout(
    title="Summary Statistics of the Top 50 Most Popular YouTube Videos by Category - Like Counts",
    title_x=0.5,  # Centers the title horizontally
    title_font=dict(size=20, color='black', family='Arial')  # Customize title font
)
fig2.show()


fig3 = go.Figure(data=[go.Table(
    header=dict(values=list(UT_Videos_df_summary_category.columns[[0,17,18,19,20,21,22,23,24]]),
                fill_color='#FF0000',
                align='left',
                font=dict(color='white', size=12,weight='bold'),
                line = dict(color='black', width=2)
                ),
    cells=dict(values=[UT_Videos_df_summary_category['category_name'],UT_Videos_df_summary_category['comment_count']['count'], UT_Videos_df_summary_category['comment_count']['mean'], UT_Videos_df_summary_category['comment_count']['std'], UT_Videos_df_summary_category['comment_count']['min'], UT_Videos_df_summary_category['comment_count']['max'], UT_Videos_df_summary_category['comment_count']['25%'], UT_Videos_df_summary_category['comment_count']['50%'], UT_Videos_df_summary_category['comment_count']['75%']],
               fill_color='white',
               align='left',
               font=dict(color='black', size=11),
               height=30,
               line = dict(color='black', width=2)))
])

fig3.update_layout(
    title="Summary Statistics of the Top 50 Most Popular YouTube Videos by Category - Comment Counts",
    title_x=0.5,  # Centers the title horizontally
    title_font=dict(size=20, color='black', family='Arial')  # Customize title font
)
#fig3.show()

