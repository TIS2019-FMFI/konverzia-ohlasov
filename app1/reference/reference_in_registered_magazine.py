from app1.references_manager.crepc_connector import crepc_connector
from app1.references_manager.xml_handler import xml_handler

class reference_in_registered_magazine(reference):
    """Odvodena trieda od reference uchovavajuca ohlas
        z registrovaneho casopisu.
    """    
    def __init__(self, data):
        raise NotImplementedError

    def is_valid(self):
        raise NotImplementedError

    def to_iso2709_string(self):
        raise NotImplementedError
    
    def __str__(self):
        raise NotImplementedError