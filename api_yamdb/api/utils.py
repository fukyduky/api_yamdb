from django.core import mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

NOREPLY_YAMDB_EMAIL = 'noreply@yamdb.app'
def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def generate_mail(to_email, code):
    subject = 'Confirmation code для YaMDB'
    to = to_email
    text_content = f'''Вы запросили confirmation code для работы с API YaMDB.\n
                        Внимание, храните его в тайне {code}'''
    mail.send_mail(
        subject, text_content,
        NOREPLY_YAMDB_EMAIL, [to],
        fail_silently=False
    )