import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv

def get_data_path(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    directory = os.path.join(base_dir, "..", "..", "data", filename)
    return str(directory)

class TMDBClient:
    def __init__(self):
        env_path = get_data_path(".env")

        if not os.path.exists(env_path):
            raise FileNotFoundError(f".env not found at {env_path}")

        # Load environment variables from .env file
        load_dotenv(env_path)
        # Get the token from the environment
        self.TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

        if not self.TMDB_BEARER_TOKEN:
            raise ValueError("TMDB_BEARER_TOKEN not found in .env")

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.TMDB_BEARER_TOKEN}"
        }

    # Complies first 5000 trending entries depending on media_type
    # Adapts to pagination from API and complies with 50 request limit per second with exponential backoff
    def fetch_trending_data(self, media_type, max_results=5000):
        """Fetches trending movies or TV shows."""
        url = f"https://api.themoviedb.org/3/trending/{media_type}/day?language=en-US"

        all_results = []
        page = 1
        wait_time = 1  # Initial wait time for rate limiting

        while len(all_results) < max_results:
            response = requests.get(f"{url}&page={page}", headers=self.headers)

            if response.status_code == 200:
                results = response.json().get("results", [])
                if not results:
                    break

                all_results.extend(results)

                if len(all_results) >= max_results:
                    break

                page += 1
                time.sleep(0.1)  # Small delay to avoid hammering API

            elif response.status_code == 429:  # Rate limit hit
                print(f"Too many requests, waiting {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff

            else:
                print(f"Error fetching data from {url}: {response.status_code}")
                break

        return all_results

    def fetch_genre_mapping(self, media_type):
        """Fetches movie and TV genres from TMDB and stores them in a dictionary."""
        url = f"https://api.themoviedb.org/3/genre/{media_type}/list?language=en-US"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            genres = response.json().get("genres", [])
            genre_dict = {genre["id"]: genre["name"] for genre in genres}

            # Save to CSV for future runs (optional)
            pd.DataFrame(list(genre_dict.items()), columns=["id", "name"]).to_csv("genres.csv", index=False)

            return genre_dict
        else:
            print(f"Error fetching {media_type} genres: {response.status_code}")
            return {}