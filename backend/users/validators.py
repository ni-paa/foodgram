from django.core.exceptions import ValidationError

FORBIDDEN_NAME = 'me'


def validate_username(username):
    if username.lower() == FORBIDDEN_NAME:
        raise ValidationError(
            f'Использовать имя {FORBIDDEN_NAME} '
            'в качестве username запрещено.')
    return username
