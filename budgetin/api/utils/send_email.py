from django.core.mail import send_mail
from django.conf import settings
from api.utils.hit_api import get_biro_info
from api.models.biro_model import Biro

def send_email(subject, body, receiver_email_list):
    # send_mail(subject, body, settings.EMAIL_HOST_USER, receiver_email_list)
    print('Sending email to: {}'.format(receiver_email_list))
    
    return True