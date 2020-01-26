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
        """ Spracuje aktualizovane ohlasy
        Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: list[dict{str:str}] -- zoznam slovnikov, jeden slovnik reprezentuje data z jedneho ohlasu
        Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """

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
        """ Spracuje xml obsahujuce meno autora
        Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: str -- id autora
        Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml(xml, 'rec_person')[0]['@id']

    def parse_database(self, xml):
        """ Spracuje xml obsahujuce nazov databazy
        Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: str -- nazov databazy
        Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        return self.find_in_nested_xml(xml, 'database_id')[0]

    def parse_source(self, xml):
        """ Spracuje xml obsahujuce zdroj ohlasu
        Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: str -- id zdroju
        Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        res = self.find_in_nested_xml(xml, 'cross_biblio_biblio')
        return res[0][0]['rec_biblio']['@id']

    def parse_full_name(self, xml):
        """ Spracuje xml obsahujuce cely nazov publikacie
        Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: str -- nazov publikacie
        Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        res = self.find_in_nested_xml(xml, 'title')[0]
        return " ".join(res['#text'].split())

    def parse_token(self,xml):
        """
        Ziska token z xml.
        :param xml:  pre parsovanie
        :return:  str -- token ak ho xml obsahuje inak None
        """
        raise NotImplementedError

    def parse_affiliation_ids(self,xml):
        """
                Ziska id prisluchajucich institucii z xml.
                :param xml:  pre parsovanie
                :return:  [str] -- zoznam idciek institucii
                """
        raise NotImplementedError

    def parse_parent_institution_id(self,xml):
        """
                Ziska id rodica institucie z xml.
                :param xml:  pre parsovanie
                :return:  str -- id rodicovskej institucie inak None
                """
        raise NotImplementedError

    def parse_year(self,xml):
        """
                Ziska rok z xml.
                :param xml:  pre parsovanie
                :return:  str -- rok
                """
        raise NotImplementedError
    def parse_authors_ids(self,xml):
        """
                        :param xml:  pre parsovanie
                        :return:  [str] -- idcka autorov
                        """
        raise NotImplementedError
    def parse_author_name(self, xml):
        """  :param xml:  pre parsovanie
             :return:  str -- cele meno autora
                               """
        raise NotImplementedError

    def parse_source_id(self,xml):
        """  :param xml:  pre parsovanie
                     :return:  str -- id zdroja
                                       """
        raise NotImplementedError
    def parse_source_name(self,xml):
        """  :param xml:  pre parsovanie
                     :return:  str -- nazov zdroja
                                       """
        raise NotImplementedError

    def parse_page(self,xml):
        """  :param xml:  pre parsovanie
                     :return:  str -- strana
                                       """
        raise NotImplementedError

    def parse_databeses_ids(self,xml):
        """  :param xml:  pre parsovanie
                            :return:  [str] -- idcka databaz
                                              """
        raise NotImplementedError

    def parse_database_name(self,xml):
        """  :param xml:  pre parsovanie
                            :return:  str -- nazov databazy
                                              """
        raise NotImplementedError

    def parse_publisher_id(self,xml):
        """  :param xml:  pre parsovanie
                                   :return:  str -- id vydavatela
                                                     """
        raise NotImplementedError

    def parse_institution_name(self,xml):
        """  :param xml:  pre parsovanie
                                           :return:  str -- nazov institucie
                                                             """
        raise NotImplementedError