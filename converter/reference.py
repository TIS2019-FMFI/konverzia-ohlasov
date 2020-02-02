from exceptions import MissingDataException
from pymarc import Field
class reference():
    def __init__(self,id="-1", field035="-1", data={}):
        """Nastavi si hodnoty z data.
        Arguments:
            data {dict{str:str}} -- slovnik hodnot pre vytvorenie ohlasu.
        """
        self.id=id
        self.field035=field035
        self.data=data
        self.CONST_INDICATOR_1 = ' '
        self.CONST_INDICATOR_2 = ' '
        pass


    def to_marc_field(self):
        """
        Returns:
            Field -- Marc21 Field obsahujuce ohlas
        """
        subfields=[]
        for i in['9','d','m','n','p','r','s','t','v','x','y','g','w']:
            if i in self.data:
                subfields.append(i)
                subfields.append(self.data[i])

        field=Field(
            tag = '591',
            indicators = [self.CONST_INDICATOR_1,self.CONST_INDICATOR_2],
            subfields = subfields)
        return field

    def __str__(self):
        """
         Returns:
            [str] -- retazec reprezentujuci ohlas
        """        
        return f'Id:{self.id} kategoria:{self.data["9"]} ohlas na {self.field035} '

    def __hash__(self):
        return hash(str(self.id)+str(self.data)+self.field035)

    def __eq__(self, other):
        if type(self)!=type(other):
            return False
        if self.field035!=other.field035:
            return  False
        for i in self.data:
            if i not in other.data:
                return False
            if self.data[i]!=other.data[i]:
                return False
        return  True
