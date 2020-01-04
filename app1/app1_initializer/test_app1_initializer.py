import pytest
from app1.app1_initializer.app1_initializer import app1_initializer
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        app1_initializer({})