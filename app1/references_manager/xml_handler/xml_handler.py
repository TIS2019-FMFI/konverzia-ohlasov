from app1.references_manager.exceptions import WrongXmlDataToParse
import xmltodict
from nested_lookup import nested_lookup


class xml_handler:
    """Poskytuje funkcie na spracovanie roznych xml vstupov. """

    def __init__(self):
        pass

    def parse_xml(self, xml):
        try:
            return xmltodict.parse(xml)
        except():
            return WrongXmlDataToParse

    def find_in_nested_xml(self, xml, key):
        try:
            return nested_lookup(key, self.parse_xml(xml))
        except():
            return WrongXmlDataToParse

    def parse_references(self, xml):
        """ Spracuje aktualizovane ohlasy Arguments: xml {str} -- retazec s XML na spracovanie Returns: list[dict{
        str:str}] -- zoznam slovnikov, jeden slovnik reprezentuje data z jedneho ohlasu Raises: WrongXmlDataToParse
        -- nespravne data pre dane parsovanie """
        return self.parse_xml(xml)

    def parse_author(self, xml):
        """ Spracuje xml obsahujuce meno autora Arguments: xml {str} -- retazec s XML na spracovanie Returns: str --
        meno autora """
        return self.find_in_nested_xml('author', xml)[0]

    def parse_database(self, xml):
        """ Spracuje xml obsahujuce nazov databazy Arguments: xml {str} -- retazec s XML na spracovanie Returns: str
        -- nazov databazy Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml('database', xml)[0]

    def parse_source(self, xml):
        """ Spracuje xml obsahujuce zdroj ohlasu Arguments: xml {str} -- retazec s XML na spracovanie Returns: str --
        nazov zdroju Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml('source', xml)

    def parse_full_name(self, xml):
        """ Spracuje xml obsahujuce cely nazov publikacie Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: str -- nazov publikacie Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml('full_name', xml)
