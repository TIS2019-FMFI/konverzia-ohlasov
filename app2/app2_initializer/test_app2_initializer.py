import pytest
from app2.app2_initializer.app2_initializer import app2_initializer
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        app2_initializer([])