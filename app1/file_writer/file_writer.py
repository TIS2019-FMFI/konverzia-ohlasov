from app1.reference.reference import reference


class file_writer:
    """Stara sa o zapisovanie ohlasov do suboru. 
    """

    def __init__(self, name, encoding="utf-8", path=""):
        """Pri inicializacii sa pripravi subor na zapisovanie.
        Arguments:
            name {str} -- nazov suboru
        
        Keyword Arguments:
            encoding {str} -- kodovanie suboru (default: {"utf-8"})
            path {str} -- cesta kde bude subor ulozeny (default: {""})
        """
        self.file = open(file=path + name, encoding=encoding, mode='w')
        self.CONST_FIELD_008 = "200127suuuuuuuuxx |   |||   |||| ||und||"
        self.CONST_RECORD_SEPARATOR = '#'

    def write_record(self, references, field035="", field008=""):
        """Zapise do suboru jeden record vo forme iso2709        
        Arguments:
            field035 -- retazec obsahujuci data do pola 035
            field008 -- retazec obsahujuci data do pola 008
            references {set(reference)} -- set ohlasov na zapisanie
            do pola 591 
        """

        leader = self.__create_leader_of_record(field035, field008, references)
        data_fields = self.__create_data_fields_of_record(field035, field008, references)

        result_record = leader + data_fields + self.CONST_RECORD_SEPARATOR
        self.file.write(result_record)

    def __create_leader_of_record(self, field035, field008, references):
        return ""

    def __create_data_fields_of_record(self, field035, field008, references):
        return ""

    def close(self):
        """Ukonci zapis a zavrie subor.
        """
        self.file.close()

