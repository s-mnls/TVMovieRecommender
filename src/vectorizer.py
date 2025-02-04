from sklearn.feature_extraction.text import TfidfVectorizer

class TextVectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def transform(self, text):
        """Converts text data into TF-IDF numerical vectors."""
        return self.vectorizer.fit_transform(text)

# Usage:
# vectorizer = TextVectorizer()
# tfidf_matrix = vectorizer.fit_transform(df['content'])
