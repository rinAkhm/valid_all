from errors import InputParameterVerificationError, ParamVerificationIsZero, ResultVerificationError
from jsonschema import validate
import re
import logging
from typing import Any


def log():
    log = logging.getLogger(__name__)
    return log


def default_behaviour():
    """Дефолтная функция"""
    return 'Счётчик сработал'


def result_validation(user_account: dict, json_schema: Any):
    if isinstance(user_account, dict):
        validate(user_account, json_schema)
        return True



def input_valid_data(email: str, password: str) -> Any:
    """Проверка на заполнение корректного email"""
    try:
        is_valid_email = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$').search(email)[0]
        is_valid_password = re.compile(r'^(?=.*\d)(?=.*[A-Z]).{8,}$').search(password)[0]
        return is_valid_email, is_valid_password
    except TypeError as err:
        log().error(f"Ошибка при проверки введенный строк: \n{err}")
        is_valid_email, is_valid_password = ['', '']
        return is_valid_email, is_valid_password


def valid_all(input_valid_line, on_fail_repeat_times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            input_email, input_password = input_valid_line(*args, **kwargs)
            if bool(input_email) and bool(input_password) is False:
                if on_fail_repeat_times == 0:
                    raise ParamVerificationIsZero('Передан параметр on_fail_repeat_times равный 0')
                elif on_fail_repeat_times >= 1:
                    raise InputParameterVerificationError("Некорректный input_param")
                elif on_fail_repeat_times < 0:
                    while True:
                        input_email, input_password = input_valid_line(*args, **kwargs)
                        if bool(input_email) and bool(input_password):
                            return True
            else:
                print(input_email, input_password)
                rez = func(*args, **kwargs)
                return rez

        return wrapper

    return decorator


@valid_all(input_valid_data, on_fail_repeat_times=1, default_behaviour=None)
def valid_data(email, password):
    """Формирует учетную запись в виде словаря из переданных данных."""
    user_account = dict()
    user_account['email'] = email
    user_account['password'] = password
    return user_account


print(valid_data('rin_akhm@bk.ru', ''))
