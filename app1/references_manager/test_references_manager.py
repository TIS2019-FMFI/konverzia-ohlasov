import pytest
from app1.references_manager.references_manager import references_manager
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        references_manager(None, None, None)