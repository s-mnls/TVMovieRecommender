from src.TMDB_API import DataLoader
from vectorizer import TextVectorizer
from recommender import Recommender

class TVRecSystem:
    def __init__(self):
        """Initialize the recommendation system."""
        self.loader = DataLoader()
        self.df = None
        self.vectorizer = TextVectorizer()
        self.recommender = None
        self.column_name = None

    def load_and_process_data(self, data_filter):
        """
        Loads, processes, and vectorizes the dataset based on user preference.
        """
        print(f"Loading data for: {data_filter}...")

        # Determine column name
        self.column_name = {
            "tv": "name",
            "movie": "title",
            "both": "titles"
        }.get(data_filter, "title")  # Default to 'title' if invalid input

        df = self.loader.load_filtered_data(data_filter).copy()

        # Handle 'both' case by combining title & name
        if data_filter == 'both':
            df['titles'] = df['title'].fillna('') + df['name'].fillna('')

        # Select necessary columns
        df = df[[self.column_name, 'genre_names', 'overview', 'id', 'original_language']]

        # Create a content column for vectorization
        df.fillna({'genre_names': '', 'overview': ''}, inplace=True)  # Fill NaN values
        df['content'] = (df['genre_names'] + ' ' + df['overview']).str.lower()

        # Drop rows with missing data
        df.dropna(inplace=True)

        self.df = df

        tfidf_matrix = self.vectorizer.transform(df['content'])

        # Initialize the recommender system
        self.recommender = Recommender(df, tfidf_matrix, self.column_name)

        print("Data successfully loaded and processed.")

    def get_recommendation(self, title, num_recommendations=5):
        """
        Fetches recommendations for a given show title.
        """

        if self.df is None or self.recommender is None:
            print("Error: Data not loaded. Please run `load_and_process_data()` first.")
            return

        print(f"\nRecommended TV shows for '{title}':")
        recommendations = self.recommender.recommend(title, num_recommendations)

        for rec in recommendations:
            row = self.df[self.df[self.column_name] == rec]
            if not row.empty:
                row = row.iloc[0]
                print(f"{row[self.column_name]}: {row['overview']}\n")
            else:
                print(f"Warning: '{rec}' not found in dataset.")

    def run(self):
        """
        Main function to run the recommendation system.
        """
        data_filter = input("What would you like to filter? (tv, movie, both): ").strip().lower()
        self.load_and_process_data(data_filter)

        while True:
            show_name = input("Enter a TV show you want recommendations for (or type 'exit' to quit): ").strip()
            if show_name.lower() == 'exit':
                print("Exiting recommendation system.")
                break
            self.get_recommendation(show_name)


# Run the recommendation system
if __name__ == "__main__":
    system = TVRecSystem()
    system.run()
