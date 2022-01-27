from django.core.mail import send_mail
from django.conf import settings
from api.utils.hit_api import get_biro_info
from api.models.biro_model import Biro

def send_email(biro_id_list, subject, body):
    email_array = []
    
    for biro_id in biro_id_list:
        curr_biro = Biro.objects.filter(id=biro_id['biro_id']).values()
        biro_info = get_biro_info(curr_biro['ithc_biro'])
        if 'err' in biro_info:
            return False
        if biro_info['biro_manager_email'] != "":
            email_array.append(biro_info['biro_manager_email'])
        if biro_info['sub_group_manager_email'] != "":
            email_array.append(biro_info['sub_group_manager_email'])
        if biro_info['group_manager_email'] != "":
            email_array.append(biro_info['group_manager_email'])
        
    #send_mail(subject, body, settings.EMAIL_HOST_USER, email_array)
    print('Sending email to: {}'.format(email_array))
    
    return True