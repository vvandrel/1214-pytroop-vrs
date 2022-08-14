class MovieGenre:

    def __init__(self):
        self.id = 0
        self.name = ''

    def __str__(self):
        return '[id: ' + str(self.id) + ', ' \
                'name: ' + self.name + ', ' + ']'


class MovieKeywords:

    def __init__(self):
        self.id = 0
        self.name = ''

    def __str__(self):
        return '[id: ' + str(self.id) + ', ' \
                'name: ' + self.name + ', ' + ']'


class MovieCastData:

    def __init__(self):
        self.id = 0
        self.name = ''
        self.cast_id = 0
        self.character = ''
        self.credit_id = ''
        self.gender = -1
        self.order = 0

    def __str__(self):
        return '[id: ' + str(self.id) + ', ' \
                'name: ' + self.name + ', ' \
                'cast_id: ' + str(self.cast_id) + ', ' \
                'character: ' + self.character + ', ' \
                'credit_id: ' + self.credit_id + ', ' \
                'gender: ' + str(self.gender) + ', ' + \
                'order: ' + str(self.order) + ']'


class MovieData:

    def __init__(self):
        self.id = 0
        self.title = ''
        self.overview = ''
        self.keywords = ''
        self.genres = ''
        self.original_language = ''
        self.director = ''
        self.cast = ''
        self.status = ''

    def __str__(self):
        return '[id: ' + str(self.id) + ', ' \
                'title: ' + self.title + ', ' \
                'overview: ' + self.overview + ', ' \
                'keywords: ' + self.keywords + ', ' \
                'genres: ' + self.genres + ', ' \
                'original_language: ' + self.original_language + ', ' \
                'director: ' + self.director + ', ' \
                'cast: ' + self.cast + ', ' \
                'status: ' + self.status + ']'
