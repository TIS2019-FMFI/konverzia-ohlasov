import pytest
from app2.virtua_connector.virtua_connector import virtua_connector
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        virtua_connector()