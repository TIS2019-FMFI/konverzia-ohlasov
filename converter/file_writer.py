from reference import reference
from pymarc import Record
from pymarc import Field
from pymarc import MARCWriter


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
        self.CONST_FIELD_008 = "|2018    ne || ||||   ||   ||eng |"
        self.CONST_FIELD_LEADER="nab a22001211a 4500"
        self.CONST_INDICATOR_1 = ' '
        self.CONST_INDICATOR_2 = ' '
        self.writer = MARCWriter(open(path + name, 'wb'))

    def write_record(self, references, field035="", field008=""):
        """Zapise do suboru jeden record vo forme iso2709        
        Arguments:
            field035 -- retazec obsahujuci data do pola 035
            field008 -- retazec obsahujuci data do pola 008
            references {set(reference)} -- set ohlasov na zapisanie
            do pola 591 
        """

        if(field008 == ""):
            field008 = self.CONST_FIELD_008
        record=Record(force_utf8=True)
        record.add_field(Field(tag = '008',data=field008))
        record.add_field(Field(tag = '035',indicators = [self.CONST_INDICATOR_1,self.CONST_INDICATOR_2],subfields = ['a', field035]))
        for i in references:
            record.add_field(i.to_marc_field())
        record.leader=record.leader[:5]+'n'+record.leader[6:]
        record.leader = record.leader[:7] + 'b' + record.leader[8:]
        record.leader = record.leader[:18] + 'a' + record.leader[19:]
        self.writer.write(record)

    def close(self):
        """Ukonci zapis a zavrie subor.
        """
        self.writer.close()
