class references_manager:
    """
    Poskytuje moznosti na ziskanie ohlasov.
    """    
    def __init__(self, initializer, logger, writer):
        """
        Arguments:
            initializer {app1_initializer} -- initializer obsahujuci argumenty zo spustenia 
            logger {progress_logger} -- logger do ,ktoreho sa bude zapisovat priebeh
            writer {file_writer} -- writer do ktoreho sa zapisu ohlasy
        """        
        raise NotImplementedError

    def get_new_references(self):
        """Do writeru zadanom pri inicializacii
        zapise novovzniknute ohlasy pricom pouzije argumenty z initializer
        """        
        raise NotImplementedError

    def get_updated_references(self):
        """Do writeru zadanom pri inicializacii
        zapise upravene ohlasy pricom pouzije argumenty z initializer
        """
        raise NotImplementedError