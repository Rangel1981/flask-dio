from http import HTTPStatus
from unittest.mock import patch

import pytest
from src.utils import elevar_quadrado, requires_role


@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9)])
def test_elevar_quadrado_sucesso(test_input, expected):
    resultado = elevar_quadrado(test_input)
    assert resultado == expected


def teste_requires_role_success(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "success")
    result = decorated_function()
    assert result == "success"

    


def teste_requires_role_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "success")
    result = decorated_function()
    assert result == ({"message": "User dont have permission"}, HTTPStatus.FORBIDDEN)

        