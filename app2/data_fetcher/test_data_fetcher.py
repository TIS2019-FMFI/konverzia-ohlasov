import pytest
from app2.data_fetcher.data_fetcher import data_fetcher
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        data_fetcher("")