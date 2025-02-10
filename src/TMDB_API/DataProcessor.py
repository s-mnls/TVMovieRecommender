import pandas as pd
from src.TMDB_API.TMDBClient import TMDBClient, get_data_path

class DataProcessor:
    def __init__(self):
        self.genre_data = None

    # Combines genres from both movie and tv into one csv and loads into DataProcessor Object
    def load_genres(self):
        try:
            # Checks for any preloaded genres.csv file (may implement caching system later)
            directory = get_data_path("genres.csv")
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
            pd.DataFrame(list(genre_map.items()), columns=["id", "name"]).to_csv(get_data_path(""), index=False)

    # Takes input of array full of genre ids and maps them to the genre names using HashMap
    def map_genres(self, genre_ids):
        return [self.genre_data.get(i, "Unknown") for i in genre_ids]
