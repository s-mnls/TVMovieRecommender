import pandas as pd
from config import TMDB_API_KEY
import requests
from dotenv import load_dotenv
import os


class DataLoader:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.df = None

        # Load environment variables from .env file
        load_dotenv()

        # Get the token from the environment
        self.TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.TMDB_BEARER_TOKEN}"
        }

    def load_data_from_file(self):
        """Loads dataset and selects relevant columns."""
        df = pd.read_csv(self.file_path, low_memory=False)
        df = df[['name', 'genres', 'overview']]
        df.dropna(inplace=True)
        df['genres'] = df['genres'].str.lower()
        df['overview'] = df['overview'].str.lower()
        df['content'] = df['genres'] + " " + df['overview']
        self.df = df

        return self.df

    # Returns top 5000 trending movies and shows
    def get_recent_trending_data(self, media_type):
        # API request setup
        url = f"https://api.themoviedb.org/3/trending/{media_type}/day?language=en-US"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("results")  # Returns results
        else:
            print(f"Error fetching {media_type} data: {response.status_code}")
            return []
