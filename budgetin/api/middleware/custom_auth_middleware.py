from api.utils.jwt import decode_token
from api.models.user_model import User
from rest_framework.request import Request


class CustomAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        token = request.COOKIES.get('token')
        if token:
            user = decode_token(token)
            if user:
                request.custom_user = user
        
        return None
