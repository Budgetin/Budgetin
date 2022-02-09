from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = 404
    default_detail = "Resource not found."

    def __init__(self, detail):
        self.default_detail = detail + " not found."
        super(NotFoundException, self).__init__()
