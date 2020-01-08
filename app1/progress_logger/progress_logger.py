#from app1.reference.reference import reference
#from app1.reference.exceptions import MissingDataException
#from app1.references_manager.exceptions import CrepConnectionError, WrongXmlDataToParse

class progress_logger:
    """
    Trieda zabezpecuje vypisovanie priebehu:
        1.Do konzoly postupne po krokoch.
        2.Do suboru po zavolani close.   
    """    
    def __init__(self, output_file_name,output_file_path):
        """Pri inicializacii dostane ako parametre meno a umiestnenie vysledneho suboru.
        Vyrobi tento subor a ulozi si ho pre buduci zapis.        
        Arguments:
            output_file_name {[str]} -- meno vysledneho suboru
        
        Keyword Arguments:
            output_file_path str -- cesta kam sa ma zapisat vysledny subor (default: {""})
        """        

        file_with_path = output_file_path + output_file_name
        self.file = open(file_with_path, 'a')
        #TODO ak sa bude appendovat tak nejaku halvicku na zaciatok
        self.buffer = ""

    def log_step(self,reference):
        """Zapise spravu o uspenom zapisani ohlasu.        
        Arguments:
            reference {reference} -- ohlas na zapisanie
        """        
        output = "Ohlas: " + reference.__str__() + "sa úspešne zapísal." 
        print(output )
        self.buffer += output + "\n"

    def log_error(self,error):
        """Zapise spravu o chybe pri spracovani ohlasu.
        
        Arguments:
            error {exception} -- vzniknuta chyba
        """        
        output = error.__str__() #este nejake info
        print(output)
        self.buffer += "error" + "\n"


    def close(self):
        """Zapise vsetky zostavajuce zmeny do suboru a zavrie ho. """        
        self.file.write(self.buffer)
        self.file.close()
