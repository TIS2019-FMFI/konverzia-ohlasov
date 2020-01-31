from reference import reference
from exceptions import MissingDataException
from exceptions import CrepConnectionError, WrongXmlDataToParse

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
        self.file = open(file_with_path, 'w',encoding='utf-8')
        #TODO ak sa bude appendovat tak nejaku halvicku na zaciatok
        self.buffer = ""

    def log_step(self,reference):
        """Zapise spravu o uspenom zapisani ohlasu.        
        Arguments:
            reference {reference} -- ohlas na zapisanie
        """        
        output = "[info] Ohlas: " + reference.__str__() + "sa úspešne zapísal."
        print(output )
        self.file.write(output+'\n')

    def log_warning(self,msg):
        output = "[warning] Ohlas: " +msg
        print(output)
        self.file.write(output + '\n')
    def log_error(self,error):
        """Zapise spravu o chybe pri spracovani ohlasu.
        
        Arguments:
            error {exception} -- vzniknuta chyba
        """        
        output = "error "+error.__str__() #este nejake info
        print(output)
        self.file.write(output+'\n')


    def close(self):
        """Zapise vsetky zostavajuce zmeny do suboru a zavrie ho. """
        self.file.close()
