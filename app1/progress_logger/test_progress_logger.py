import pytest
from app1.progress_logger.progress_logger import progress_logger
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        progress_logger("")