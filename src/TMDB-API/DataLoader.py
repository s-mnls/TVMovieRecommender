import pandas as pd

from TMDBClient import TMDBClient
from DataProcessor import DataProcessor
class DataLoader:
    def __init__(self):
        self.client = TMDBClient()
        self.processor = DataProcessor()
        self.movie_df = None
        self.tv_df = None

    def load_trending_data(self, media_type):
        """Loads trending data and processes genre mappings."""
        data = self.client.fetch_trending_data(media_type)

        if not data:
            return None

        df = pd.DataFrame(data)
        df["genre_names"] = df["genre_ids"].apply(self.processor.map_genres)

        df.to_csv(f"titles-{media_type}.csv", index=False)
        print(f"✅ Saved {len(df)} {media_type} records to titles-{media_type}.csv")

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