from app1.reference import reference
class file_writer:
    """Stara sa o zapisovanie ohlasov do suboru. 
    """    
    def __init__(self,name,encoding="utf-8", path=""):
        """Pri inicializacii sa pripravi subor na zapisovanie.
        Arguments:
            name {str} -- nazov suboru
        
        Keyword Arguments:
            encoding {str} -- kodovanie suboru (default: {"utf-8"})
            path {str} -- cesta kde bude subor ulozeny (default: {""})
        """                
        raise NotImplementedError

    def write_reference(self, reference):
        """Zapise do suboru jeden ohlas vo forme iso2709        
        Arguments:
            reference {reference} -- ohlas na zapisanie
        """        
        raise NotImplementedError

    def close(self):
        """Ukonci zapis a zavrie subor.
        """        
        raise NotImplementedError