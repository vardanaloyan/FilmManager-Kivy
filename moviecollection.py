"""Movie collection class"""

from operator import attrgetter
from movie import Movie
""" Python Standard modules"""
import os # included for checking existance of the movies.csv file

class MovieCollection:
    """ list of Movies """

    def __init__(self):
        self.movies = []

    def __str__(self):
        """ Return statement of required output """
        return "{}".format(self.movies)

    def load_movies(self, FILE_NAME):
        """ Method to load movies from csv file """
        if not os.path.isfile(FILE_NAME):
            return
        movie_output_file = open(FILE_NAME, "r")
        for line in movie_output_file.readlines():
            movie_string = line.strip("\n").split(",")
            if movie_string[3] == "w":
                is_watched = True
            else:
                is_watched = False
            movie = Movie(movie_string[0], int(movie_string[1]), movie_string[2], is_watched)
            self.movies.append(movie)
        movie_output_file.close()

    def add_movie(self, new_movie):
        """ Method to add a new movie """
        self.movies.append(Movie(new_movie[0], new_movie[1], new_movie[2], new_movie[3]))

    def sort(self, movie_attribute, reverse = False):
        """ Method to sort movies based on a key and then by title """
        self.movies.sort(key=attrgetter(movie_attribute, "title"), reverse=reverse)

    def movie_watched_count(self):
        """ Method to return the number of watched movies, is_watched = True (default) """
        watched_count = 0
        for line in self.movies:
            if line.is_watched:
                watched_count += 1
        return watched_count

    def movie_unwatched_count(self):
        """ Method to return the number of un_watched movies, is_watched = False """
        unwatched_count = 0
        for line in self.movies:
            if line.is_watched is False:
                unwatched_count += 1
        return unwatched_count

    def movie_count(self):
        """ Method to return the number of movies loaded into the file """
        total_movie_count = 0
        for line in self.movies:
            total_movie_count += 1
        return total_movie_count

    def save_movies(self, FILE_NAME):
        """ Method to save movies to csv file """
        with open(FILE_NAME, "w") as f:
            for movie in self.movies:
                f.write('{},{},{},{}\n'.format(movie.title, movie.year, movie.category, "w" if movie.is_watched else "u"))

    def display_movies(self):
        """ Method to print movie data formatted """
        i = 1
        for line in self.movies:
            print("{}.  {} {:<38} - {} ({})".format(i, line.is_watched, line.title, line.year,
                                                                line.category, end=""))
            i += 1
