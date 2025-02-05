import pandas as pd
import os
from TMDBClient import TMDBClient

class DataProcessor:
    def __init__(self):
        self.genre_data = None

    # Finds
    @staticmethod
    def get_data_path(filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
        directory = os.path.join(base_dir, "..", "data", filename)
        return directory

    # Combines genres from both movie and tv into one csv and loads into DataProcessor Object
    def load_genres(self):
        try:
            # Checks for any preloaded genres.csv file (may implement caching system later)
            directory = self.get_data_path("genres.csv")
            df = pd.read_csv(directory)
            self.genre_data = dict(zip(df["id"], df["name"]))
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If nothing is found it fetches for data using TMDB API
            print('No genres data found')
            client = TMDBClient()

            # Combines genres into one dictionary and saves into public attribute for later access
            genre_map = client.fetch_genre_mapping("movie")
            genre_map.update(client.fetch_genre_mapping("tv"))
            self.genre_data = genre_map

            # Stores dictionary into a DataFrame so it can be exported as a csv
            pd.DataFrame(list(genre_map.items()), columns=["id", "name"]).to_csv("genres.csv", index=False)

    # Takes input of array full of genre ids and maps them to the genre names using HashMap
    def map_genres(self, genre_ids):
        return [self.genre_data.get(i, "Unknown") for i in genre_ids]
