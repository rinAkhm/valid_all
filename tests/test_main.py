import os
import pytest
from main import result_validation, input_valid_data, valid_data
from errors import InputParameterVerificationError, ResultVerificationError

JSONSCHEMA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'jsonschema.json')


def test_result_valid_json():
    """Проверяет result_validation."""
    assert result_validation({"email": "rin_ak@yandex.ru", "password": "QWerty@22"}, JSONSCHEMA) == {
        "email": "rin_ak@yandex.ru", "password": "QWerty@22"}
    assert result_validation({"email": "rin_ak@yandex.ru", "pasword": "QWerty@22"}, JSONSCHEMA) == dict()


def test_input_valid_data():
    """Проверяет input_valid_data."""
    assert input_valid_data("rin_ak@yandex.ru", "QWerty@22") == ("rin_ak@yandex.ru", "QWerty@22")
    assert input_valid_data("rin_yandex", "QWerty@22") == ("", "")
    assert input_valid_data("rin_akyandex.ru", "qwerty") == ("", "")
    assert input_valid_data("rin_akyandex.ru", "") == ("", "")


def test_valid_data_positive():
    """Провереяет valid_all на позитивные кейсы."""
    assert valid_data('rin_akhm@bk.ru', 'pasSword3', 'jsonschema.json') == {
        "email": "rin_akhm@bk.ru", "password": "pasSword3"}
    assert valid_data('mar_var@yandex.ru', 'Password@321', 'jsonschema.json') == {
        "email": "rin_akhm@bk.ru", "password": "pasSword3"}


def test_valid_data_negative():
    """Провереяет valid_all на негативные кейсы."""
    with pytest.raises(ResultVerificationError) as e:
        valid_data('rin_akhm@bk.ru', 'pasSword3', 'invalid_jsonschema.json')
        assert "Некорректный result_valid" in e.value

    with pytest.raises(InputParameterVerificationError) as e:
        valid_data('rin_akhmbk.ru', 'pasSword3', 'jsonschema.json')
        assert "Некорректный input_param" in e.value
