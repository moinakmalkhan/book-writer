import threading
from django.core.mail import send_mail
from django.conf import settings

def send_email(message,  recipient_list):
    subject = "Reset your password"
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, recipient_list)


def send_email_threaded(message, recipient_list):
    email_thread = threading.Thread(target=send_email, args=(message, recipient_list))
    email_thread.start()

