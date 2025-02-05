from TMDBClient import TMDBClient
from DataProcessor import DataProcessor
class DataLoader:
    def __init__(self):
        self.client = TMDBClient()
        self.processor = DataProcessor()
        self.movie_df = None
        self.tv_df = None