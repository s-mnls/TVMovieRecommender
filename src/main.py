from data import DataLoader
from vectorizer import TextVectorizer
from recommender import Recommender
import os

# Get the absolute path of the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the correct file path
csv_path = os.path.join(BASE_DIR, "data", "titles-modified.csv")

# Load and preprocess data
loader = DataLoader(csv_path)
df = loader.load_data()

# Vectorize text data
vectorizer = TextVectorizer()
tfidf_matrix = vectorizer.transform(df['content'])

# Create recommendation system
recommender = Recommender(df, tfidf_matrix)

# Get recommendations
tv_show_name = "Steven Universe"
print(f"Recommended TV shows for '{tv_show_name}':")
print(recommender.recommend(tv_show_name, 5))
