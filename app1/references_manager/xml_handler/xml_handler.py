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

        begin = xml.find('<oai:record>')
        end = xml.rfind('</oai:record>') + len("</oai:record>")

        records_xml = xml[begin:end]
        records_xml = records_xml.replace("</oai:record>", " ")
        records = records_xml.split("<oai:record>")

        list_of_records = []
        for i in range(1, len(records)):
            record_xml = "<record>\n" + records[i].replace("oai:", "") + "</record>\n"
            list_of_records.append(xmltodict.parse(record_xml))

        return list_of_records

    def parse_author(self, xml):
        """ Spracuje xml obsahujuce meno autora Arguments: xml {str} -- retazec s XML na spracovanie Returns: str --
        meno autora """
        return self.find_in_nested_xml('author', xml)[0]

    def parse_database(self, xml):
        """ Spracuje xml obsahujuce nazov databazy Arguments: xml {str} -- retazec s XML na spracovanie Returns: str
        -- nazov databazy Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml(xml, 'database_id')[0]

    def parse_source(self, xml):
        """ Spracuje xml obsahujuce zdroj ohlasu Arguments: xml {str} -- retazec s XML na spracovanie Returns: str --
        nazov zdroju Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml(xml, 'source')[0]

    def parse_full_name(self, xml):
        """ Spracuje xml obsahujuce cely nazov publikacie Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: str -- nazov publikacie Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml(xml, 'full_name')[0]

