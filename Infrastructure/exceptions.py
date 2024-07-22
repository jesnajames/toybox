class NotFoundException(Exception):
    def __init__(self, message) -> None:
        super().__init__()
        self.error_code = 404
        self.error_description = message
    pass