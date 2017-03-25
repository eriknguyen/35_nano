import media
import fresh_tomato

beauty_beast = media.Movie("Beauty and the Beast", "Beauty and the beast", "poster", "https://www.youtube.com/watch?v=e3Nl_TCQXuw")
kong = media.Movie("Kong: Skull Island", "", "", "https://www.youtube.com/watch?v=44LdLqgOpjo")

# kong.show_trailer()
movies = [beauty_beast, kong]
# fresh_tomato.open_movies_page(movies)
print(media.Movie.VALID_RATINGS)
