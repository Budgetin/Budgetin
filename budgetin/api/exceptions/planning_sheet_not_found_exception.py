from rest_framework.exceptions import APIException


class PlanningSheetNotFoundException(APIException):
    status_code = 400
    default_detail = "Worksheet named 'Planning' not found"
