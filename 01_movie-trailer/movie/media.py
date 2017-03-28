import webbrowser


class Movie():
    """ This class is to movie related information """
    VALID_RATINGS = ["G", "PG", "PG-13", "R"]
    a = 1

    def __init__(self, title, story_line, poster, trailer):
        self.title = title
        self.story_line = story_line
        self.poster_image_url = poster
        self.trailer_youtube_url = trailer

    def show_trailer(self):
        webbrowser.open(self.trailer)
