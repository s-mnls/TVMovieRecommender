import pandas as pd

from src.TMDB_API import *
from src.TMDB_API.TMDBClient import get_data_path


class DataLoader:
    def __init__(self):
        self.client = TMDBClient()
        self.processor = DataProcessor()
        try:
            file_path = get_data_path('titles-movie.csv')
            self.movie_df = pd.read_csv(file_path, low_memory=False, on_bad_lines='skip')
        except FileNotFoundError:
            self.load_filtered_data('movie')

        try:
            file_path = get_data_path('titles-tv.csv')
            self.tv_df = pd.read_csv(file_path, low_memory=False, on_bad_lines='skip')
        except FileNotFoundError:
            self.load_filtered_data('tv')

    def load_trending_data(self, media_type):
        """Loads trending data and processes genre mappings."""
        data = self.client.fetch_trending_data(media_type)
        if not data:
            return None

        self.processor.load_genres()
        df = pd.DataFrame(data)
        df["genre_names"] = df["genre_ids"].apply(self.processor.map_genres)

        df.to_csv(get_data_path("")+"/"+f"titles-{media_type}.csv", index=False)
        print(f"Saved {len(df)} {media_type} records to titles-{media_type}.csv")

        if media_type == "movie":
            self.movie_df = df
        else:
            self.tv_df = df

        return df

    def load_filtered_data(self, filter_option="both"):
        """Loads and combines filtered datasets."""
        if filter_option in ["both", "movie"] and self.movie_df is None:
            self.movie_df = self.load_trending_data("movie")

        if filter_option in ["both", "tv"] and self.tv_df is None:
            self.tv_df = self.load_trending_data("tv")

        filter_map = {
            "movie": self.movie_df,
            "tv": self.tv_df,
            "both": pd.concat([self.movie_df, self.tv_df], ignore_index=True)
        }

        return filter_map.get(filter_option, None)
