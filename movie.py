"""Movie class created"""


class Movie:
    """Create a class for a movie instance with associated attributes"""

    def __init__(self, title="", year=0, category="", is_watched=False):
        """Initialise a movie class instance."""
        self.title = title
        self.year = year
        self.category = category
        self.is_watched = is_watched


    def __str__(self):
        """Method to return a formatted string of movie details"""
        return "{} ({} from {})".format(self.title, self.category, self.year)

    def mark_watched(self):
        """Check Boolean for watch status (True) of movie if watched and print '*' """
        if self.is_watched is True:
            return "{}, {}, {}, {}".format(self.title, self.year, self.category, "*")
        
        self.is_watched = True
        return "{}, {}, {}, {}".format(self.title, self.year, self.category, "")

    def mark_unwatched(self):
        """Check Boolean for watch status of movie is False for unwatched movie"""
        if self.is_watched is False:
            return "{}, {}, {}, {}".format(self.title, self.year, self.category, "")
        
        self.is_watched = False
        return "{}, {}, {}, {}".format(self.title, self.year, self.category, "*")

