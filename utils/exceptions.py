class RequestMethodNotImplemented(Exception):
    """
    Raised when request is sent with not implemented method e.g. DELETE
    """
    pass


class ServerError(Exception):
    """
    Raised when there was an error while sending request or receiving its response
    """
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"Server returned bad response with status code: {self.status_code}"
