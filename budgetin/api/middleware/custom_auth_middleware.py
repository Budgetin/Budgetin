from api.utils.jwt import decode_token
from api.models import User

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
        else: #DEBT. delete this else block
            request.custom_user = {
                "id": 1,
                "username": "u067014",
                "display_name": "Harve Louis Marcello",
                "role": "Admin",
                "eselon": "S7B",
                "initial": "HLM"
            }
                
        return None
