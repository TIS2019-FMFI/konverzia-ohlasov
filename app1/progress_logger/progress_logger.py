from app1.reference import reference
class progress_logger:
    """
    Trieda zabezpecuje vypisovanie priebehu:
        1.Do konzoly postupne po krokoch.
        2.Do suboru po zavolani close.   
    """    
    def __init__(self, output_file_name,output_file_path=""):
        """Pri inicializacii dostane ako parametre meno a umiestnenie vysledneho suboru.
        Vyrobi tento subor a ulozi si ho pre buduci zapis.        
        Arguments:
            output_file_name {[str]} -- meno vysledneho suboru
        
        Keyword Arguments:
            output_file_path str -- cesta kam sa ma zapisat vysledny subor (default: {""})
        """        
        raise NotImplementedError

    def log_step(self,reference):
        """Zapise spravu o uspenom zapisani ohlasu.        
        Arguments:
            reference {reference} -- ohlas na zapisanie
        """        
        raise NotImplementedError

    def log_error(self,error):
        """Zapise spravu o chybe pri spracovani ohlasu.
        
        Arguments:
            error {exception} -- vzniknuta chyba
        """        
        raise NotImplementedError

    def close(self):
        """Zapise vsetky zostavajuce zmeny do suboru a zavrie ho. """        
        raise NotImplementedError
