from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class Recommender:
    def __init__(self, df, tfidf_matrix):
        self.df = df
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.indices = pd.Series(df.index, index=df['name']).drop_duplicates()

    def recommend(self, title, num_recommendations=5):
        """Returns a list of recommended TV shows based on a given title. default=5"""
        if title not in self.indices:
            return ["TV show not found in the dataset."]

        idx = self.indices[title]
        similarity_scores = list(enumerate(self.similarity_matrix[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
        tv_show_indices = [i[0] for i in similarity_scores]
        return self.df['name'].iloc[tv_show_indices].tolist()

# Usage:
# recommender = Recommender(df, tfidf_matrix)
# print(recommender.recommend("Breaking Bad", 5))
