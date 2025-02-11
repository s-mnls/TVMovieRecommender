# TVMovieRecommender

A machine learning-based recommendation system for TV shows or movies.

## Table of Contents

- [Introduction](#introduction)

## Introduction

TVMovieRecommender is a Python-based application that provides personalized TV show or movie recommendations using machine learning techniques. It processes TV show or movie data, vectorizes textual information, and suggests similar shows based on user input.

## Features

- **Data Loading**: Fetches and filters TV show or movie data using TMDB API.
- **Text Processing**: Cleans and prepares textual data for analysis.
- **Vectorization**: Converts text data into numerical vectors using TF-IDF.
- **Recommendation**: Suggests TV shows or movies similar to a user-provided title.

## Future Features/Goals

- **Caching**: Ideally, I would like the program to recognize when the data becomes outdated, and replace any .csv files that need updating.
- **Language Preferences**: I would like to implement a feature that places a filter on exclusively English media or exclusively Japanese media, etc.
- **Deployment/UI**: I want to try and have this on some sort of graphical interface or website to play around and test on.

## Attribution

This project uses data from [The Movie Database (TMDb)](https://www.themoviedb.org/), but it is **not** endorsed or certified by TMDb.

<a href="https://www.themoviedb.org/">
    <img src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_2-d537fb228cf3ded904ef09b136fe3fec72548ebc1fea3fbbd1ad9e36364db38b.svg" 
         alt="Powered by TMDb" width="200">
</a>
