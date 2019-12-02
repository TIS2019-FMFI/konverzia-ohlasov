import pytest
from app1.references_manager.exceptions import WrongXmlDataToParse
from app1.references_manager.xml_handler.xml_handler import xml_handler
def test_example1():
    assert 5==5

def test_example2():
    with pytest.raises(NotImplementedError):
        xml_handler()