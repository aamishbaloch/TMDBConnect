
class ErrorConnectingTMDB(Exception):
    message = 'Connection to TMDB failed!'

    def __init__(self):
        super().__init__(self.message)
