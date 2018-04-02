import requests
import json
from sac_room.settings import REDIRECT_URI
import _thread as thread
from django.core.mail import send_mail
from sac_room.settings import EMAIL_HOST_USER


def send_parallel_mail(sub,msg,to):
    thread.start_new_thread( send_mail, (sub, msg, EMAIL_HOST_USER, to) )



