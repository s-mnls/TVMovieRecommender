import pandas as pd
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

    '''
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
    '''

    def fetch_trending_data(self, media_type):
        # API request setup
        url = f"https://api.themoviedb.org/3/trending/{media_type}/day?language=en-US"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("results")[5000]  # Returns top 5000 results
        else:
            print(f"Error fetching {media_type} data: {response.status_code}")
            return []

    def fetch_genre_mapping(self, media_type):
        """Fetches movie and TV genres from TMDB and stores them in a dictionary."""
        genre_url = f"https://api.themoviedb.org/3/genre/{media_type}/list?language=en-US"
        genres = requests.get(genre_url, headers=self.headers).json().get("genres", [])

        # Combine movie and TV genres into one dictionary
        genre_dict = {genre["id"]: genre["name"] for genre in genres}

        # Save to CSV for future runs (optional)
        pd.DataFrame(list(genre_dict.items()), columns=["id", "name"]).to_csv("genres.csv", index=False)

        return genre_dict

    def load_genre_mapping(self, media_type):
        """Loads genre mapping from CSV if available, otherwise fetches from API."""
        try:
            df = pd.read_csv("genres.csv")
            return dict(zip(df["id"], df["name"]))
        except FileNotFoundError:
            return self.fetch_genre_mapping(media_type)

    def load_trending_data(self, media_type):
        data = self.fetch_trending_data(media_type)

        genre_data = self.fetch_genre_mapping(media_type)

        df = pd.DataFrame(data)

        # Uses Pandas .apply to efficiently match genre_ids with genre_names in genre_data
        # Normally I would have to use a for loop to loop through each movie and map each genre_id to the genre_data dictionary
        # However, given the size of the dataset, Pandas helps make this process more efficient
        df["genre_names"] = df["genre_ids"].apply(lambda ids: [genre_data.get(i, "Unknown") for i in ids])

        # Save datasets separately
        df.to_csv(f"titles-{media_type}.csv", index=False)

        return df

    def load_filtered_data(self, filter_option="both"):
        if filter_option == "both":
            if self.tv_df is None or self.movie_df is None:

        elif filter_option == "tv":
            if self.tv_df is None:

        elif filter_option == "movie":
            if self.movie_df is None:

        else:
