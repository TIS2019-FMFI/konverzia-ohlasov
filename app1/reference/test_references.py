import pytest
from app1.reference.exceptions import MissingDataException
from app1.reference.reference_factory import reference_factory
from app1.reference.reference import reference
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        reference_factory().get_reference("")