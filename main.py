from errors import InputParameterVerificationError
import re


def input_valid_data(email, password):
    """Проверка на заполнение корректного email"""
    is_valid_email = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$')
    is_valid_email = is_valid_email.fullmatch(password)
    if len(password) >= 8:
        is_valid_password = re.compile(r'^(?=.*\d)(?=.*[A-Z]).{8,}$')
        is_valid_password = is_valid_email.fullmatch(email)
    else:
        is_valid_password = None
    return is_valid_email, is_valid_password


def valid_all(input_valid_line):
    def decorator(func):
        def wrapper(*args, **kwargs):
            input_email, input_password = input_valid_line(*args, **kwargs)
            if all(input_email, input_password):
                rez = func(*args, **kwargs)
                return rez
            else:
                raise InputParameterVerificationError("Некорректный input_param")

        return wrapper

    return decorator


@valid_all(input_valid_line)
def valid_data(email, password):
    """Формирует учетную запись в виде словаря из переданных данных."""
    user_account = dict()
    user_account['email'] = email
    user_account['password'] = password
    return user_account


print(valid_data('rin_akhm@bk.ru', 'passworD33'))
