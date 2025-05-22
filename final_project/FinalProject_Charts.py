#import csv file
import pandas as pd
df = pd.read_csv('data/YouTubeTrending.Videos.csv')
UT_Videos_df = df
print(df.columns)
import plotly.express as px

top_category_region = (
    UT_Videos_df.groupby(['category_name', 'region_name'])['view_count']
    .sum()
    .reset_index()
)

region_name_totals = (
    top_category_region.groupby('region_name')['view_count']
    .sum()
    .sort_values(ascending=False)
)

top_10_regions = region_name_totals.head(10).index.tolist()

filtered_data = top_category_region[top_category_region['region_name'].isin(top_10_regions)]

fig = px.bar(
    filtered_data,
    x='region_name',
    y='view_count',
    color='category_name',
    title='Top 10 Trending Categories by View Count (Stacked by Region)',
    labels={'category_name': 'Category', 'view_count': 'Total Views', 'region_name': 'Region'},
    barmode='stack',
    category_orders={'region_name': top_10_regions}  # Force order by total views
)

fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828'),
    legend_title_text='category_name'
)

fig.show()
###
top_regions = (
    df.groupby('region_name')['view_count']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    top_regions,
    x='region_name',
    y='view_count',
    title='Total Views by Region',
    labels={'region_name': 'Region', 'view_count': 'Total Views'},
    color_discrete_sequence=['#FF0000']
)
fig2.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828')
)
fig2.show()

fig3 = px.scatter(
    df,
    x='like_count',
    y='view_count',
    color='category_name',
    title='Views vs Likes Colored by Category',
    labels={'like_count': 'Likes', 'view_count': 'Views', 'category_name': 'Category'},
    hover_data=['title', 'channel_title']
)
fig3.show()

category_summary = (
    df.groupby('category_name')[['view_count', 'like_count','comment_count']]
    .sum()
    .sort_values(by='view_count', ascending=False)
    .head(10)
    .reset_index()
)
print(category_summary)
import plotly.graph_objects as go

fig4 = go.Figure()

fig4.add_trace(go.Bar(
    x=category_summary['category_name'],
    y=category_summary['view_count'],
    name='Total Views',
    marker_color='#FF0000' ,
    text=category_summary['view_count'],
    textposition='outside'
))

# Add Like Count bar
fig4.add_trace(go.Bar(
    x=category_summary['category_name'],
    y=category_summary['like_count'],
    name='Total Likes',
    marker_color='#282828',
    text=category_summary['like_count'],
    textposition='outside'
))
# Add Comment Count bar
fig4.add_trace(go.Bar(
    x=category_summary['category_name'],
    y=category_summary['comment_count'],
    name='Total Comments',
    marker_color='rosybrown' ,
    text=category_summary['comment_count'],
    textposition='outside'
))

fig4.update_layout(
    title='Top 10 Trending Categories by View Count and Like Count',
    xaxis_title='Category',
    yaxis_title='Count',
    barmode='group',
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#282828'),
    legend=dict(title=None)
)

fig4.show()
