class APIError(Exception):
    def __init__(self, message="Internal Server Error", status_code="500"):
        self.message = message
        self.status_code = status_code
