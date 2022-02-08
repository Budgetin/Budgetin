from distutils.command.config import config
from django.core.mail import send_mail

def send_email(subject, body, receiver_email_list):
    # send_mail(subject, body, from_email = 'noreply.budgetin@dti.co.id', receiver_email_list)
    send_mail(
        subject = subject, 
        message = body, 
        from_email = config('EMAIL_HOST_USER'), 
        recipient_list=receiver_email_list)
    print('Sending email to: {}'.format(receiver_email_list))
    
    return True