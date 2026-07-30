import pytest
from src.utils import elevar_quadrado


@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9)])
def test_elevar_quadrado_sucesso(test_input, expected):
    resultado = elevar_quadrado(test_input)
    assert resultado == expected