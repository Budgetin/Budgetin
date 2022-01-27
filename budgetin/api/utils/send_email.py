from django.core.mail import send_mail

def send_email(subject, body, receiver_email_list):
    # send_mail(subject, body, settings.EMAIL_HOST_USER, receiver_email_list)
    print('Sending email to: {}'.format(receiver_email_list))
    
    return True