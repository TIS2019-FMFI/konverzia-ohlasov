from exceptions import WrongXmlDataToParse
import xmltodict
from collections import OrderedDict
from nested_lookup import nested_lookup


class xml_handler:
    """Poskytuje funkcie na spracovanie roznych xml vstupov. """

    def __init__(self):
        self.typy_zapisov = ["text_number", "roman", "latin"]

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

    def parse_unformatted_references(self, xml):
        begin = xml.find('<oai:record>')
        end = xml.rfind('</oai:record>') + len("</oai:record>")

        records_xml = xml[begin:end]
        records_xml = records_xml.replace("</oai:record>", " ")
        records = records_xml.split("<oai:record>")

        list_of_records = []
        for i in range(1, len(records)):
            record_xml = "<record>\n" + records[i].replace("oai:", "") + "</record>\n"
            list_of_records.append(record_xml)
        return list_of_records

    def parse_references(self, xml):
        # (id_recordu, id_responseto, strana_response_to, citation_category_z_response_to)
        unformatted = self.parse_unformatted_references(xml)

        res = []
        for ref in unformatted:
            record_id = self.find_in_nested_xml(ref, 'header')[0]['identifier'][len('crepc.sk:biblio/'):]
            response_to_ids = self.find_in_nested_xml(ref, 'cross_biblio_biblio')[0]
            response_to_page = self.find_in_nested_xml(ref, 'number_from')

            if len(response_to_page) > 0:
                response_to_page = response_to_page[0]['latin']
            else:
                response_to_page = None
            if type(response_to_ids) != list:
                response_to_ids=[response_to_ids]
            for response in response_to_ids:
                if 'citation_category' in response:
                    response_to_id = response['rec_biblio']['@id']
                    response_to_category = response['citation_category']
                    res.append((record_id, response_to_id, response_to_page, response_to_category))
        return res

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
        res = self.delist(self.find_in_nested_xml(xml, 'cross_biblio_biblio'))
        for i in res:
            i=self.delist(i)
            if "@source" in i:
                return i['rec_biblio']['@id']
        return None

    def parse_full_name(self, xml):
        """ Spracuje xml obsahujuce cely nazov publikacie
        Arguments: xml {str} -- retazec s XML na spracovanie
        Returns: str -- nazov publikacie
        Raises: WrongXmlDataToParse -- nespravne data pre dane parsovanie """
        res = self.find_in_nested_xml(xml, 'title')
        index=0
        while index < len(res):
            i=res[index]
            index+=1
            if type(i)==list:
                res.extend(i[1:])
                i=i[0]
            if 'title_proper' in nested_lookup('@title_type',i):
                return " ".join(i['#text'].split())

        return None

    def parse_token(self, xml):
        """
        Ziska token z xml.
        :param xml:  pre parsovanie
        :return:  str -- token ak ho xml obsahuje inak None
        """
        if not len(self.find_in_nested_xml(xml, 'oai:resumptionToken')):
            return None
        if '#text' not in self.find_in_nested_xml(xml, 'oai:resumptionToken')[0]:
            return None
        return self.find_in_nested_xml(xml, 'oai:resumptionToken')[0]['#text']

    def parse_affiliation_ids(self, xml):
        """
                Ziska id prisluchajucich institucii z xml.
                :param xml:  pre parsovanies
                :return:  [str] -- zoznam idciek institucii
                """
        affiliations = self.find_in_nested_xml(xml, 'rec_institution')
        ids = []
        for aff in affiliations:
            if len(nested_lookup('@id', aff)):
                ids.append(nested_lookup('@id', aff)[0])
        return ids

    def parse_parent_institution_id(self, xml):
        """
                Ziska id rodica institucie z xml.
                :param xml:  pre parsovanie
                :return:  str -- id rodicovskej institucie inak None
                """
        tmp=self.delist(self.find_in_nested_xml(xml, 'cross_institution_institution'))
        if type(tmp)!=list:
            tmp=[tmp]
        for i in tmp:
            i=self.delist(i)
            if "parent_child_level" in nested_lookup('@bond_type',i):
                return self.delist(nested_lookup('rec_institution',i))['@id']
        return None

    def parse_year(self, xml):
        """
                Ziska rok z xml.
                :param xml:  pre parsovanie
                :return:  str -- rok
                """
        tmp=self.delist(self.find_in_nested_xml(xml, 'year'))
        if nested_lookup("#text",tmp):
            return nested_lookup("#text",tmp)[0]
        if len(self.find_in_nested_xml(xml, 'year')):
            return self.find_in_nested_xml(xml, 'year')[0]
        return None


    def parse_authors_ids(self, xml):
        """
                        :param xml:  pre parsovanie
                        :return:  [str] -- idcka autorov
                        """
        ids = []
        authors = self.find_in_nested_xml(xml, 'rec_person')
        for author in authors:
            ids.append(author['@id'])
        return ids

    def parse_author_name(self, xml):
        """  :param xml:  pre parsovanie
             :return:  str -- cele meno autora
                               """
        first_name = self.delist(self.find_in_nested_xml(xml, 'firstname'))
        last_name = self.delist(self.find_in_nested_xml(xml, 'lastname'))
        ret={'meno':None, 'priezvisko':None}
        if type(first_name)!=list:
            first_name=[first_name]
        if len(first_name):
                ret['meno']=first_name[0]
        if type(last_name) != list:
            last_name=[last_name]
        if len(last_name):
                ret['priezvisko']=last_name[0]
        return ret

    def parse_source_id(self, xml):
        """  :param xml:  pre parsovanie
                     :return:  str -- id zdroja
                                       """
        return self.parse_source(xml)

    def parse_source_name(self, xml):
        """  :param xml:  pre parsovanie
                     :return:  str -- nazov zdroja
                                       """
        return self.parse_full_name(xml)

    def parse_page(self, xml):
        """  :param xml:  pre parsovanie
                     :return:  str -- strana
                                       """
        res = self.delist(self.find_in_nested_xml(xml, 'cross_biblio_biblio'))
        for i in res:
            i = self.delist(i)
            if "@source" in i:
                pom=nested_lookup("number_from",i)
                if len(pom):
                    for typ in self.typy_zapisov:
                        if len(nested_lookup(typ,pom)):
                            return  nested_lookup(typ,pom)[0]
        return None

    def parse_page_to(self, xml):
        """  :param xml:  pre parsovanie
                     :return:  str -- strana
                                       """
        res = self.delist(self.find_in_nested_xml(xml, 'cross_biblio_biblio'))
        for i in res:
            i = self.delist(i)
            if "@source" in i:
                pom=nested_lookup("number_to",i)
                if len(pom):
                    for typ in self.typy_zapisov:
                        if len(nested_lookup(typ,pom)):
                            return  nested_lookup(typ,pom)[0]
        return None

    def parse_databeses_ids(self, xml):
        """  :param xml:  pre parsovanie
             :return:  [str] -- idcka databaz
                                              """
        ids = []
        databases = self.delist(self.find_in_nested_xml(xml, 'cross_biblio_database'))
        if type(databases)!=list:
            databases=[databases]
        for db in databases:
            if type(db)==list:
                db=db[0]
            ids.append(db['rec_database']['@id'])
        return ids

    def parse_database_name(self, xml):
        """  :param xml:  pre parsovanie
                            :return:  str -- nazov databazy
                                              """
        other={"nazov":None, "je_short":False}
        tmp=self.delist(self.find_in_nested_xml(xml, 'name'))
        if type(tmp)!=list:
            tmp=[tmp]
        for i in tmp:
            i = self.delist(i)
            if type(i)!=list:
                i=[i]
            if "short_name" in i[0]["@name_type"]:
                return {"nazov":i[0]["#text"], "je_short":True}
            if other['nazov'] is None:
                other['nazov']=i[0]["#text"]
                other['typ']=i[0]["@name_type"]
        return other

    def parse_publisher_id(self, xml):
        """  :param xml:  pre parsovanie
                                   :return:  str -- id vydavatela
                                                     """
        for i in self.find_in_nested_xml(xml, 'cross_biblio_institution'):
            if "publisher" in nested_lookup("@role_type",i):
                return nested_lookup("rec_institution",i)[0]['@id']
        return None

    def parse_institution_name(self, xml):
        """  :param xml:  pre parsovanie
                                           :return:  str -- nazov institucie
                """
        tmp=self.delist(self.find_in_nested_xml(xml, 'institution_name'))
        while type(tmp)==list:
            tmp=tmp[0]
        return tmp['#text']

    def parse_source_additional(self,xml):
        res = self.delist(self.find_in_nested_xml(xml, 'cross_biblio_biblio'))
        for i in res:
            i = self.delist(i)
            if "@source" in i:
                rocnik=None
                for typ in self.typy_zapisov:
                    if len(nested_lookup(typ, nested_lookup("volume", i))):
                        rocnik = nested_lookup(typ, nested_lookup("volume", i))[0]
                        break

                rok=None
                if len(nested_lookup("year",nested_lookup("date",i))):
                   rok=nested_lookup("year",nested_lookup("date",i))[0]

                cislo=None
                for typ in self.typy_zapisov:
                    if len(nested_lookup(typ,nested_lookup("issue",i))):
                        cislo=nested_lookup(typ,nested_lookup("issue",i))[0]

        return {"rocnik":rocnik,"rok":rok, "cislo":cislo}

    def parse_type(self,xml):
        akt=self.find_in_nested_xml(xml, '@form_type')
        if len(akt):
            return akt[0]
        return None

    def parse_location(self,xml):
        for i in self.find_in_nested_xml(xml, 'cross_biblio_institution'):
            if "publisher" in nested_lookup("@role_type",i):
                if len(nested_lookup("town",i)):
                    return nested_lookup("town",i)[0]
        return None
    def parse_published_year(self,xml):
        for i in self.find_in_nested_xml(xml, 'biblio_year'):
            if "published" in nested_lookup("@type",i):
                return nested_lookup("year",i)[0]['#text']
        return None

    def parse_doi(self,xml):
        for i in self.find_in_nested_xml(xml, 'digi_identifier'):
            if ("DOI" in nested_lookup("@di_type", i)) and len(nested_lookup("digi_value", i)):
                return nested_lookup("digi_value", i)[0]
        return None
    def parse_page_range_spec(self,xml):
        for i in self.find_in_nested_xml(xml, 'range'):
            if "range_specification" in i:
                return i["range_specification"]
        return None

    def delist(self,x):
        while type(x)==list and len(x)==1:
            x=x[0]
        return x

