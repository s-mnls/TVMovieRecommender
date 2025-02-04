import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Loads dataset and selects relevant columns."""
        df = pd.read_csv(self.file_path)
        df = df[['title', 'genres', 'overview']]
        df.dropna(inplace=True)
        df['genres'] = df['genres'].str.lower()
        df['overview'] = df['overview'].str.lower()
        df['content'] = df['genres'] + " " + df['overview']
        self.df = df

        return self.df

# Usage:
# loader = DataLoader("data/netflix_titles.csv")
# df = loader.load_data()
