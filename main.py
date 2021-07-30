from errors import InputParameterVerificationError, ParamVerificationIsZero, ResultVerificationError
import jsonschema
import re
import json
import logging
from typing import Any, Callable
import os


def log():
    """Логирует ошибки."""
    log = logging.getLogger(__name__)
    return log


def default_state(param):
    """Просто дефолтная функция."""
    log().error('Попытки запуска исчерпаны')
    return 'Счётчик сработал'


def result_validation(user_account: dict, json_schema: Any):
    """Проверяет вилидацию json."""
    if isinstance(json_schema, dict):
        try:
            jsonschema.validate(user_account, json_schema)
            return user_account
        except (jsonschema.SchemaError, jsonschema.FormatError):
            log().error('Ошибка валидации json')
            return dict()
    else:
        with open(json_schema, 'r') as file:
            schema = json.load(file)
            try:
                jsonschema.validate(user_account, schema)
                return user_account
            except (jsonschema.SchemaError, jsonschema.FormatError) as err:
                log().error(err)
                return dict()


def input_valid_data(email: str, password: str) -> [str, str]:
    """Проверка на заполнение корректного email"""
    try:
        is_valid_email = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$').search(email)[0]
        is_valid_password = re.compile(r'^(?=.*\d)(?=.*[A-Z]).{8,}$').search(password)[0]
        return is_valid_email, is_valid_password
    except TypeError as err:
        log().error(f"Ошибка при проверки введенный строк: \n{err}")
        is_valid_email, is_valid_password = ['', '']
        return is_valid_email, is_valid_password


def valid_all(input_valid_data, result_validation, on_fail_repeat_times, default_behaviour: [Callable, None] = None):
    """Свой декаратор для проверки входных параметров, а также выходного результата"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            input_email, input_password = input_valid_data(*args)
            if bool(input_email) and bool(input_password) is True:
                if on_fail_repeat_times == 0:
                    raise ParamVerificationIsZero('Передан параметр on_fail_repeat_times равный 0')
                elif on_fail_repeat_times >= 1:
                    param, path = func(*args, **kwargs)
                    result_valid = result_validation(param, path)
                    if result_valid:
                        print('Валидация прошла успешна')
                        return result_valid
                    else:
                        for i in range(1, on_fail_repeat_times + 1):
                            result_valid = result_validation(param, path)
                            if not result_valid:
                                if (default_behaviour is None) and (i == on_fail_repeat_times):
                                    raise ResultVerificationError('Некорректный result_valid')
                                elif (bool(default_behaviour)) and (i == on_fail_repeat_times):
                                    default_state(default_behaviour)
                                    break
                else:
                    while True:
                        input_email, input_password = input_valid_data(*args, **kwargs)
                        if bool(input_email) and bool(input_password):
                            return True
            else:
                raise InputParameterVerificationError("Некорректный input_param")

        return wrapper

    return decorator


@valid_all(input_valid_data, result_validation, on_fail_repeat_times=3, default_behaviour='не ноне')
def valid_data(email, password):
    """Формирует учетную запись в виде словаря из переданных данных."""
    user_account = dict()
    user_account['email'] = email
    user_account['password'] = password
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jsonschema.json')
    return user_account, path


print(valid_data('rin_akhm@bk.ru', 'pasSword2'))
