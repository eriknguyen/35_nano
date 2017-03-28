import media
import fresh_tomato

beauty_beast = media.Movie("Beauty and the Beast", "Beauty and the beast", "poster", "https://www.youtube.com/watch?v=e3Nl_TCQXuw")
kong = media.Movie("Kong: Skull Island", "", "", "https://www.youtube.com/watch?v=44LdLqgOpjo")

# kong.show_trailer()
movies = [beauty_beast, kong]
# fresh_tomato.open_movies_page(movies)
print(media.Movie.VALID_RATINGS)
print(media.Movie.__doc__)

media.Movie.__module__ = "test"
print(media.Movie.__module__)

print(media.Movie.__dict__)
print(media.Movie.__name__)

print("=======")
print(kong.a)
kong.a = 22
print(media.Movie.a)
media.Movie.a = 33
print(kong.a)
print(media.Movie.a)