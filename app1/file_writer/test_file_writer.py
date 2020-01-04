import pytest
from app1.file_writer.file_writer import file_writer
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        file_writer("").write_reference(None)