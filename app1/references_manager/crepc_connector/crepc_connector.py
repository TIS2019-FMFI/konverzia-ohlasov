from app1.references_manager.exceptions import CrepConnectionError

class crepc_connector:
    """trieda zabezpecujuca komunikaciu s centralnym
    registrom publikacnej cinnosti
    """    
    def __init__(self):
        raise NotImplementedError

    def get_new_references(self,since,to=""):
        """ 
        Ziska novo vzniknute ohlasy       
        Arguments:
            since {str} -- datum od ktoreho sa budu ziskavat ohlasy
        
        Keyword Arguments:
            to {str} -- datum po ktory sa budu ziskavat ohlasy (default: {""})
        Returns:
            Str -- retazec obsahujuci XML so zoznamom ohlasov
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """        
        raise NotImplementedError

    def get_updated_references(self, since,to=""):
        """" 
        Ziska upravene ohlasy       
        Arguments:
            since {str} -- datum od ktoreho sa budu ziskavat ohlasy
        
        Keyword Arguments:
            to {str} -- datum po ktory sa budu ziskavat ohlasy (default: {""})
        Returns:
            Str -- retazec obsahujuci XML so zoznamom ohlasov
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """       
        raise NotImplementedError
    
    def get_author_for(self, id):
        """" 
        Ziska cele meno autora pre zadane id.      
        Arguments:
            id {str} -- id autora
        Returns:
            Str -- cele meno autora
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """       
        raise NotImplementedError
    
    def get_database_for(self, id):
        """" 
        Ziska nazov databazy pre zadane id.      
        Arguments:
            id {str} -- id databazy
        Returns:
            Str -- nazov databazy
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """
        raise NotImplementedError
    
    def get_source_for(self,id):
        """" 
        Ziska cely nazov zdroja pre zadane id.      
        Arguments:
            id {str} -- id zdroja
        Returns:
            Str -- cely nazov zdroja
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """
        raise NotImplementedError
    
    def get_full_name_for(self,id):
        """" 
        Ziska cely nazov publikacie pre zadane id.      
        Arguments:
            id {str} -- id publikacie
        Returns:
            Str -- cely nazov publikacie
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """
        raise NotImplementedError
    