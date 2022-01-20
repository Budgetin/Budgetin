from api.utils.jwt import decode_token
from api.models.user_model import User


class CustomAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        authorization_headers = request.META.get('HTTP_AUTHORIZATION')
        if authorization_headers:
            authorization_headers = authorization_headers.split()
            bearer = authorization_headers[0]
            token = authorization_headers[1]
            user = decode_token(token)

            if bearer == "Bearer" and user:
                request.custom_user = user
        return None
