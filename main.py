from errors import (
    InputParameterVerificationError,
    ParamVerificationIsZero,
    ResultVerificationError,
)
import jsonschema
import re
import json
import logging
from typing import Any, Callable, Dict, Tuple
import os


def logger(message: str) -> None:
    """Логирует ошибки."""
    log = logging.getLogger(__name__)
    log.error(f"{message}")


def default_behaviour() -> None:
    """Просто дефолтная функция."""
    logger("Попытки запуска исчерпаны")


def result_validation(user_account: dict, json_schema: str) -> dict:
    """Проверяет вилидацию json."""
    with open(json_schema, "r") as file:
        schema = json.load(file)
        try:
            jsonschema.validate(user_account, schema)
            return user_account
        except (jsonschema.FormatError, jsonschema.ValidationError) as err:
            logger(err)
            return dict()


def input_valid_data(email: str, password: str) -> bool:
    """Проверка на заполнение корректного полей."""
    try:
        is_valid_email = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
        )
        var1 = is_valid_email.findall(email)
        is_valid_password = re.compile(r"^(?=.*\d)(?=.*[A-Z]).{8,}$")
        var2 = is_valid_password.findall(password)
        return bool(var1) and bool(var2)
    except (TypeError, AttributeError) as err:
        logger(f"Ошибка при проверки строк: \n{err}")
        return False


def valid_all(
    input_valid_data: Callable,
    result_validation: Callable,
    on_fail_repeat_times: int,
    default_behaviour: Any,
) -> Callable:
    """Декоратор с параметрами."""

    def decorator(func: Callable) -> Callable:
        """Получает результат функции Valid data."""

        def wrapper(*args: str, **kwargs: dict) -> Any:
            """Принемает параметры передаваемой функции."""
            input_email, input_password, name = args
            if input_valid_data(input_email, input_password):
                if on_fail_repeat_times == 0:
                    raise ParamVerificationIsZero(
                        "Передан параметр on_fail_repeat_times равный 0"
                    )
                elif on_fail_repeat_times >= 1:
                    param, path = func(*args, **kwargs)
                    result_valid = result_validation(param, name)
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
                                    default_behaviour()
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


@valid_all(
    input_valid_data, result_validation, on_fail_repeat_times=3, default_behaviour=None
)
def valid_data(
    email: str, password: str, schema: str = "jsonschema.json"
) -> Tuple[Dict[str, str], str]:
    """Формирует учетную запись в виде словаря из полуенных строк."""
    user_account = dict()
    user_account["email"] = email
    user_account["password"] = password
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), schema)
    return user_account, path


if __name__ == "__main__":
    valid_data("rin_ak@bk.ru", "passsSword@33", "jsonschema.json")
