from errors import (
    InputParameterVerificationError,
    ParamVerificationIsZero,
    ResultVerificationError,
)
import jsonschema
import re
import json
import logging
from typing import Any, Callable
import os


def logger():
    """Логирует ошибки."""
    log = logging.getLogger(__name__)
    return log


def default_state():
    """Просто дефолтная функция."""
    logger().error("Попытки запуска исчерпаны")
    return "Счётчик сработал"


def result_validation(user_account: dict, json_schema: str) -> dict:
    """Проверяет вилидацию json."""
    with open(json_schema, "r") as file:
        schema = json.load(file)
        try:
            jsonschema.validate(user_account, schema)
            return user_account
        except (jsonschema.FormatError, jsonschema.ValidationError) as err:
            logger().error(err)
            return dict()


def input_valid_data(email: str, password: str) -> [str, str]:
    """Проверка на заполнение корректного email."""
    try:
        is_valid_email = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
        ).search(email)[0]
        is_valid_password = re.compile(
            r"^(?=.*\d)(?=.*[A-Z]).{8,}$"
        ).search(password)[0]
        return is_valid_email, is_valid_password
    except TypeError as err:
        logger().error(f"Ошибка при проверки введенный строк: \n{err}")
        is_valid_email, is_valid_password = ["", ""]
        return is_valid_email, is_valid_password


def valid_all(
        input_valid_data: Callable,
        result_validation: Callable,
        on_fail_repeat_times: int,
        default_behaviour: [Callable, None] = None) -> Any:
    """Свой декаратор для проверки входных параметров,
    а также выходного результата"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            input_email, input_password, schema = args
            is_valid_input_email, is_valid_input_password = input_valid_data(
                input_email, input_password
            )
            path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), schema)
            if bool(is_valid_input_email) and \
                    bool(is_valid_input_password) is True:
                if on_fail_repeat_times == 0:
                    raise ParamVerificationIsZero(
                        "Передан параметр on_fail_repeat_times равный 0"
                    )
                elif on_fail_repeat_times >= 1:
                    param = func(*args, **kwargs)
                    result_valid = result_validation(param, path)
                    if result_valid:
                        print("Валидация прошла успешна")
                        return result_valid
                    else:
                        for i in range(1, on_fail_repeat_times + 1):
                            result_valid = result_validation(param, path)
                            if not result_valid:
                                if (default_behaviour is None) and (
                                        i == on_fail_repeat_times
                                ):
                                    raise ResultVerificationError(
                                        "Некорректный result_valid"
                                    )
                                elif (bool(default_behaviour)) and (
                                        i == on_fail_repeat_times
                                ):
                                    default_state(default_behaviour)
                                    break
                else:
                    while True:
                        input_email, input_password = \
                            input_valid_data(*args, **kwargs)
                        if bool(input_email) and bool(input_password):
                            return True
            else:
                raise InputParameterVerificationError(
                    "Некорректный input_param")

        return wrapper

    return decorator


@valid_all(
    input_valid_data,
    result_validation,
    on_fail_repeat_times=3,
    default_behaviour=None
)
def valid_data(email: str, password: str) -> dict:
    """Формирует учетную запись в виде словаря из переданных данных."""
    user_account = dict()
    user_account["email"] = email
    user_account["password"] = password
    return user_account
