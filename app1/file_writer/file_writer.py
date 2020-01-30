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
        self.CONST_RECORD_SEPARATOR = chr(29)
        self.CONST_FIELD_SEPARATOR = chr(30)
        self.CONST_SUBFIELD_SEPARATOR = chr(31)
        self.CONST_LEADER_LENGTH = 24
        self.CONST_DIRECTORY_LENGTH = 12
        self.CONST_INDICATOR_1 = ' '
        self.CONST_INDICATOR_2 = ' '

    def write_record(self, references, field035="", field008=""):
        """Zapise do suboru jeden record vo forme iso2709        
        Arguments:
            field035 -- retazec obsahujuci data do pola 035
            field008 -- retazec obsahujuci data do pola 008
            references {set(reference)} -- set ohlasov na zapisanie
            do pola 591 
        """

        if(field008 == ""):
            data_fields = self.__create_data_fields_of_record(field035, self.CONST_FIELD_008, references)
        else:
            data_fields = self.__create_data_fields_of_record(field035, field008, references)
        data_fields += self.CONST_RECORD_SEPARATOR

        leader = self.__create_leader_of_record(data_fields, references)

        result_record = leader + data_fields
        self.file.write(result_record)

    def __create_leader_of_record(self, data_fields, references):
        # information about record

        length = f'{(self.CONST_LEADER_LENGTH + len(data_fields)):05}'   #record's length
        status = 'n'
        type = 'a'
        implementation_defined = "b "
        character_coding_scheme = 'a'
        indicator_count = '2'
        subfield_code_length = '2'
        #base_address_of_data = f'{(self.CONST_LEADER_LENGTH + (self.CONST_DIRECTORY_LENGTH * (len(references) + 2))  + len(self.CONST_FIELD_SEPARATOR)):05}'  #start position data field
        base_address_of_data = f'{(self.CONST_LEADER_LENGTH + (self.CONST_DIRECTORY_LENGTH * (len(references) + 2))):05}'  #start position data field
        implementation_defined2 = "1a "
        entry_map = "4500"

        result_record = length + status + type + implementation_defined + character_coding_scheme + indicator_count + subfield_code_length + base_address_of_data + implementation_defined2 + entry_map

        return result_record

    def __create_data_fields_of_record(self, field035, field008, references):
        data_fields = ""
        directory = ""

        field008_res = self.CONST_FIELD_SEPARATOR + field008
        data_fields += field008_res
        directory += "008" + f'{len(field008_res):04}' + "00000"

        field035_res = self.CONST_FIELD_SEPARATOR + self.CONST_INDICATOR_1 + self.CONST_INDICATOR_2 + \
                       self.CONST_SUBFIELD_SEPARATOR + 'a' + field035
        data_fields += field035_res
        directory += "035" + f'{len(field035_res):04}' + f'{len(field008_res):05}'

        position = len(field008_res) + len(field035_res)
        for i in references:
            field = self.CONST_FIELD_SEPARATOR + self.CONST_INDICATOR_1 + self.CONST_INDICATOR_2 + i.to_iso2709_string()
            data_fields += field
            directory += "591" + f'{len(field):04}' + f'{position:05}'
            position += len(field)

        result = directory + data_fields + self.CONST_FIELD_SEPARATOR
        return result

    def close(self):
        """Ukonci zapis a zavrie subor.
        """
        self.file.close()
