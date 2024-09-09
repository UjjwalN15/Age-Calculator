from django.conf import settings
from django.core.mail import send_mail


def send_email_for_agecalculation(email, age, name, dob):
    subject = f'From Age Calculator'
    message = (
        f'Hi {name}, \n\n'
        f'Thank you for using our age calculator system '
        f'Your date of birth is {dob} and your calculated age is {age} years.\n'
        f'Have a good day.\n\n'
        f'Thank you,\n'
        f'The Age Calculator Team'
    )
    from_email = settings.EMAIL_HOST
    send_mail(subject, message, from_email, [email])