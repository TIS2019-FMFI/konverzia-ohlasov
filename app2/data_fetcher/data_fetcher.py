from app2.virtua_connector import virtua_connector

class data_fetcher:
    """Podava informacie connectoru a vlozi ich do systemu.
    """    
    def __init__(self, file_path): 
        """        
        Arguments:
            file_path {str} -- cesta k suboru na vlozenie
        """           
        raise NotImplementedError

    def insert_new_references(self):
        """zacne vkladanie novo vzniknutych ohlasov
        """        
        raise NotImplementedError

    def insert_updated_references(self):
        """zacne vkladanie upravenych ch ohlasov
        """     
        raise NotImplementedError