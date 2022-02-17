from rest_framework.exceptions import APIException


class ValidationException(APIException):
    status_code = 400
    default_detail = "Validation Error"
    
    def __init__(self, detail):
        self.default_detail = detail
        super(ValidationException, self).__init__()