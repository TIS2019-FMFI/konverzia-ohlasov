class virtua_connector:
    """Zabezpecuje komunikaciu so systemom virtua.
    """    
    def __init__(self):
        raise NotImplementedError

    def insert_file_with_new(self,file):
        """Vlozi subor s novo vzniknutymi ohlasmi
        
        Arguments:
            file  -- subor na vlozenie
        
        """        
        raise NotImplementedError

    def insert_file_with_updated(self,file):
        """Vlozi subor s upravenymi ohlasmi
        
        Arguments:
            file  -- subor na vlozenie
        
        """        
        raise NotImplementedError