class ExponeaTimeoutException(Exception):
    def __init__(self, message="Program did not finish in given timeout"):
        self.message = message
        super().__init__(self.message)
