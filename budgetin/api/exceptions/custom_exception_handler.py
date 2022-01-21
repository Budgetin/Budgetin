from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    response.data['message'] = response.data['detail']
    response.data.pop('detail')
    
    return response