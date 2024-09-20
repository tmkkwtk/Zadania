class Movies:
    def __init__(self, title, year, genre, play_count):
        self.title = title
        self.year = year
        self.genre = genre
        self.play_count = play_count

    def play(self):
        self.play_count += 1

    def __str__(self):
        return f"{self.title} ({self.year})"


class Series(Movies):
    def __init__(self, number_of_series, number_of_episode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number_of_series = number_of_series
        self.number_of_episode = number_of_episode

    def __str__(self):
        return f"{self.title} S{str(self.number_of_series).zfill(2)}E{str(self.number_of_episode).zfill(2)}"


def fulfill():

    library = []

    library.append(Movies("Pulp Fiction", 1994, "crime film", 1))
    library.append(Movies("The Shawshank Redemption", 1994, "drama", 1))
    library.append(Movies("The Dark Knight", 2008, "action", 1))

    library.append(
        Series(
            title="The Simpsons",
            year=1989,
            genre="animated sitcom",
            play_count=1,
            number_of_series=1,
            number_of_episode=1,
        )
    )
    library.append(
        Series(
            title="Game of Thrones",
            year=2011,
            genre="fantasy",
            play_count=1,
            number_of_series=1,
            number_of_episode=1,
        )
    )
    library.append(
        Series(
            title="Breaking Bad",
            year=2008,
            genre="thriller",
            play_count=1,
            number_of_series=1,
            number_of_episode=1,
        )
    )

    return library


def get_movies():
    movies = sorted(
        [
            movie
            for movie in library
            if isinstance(movie, Movies) and not isinstance(movie, Series)
        ],
        key=lambda movie: movie.title,
    )
    for movie in movies:
        print(movie)


def get_series():
    series = sorted(
        [one_series for one_series in library if isinstance(one_series, Series)],
        key=lambda one_series: one_series.title,
    )
    for one_series in series:
        print(one_series)


def search(keyword):
    findings = []
    for work in library:
        if keyword.lower() in work.title.lower():
            findings.append(work)
    for find in findings:
        print(find)


def generate_views():
    import random

    choice = random.choice(library)
    for i in range(random.randint(1, 100)):
        choice.play()


def generate_views_x_times(x=10):
    for i in range(x):
        generate_views()


def top_titles(how_many, content_type):
    from datetime import date

    if content_type.lower() == "series":
        print(f"Najpopularniejsze seriale dnia {date.today()} ")
        top_list = sorted(
            [work for work in library if isinstance(work, Series)],
            key=lambda work: work.play_count,
            reverse="True",
        )
    else:
        print(f"Najpopularniejsze filmy dnia {date.today()} ")
        top_list = sorted(
            [work for work in library if isinstance(work, Movies)],
            key=lambda work: work.play_count,
            reverse="True",
        )
    for x in range(how_many):
        print(vars(top_list[x]))


if __name__ == "__main__":
    print("Biblioteka filmów")
    library = fulfill()
    generate_views_x_times()
    top_titles(3, "movies")
    top_titles(3, "series")
