class xml_handler:
    """Poskytuje funkcie na spracovanie roznych xml vstupov.
    """    
    def __init__(self):
        raise NotImplementedError

    def parse_new_references(self,xml):
        """ 
        Spracuje novo vzniknute ohlasy       
        Arguments:
            xml {str} -- retazec s XML na spracovanie
        Returns:
            list[dict{str:str}] -- zoznam slovnikov, jeden slovnik reprezentuje data z jedneho ohlasu 
        """ 
        raise NotImplementedError

    def parse_updated_references(self, xml):
        """ 
        Spracuje aktualizovane ohlasy       
        Arguments:
            xml {str} -- retazec s XML na spracovanie
        Returns:
            list[dict{str:str}] -- zoznam slovnikov, jeden slovnik reprezentuje data z jedneho ohlasu 
        """ 
        raise NotImplementedError
    
    def parse_author(self, xml):
        """ 
        Spracuje xml obsahujuce meno autora       
        Arguments:
            xml {str} -- retazec s XML na spracovanie
        Returns:
           str -- meno autora 
        """ 
        raise NotImplementedError
    
    def parse_database(self, xml):
        """ 
        Spracuje xml obsahujuce nazov databazy       
        Arguments:
            xml {str} -- retazec s XML na spracovanie
        Returns:
           str -- nazov databazy 
        """
        raise NotImplementedError
    
    def parse_source(self,xml):
        """ 
        Spracuje xml obsahujuce zdroj ohlasu       
        Arguments:
            xml {str} -- retazec s XML na spracovanie
        Returns:
           str -- nazov zdroju 
        """
        raise NotImplementedError
    
    def parse_full_name(self,xml):
        """ 
        Spracuje xml obsahujuce cely nazov publikacie      
        Arguments:
            xml {str} -- retazec s XML na spracovanie
        Returns:
           str -- nazov publikacie
        """
        raise NotImplementedError