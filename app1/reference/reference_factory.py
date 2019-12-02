from app1.reference.reference_in_not_registered_magazine import reference_in_not_registered_magazine
from app1.reference.reference_in_registered_magazine import reference_in_registered_magazine
from app1.reference.reference_in_publication import reference_in_publication


class reference_factory:
    """factory pre ziskavanie instancii ohlasov
    """    
    def get_reference(self, data):
        """
        Arguments:
            data {dict{str:str}} -- slovnik hodnot pre vytvorenie ohlasu
        
        returns:
            reference: ohlas vyrobeny podla slovniku data
        """        
        raise NotImplementedError