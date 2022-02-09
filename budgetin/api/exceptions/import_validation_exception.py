from rest_framework.exceptions import APIException


class ImportValidationException(APIException):
    status_code = 400
    default_detail = "Inconsistent data found"
    
    def __init__(self, detail):
        self.default_detail = detail
        super(ImportValidationException, self).__init__()
