from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    try:
        response.data['message'] = str(response.data['detail'])
        response.data.pop('detail')
    except:
        response.data['message'] = 'Unhandled error'
    finally:
        return response