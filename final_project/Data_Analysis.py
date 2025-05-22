from textblob import TextBlob
import pandas as pd
import plotly.express as px
UT_Videos_df = pd.read_csv('data/YouTubeTrending.Videos.csv')
print(UT_Videos_df.columns)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_description = vectorizer.fit_transform(UT_Videos_df['description'].fillna(''))

from scipy.sparse import hstack
X_category = pd.get_dummies(UT_Videos_df['category_name'])
X_region = pd.get_dummies(UT_Videos_df['region_name'])
X_combined = hstack([X_description, X_category.values, X_region.values])
import numpy as np
y_likes = np.log1p(UT_Videos_df['like_count'])
y_views = np.log1p(UT_Videos_df['view_count'])

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

X_train, X_test, y_train, y_test = train_test_split(X_combined, y_likes, test_size=0.2, random_state=42)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

print("Model training complete. Generating predictions...")

y_pred = model.predict(X_test)

print("Model evaluation metrics:")
print("R² Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))


