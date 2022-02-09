from rest_framework.exceptions import APIException


class SheetNotFoundException(APIException):
    status_code = 400
    default_detail = "Excel sheet not found"

    def __init__(self, detail):
        self.default_detail = detail + " sheet not found"
        super(SheetNotFoundException, self).__init__()