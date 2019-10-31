""" The main application"""

""" kivy modules"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ListProperty

"""Movie collection class"""
from moviecollection import MovieCollection
from movie import Movie

__author__ = 'valoyan2@gmail.com'
FILE_NAME = "movies.csv"

WATCHED_COLOR = [0, 0, 0.5, 1]  # Navy
UN_WATCHED_COLOR = [0, 0.5, 0.5, 1]  # Teal

"""
    STATES
    key is what shows on the button
    value is what variable it refers
"""
STATES = {'Year':'year', 'Title':'title', 'Category':'category', 'Watched':'is_watched'}

""" Allowed categories for adding a new movie"""
ALLOWED_CATEGORIES = ["Action", "Comedy", "Documentary", "Drama", "Fantasy", "Thriller"]

class MainApp(App):
    """ MainApp is a Kivy App for managing watched/unwatched films """
    current_state = StringProperty()
    state_codes = ListProperty()

    def build(self):
        self.initCollection()
        """ Method to save the movies when quiting..."""
        Window.bind(on_request_close=self.on_request_close)

        """ build Kivy app from the kv file """
        self.title = "Movies to Watch 2.1"
        self.root = Builder.load_file('app.kv')
        self.state_codes = sorted(STATES.keys())
        self.current_state = self.state_codes[0]
        self.update_status_label()
        return self.root

    def initCollection(self):
        """ Method to initialize movie and movie collection instances"""
        self.movie = Movie()
        self.movie_collection = MovieCollection()
        self.movie_collection.load_movies(FILE_NAME)
        self.movie_collection.sort("category")


    def change_state(self, state_code):
        """ handle change of spinner selection, output result to sort dinamic widgets """
        self.Sort(STATES[state_code])

    def update_event_label(self, text):
        self.root.ids.event_label.text = text

    def update_status_label(self):
        watched = self.movie_collection.movie_watched_count()
        unwatched = self.movie_collection.movie_unwatched_count()
        self.root.ids.status_label.text = "To watch: {}, Watched: {}".format(unwatched, watched)


    def Sort(self, key):
        """ Method to sort movies
        *when sorting key is 'watched(GUI)/is_watched(app)' it will do reverse sort """
        self.root.ids.entries_box.clear_widgets()
        if key == "is_watched":
            self.movie_collection.sort(key, reverse = True)
        else:
            self.movie_collection.sort(key)

        self.create_movie_buttons()

    def clear(self):
        """Method to clears texts and inputs"""
        self.root.ids.input_title.text = ""
        self.root.ids.input_category.text = ""
        self.root.ids.input_year.text = ""
        self.update_event_label("")
        self.root.ids.status_label.text = ""

    def add_movie(self):
        """Method to add a new movie and set the statuses"""
        title = self.root.ids.input_title.text
        category = self.root.ids.input_category.text
        year = self.root.ids.input_year.text

        if not title or not category or not year:
            self.update_event_label("All fields must be completed")
            return
        if category not in ALLOWED_CATEGORIES:
            self.update_event_label("Allowed categories are " + ", ".join(ALLOWED_CATEGORIES))
            return

        self.movie_collection.add_movie((title, year, category, False))
        self.root.ids.entries_box.clear_widgets()
        self.create_movie_buttons()

        self.root.ids.input_title.text = ""
        self.root.ids.input_category.text = ""
        self.root.ids.input_year.text = ""

    def create_movie_buttons(self):
        """
        Create the movie buttons and add them to the GUI
        """
        for movie in self.movie_collection.movies:
            # create a button for each phonebook entry
            temp_button = Button(text=str(movie))
            temp_button.bind(on_release=self.press_entry)
            temp_button.state = 'down' if movie.is_watched else 'normal'
            temp_button.movie = movie
            temp_button.background_color= WATCHED_COLOR if temp_button.state == 'down' else  UN_WATCHED_COLOR
            self.root.ids.entries_box.add_widget(temp_button)

    def press_entry(self, instance):
        """ Method to set triggered button's state (activity, color, watched),
        Method sets status about marked movie,
        Method called when movie buttons triggered on_release signal"""
        if instance.state == 'down':
            instance.state = 'normal'
        else:
            instance.state = 'down'

        name = instance.text

        if instance.state == 'down':
            instance.movie.mark_watched()
            instance.background_color= WATCHED_COLOR
            self.update_event_label("You have {} {}".format("watched", name))
        else:
            instance.movie.mark_unwatched()
            instance.background_color = UN_WATCHED_COLOR

        self.update_status_label()

    def on_request_close(self, *args, **kwargs):
        # print cd u("------closeing"*2)
        self.movie_collection.save_movies(FILE_NAME)

if __name__ == "__main__":
    MainApp().run()