from xml_handler import  xml_handler
from crepc_connector import crepc_connector
from reference import reference

from exceptions import MissingDataException

class reference_factory:
    """factory pre ziskavanie instancii ohlasov
    """
    def __init__(self,logger):
        self.handler = xml_handler()
        self.connector = crepc_connector()
        self.logger=logger;
        self.known_inst=set()
    def get_reference(self, id591=None, id035=None, citation_cat=None,page=None):
        data={}
        record591=self.connector.get_biblio(id591)
        record035=self.connector.get_biblio(id035)

        #otestovanie prislisnosti k UK
        if not self.test_affiliation(record035):
            return None

        #skontrolovanie kategorie
        if citation_cat not in ["01","02","03","04","05","06","07","08"]:
            raise MissingDataException('Chyba citation category pre ohlas id:{id591} k id035:{id035}')

        #ziskanie typu ohlasu
        typ = self.get_type(record591, id591)
        print(typ)

        #nastavenie citation category
        data['9']=f'[o{citation_cat[1]}]'

        #nastavenie roku, ak je to prispevok v zborniku tak sa berie rok zborniku
        if typ in ['formPrispevokZbornik_conf.xml']:
            data['d']=self.handler.parse_year(self.connector.get_biblio(self.handler.parse_source_id(record591)))
        else:
            data['d']=self.get_year(record591)

        #nastavenie autorov
        data['m']=self.get_author(record591)

        # nastavenie \n pre clanky a prispevky (zborniky a monografie nemaju \n)
        if typ in['formClanok_conf.xml', 'formPrispevokZbornik_conf.xml']:
            data['n']=self.get_name(record591)

        #nastavenie \p
        if typ in ['formMonografia_conf.xml', 'formZbornik_conf.xml']:
            #pre zbornik alebo monografiu je to jeho nazov
            data['p']=self.get_name(record591)
        else:
            #inak je to nazov zdroja
            data['p']=self.get_source(record591)
            #ak je to v casopise treba este roc...
            if citation_cat in ["01","02","03","04"]:
                data['p']=data['p']+", "+self.get_source_additional(record591)

        #nastavenie \r monografia a zbornik priamo
        if typ in ['formMonografia_conf.xml', 'formZbornik_conf.xml']:
            data['r']=self.get_publisher(record591)

        #prispevok v zborniku ma vydavatelske udaje zborniku
        if typ in ['formPrispevokZbornik_conf.xml']:
            data['r']=self.get_publisher(self.connector.get_biblio(self.handler.parse_source_id(record591)))

        #clanok a prispevok ma aj stranu \s
        if typ in ['formClanok_conf.xml', 'formPrispevokZbornik_conf.xml']:
                data['s']=f"s. {page}"

        #ziskanie databazy
        if citation_cat in ["01","02"]:
            data['t']=self.get_database(record591)

        #nastavenie \w
        data['w']=id591
        return reference(id=id591, field035=id035, data=data)


    def get_type(self,record,id):
        akt=self.handler.parse_type(record)
        if akt is None:
            raise MissingDataException(f'Nemozno ziskat typ z xml pre ohlas id:{id}')
        return akt

    def get_name(self,record):
        return self.handler.parse_full_name(record)

    def get_year(self,record):
        return self.handler.parse_year(record)

    def get_author(self,record):
        at=self.handler.parse_authors_ids(record)
        vys=""
        for id in at:
            akt =self.connector.get_author_for(id)
            meno=self.handler.parse_author_name(akt)
            vys+="-"+meno
        return vys[1:]

    def get_source(self,record):
        id=self.handler.parse_source_id(record)
        so=self.connector.get_biblio(id)
        return self.handler.parse_source_name(so)
    def get_source_additional(self,record):
        return  self.handler.parse_source_additional(record)


    def get_publisher(self,record):
        id=self.handler.parse_publisher_id(record)
        if  id is not None:
            return self.handler.parse_institution_name(self.connector.get_institution(id))
        return "n/a"

    def get_database(self,record):
        databazy=self.handler.parse_databeses_ids(record)
        print(f'databazy:{databazy}')
        ret=""
        for i in databazy:
            akt=self.handler.parse_database_name(self.connector.get_database_for(i))
            ret+="; "+akt
        return ret[2:]

    def test_affiliation(self,record):
        aff=self.handler.parse_affiliation_ids(record)
        for i in aff:
            if self.test_institution_affiliation(i):
                return True
        return False
    def get_published_location(self,record):
        return ""

    def test_institution_affiliation(self,id):
        if id in self.known_inst:
            return True
        if id=="24712":
            return True
        par=self.handler.parse_parent_institution_id(self.connector.get_institution(id))
        if par is not None:
            if self.test_institution_affiliation(par):
                self.known_inst.add(id)
                return True
        return False
