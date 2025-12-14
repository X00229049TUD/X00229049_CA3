from calculator import modulo
import pytest

def test_modulo_basic() -> None:
    assert modulo(5, 2) == 1.0

def test_modulo_with_floats() -> None:
    assert modulo(5.5, 2) == 1.5

def test_modulo_by_zero_raises() -> None:
    with pytest.raises(ValueError):
        modulo(5, 0)
