from xml_handler import xml_handler
from crepc_connector import crepc_connector
from reference import reference

from exceptions import MissingDataException


class reference_factory:
    """factory pre ziskavanie instancii ohlasov
    """

    def __init__(self, logger):
        self.handler = xml_handler()
        self.connector = crepc_connector()
        self.logger = logger;
        self.known_inst = set()

    def get_reference(self, id591=None, id035=None, citation_cat=None, page=None):
        data = {}
        record591 = self.connector.get_biblio(id591)
        record035 = self.connector.get_biblio(id035)

        # otestovanie prislisnosti k UK
        if not self.test_affiliation(record035):
            return None

        # skontrolovanie kategorie
        if citation_cat not in ["01", "02", "03", "04", "05", "06", "07", "08"]:
            raise MissingDataException(f'Chyba citation category pre ohlas id:{id591} k id035:{id035}')

        # ziskanie typu ohlasu
        typ = self.get_type(record591, id591)

        # nastavenie citation category
        data['9'] = f'[o{citation_cat[1]}]'

        # nastavenie roku, ak je to prispevok v zborniku tak sa berie rok zborniku
        rok = None
        if typ in ['formPrispevokZbornik_conf.xml']:
            data['d'] = self.get_year(self.connector.get_biblio(self.handler.parse_source_id(record591)), id591)
        else:
            data['d'] = self.get_year(record591, id591)

        # nastavenie autorov
        data['m'] = self.get_author(record591, id591)

        # nastavenie \n pre clanky a prispevky (zborniky a monografie nemaju \n)
        if typ in ['formClanok_conf.xml', 'formPrispevokZbornik_conf.xml']:
            data['n'] = self.get_name(record591, id591)

        # nastavenie \p
        if typ in ['formMonografia_conf.xml', 'formZbornik_conf.xml']:
            # pre zbornik alebo monografiu je to jeho nazov
            data['p'] = self.get_name(record591, id591)
        else:
            # inak je to nazov zdroja
            data['p'] = self.get_source(record591, id591)
            # ak je to v casopise treba este roc...
            if typ in ['formClanok_conf.xml']:
                data['p'] = data['p'] + self.get_source_additional(record591, id591)
        doi = self.get_doi(record591)
        if doi is not None:
            if 'p' in data:
                data['p'] += ", " + doi
            else:
                data['p'] = doi

        # nastavenie \r monografia a zbornik priamo
        if typ in ['formMonografia_conf.xml', 'formZbornik_conf.xml']:
            data['r'] = self.get_publisher(record591, id591)
        # prispevok v zborniku ma vydavatelske udaje zborniku
        if typ in ['formPrispevokZbornik_conf.xml']:
            data['r'] = self.get_publisher(self.connector.get_biblio(self.handler.parse_source_id(record591)), id591)

        # clanok a prispevok ma aj stranu \s
        if typ in ['formClanok_conf.xml', 'formPrispevokZbornik_conf.xml']:
            strana = self.get_page(record591)
            range_spec = self.get_page_range_spec(record591)
            if strana is None and range_spec is None and doi is None:
                self.logger.log_warning(
                    f"Ohlas id591:{id591} nema ani doi, ani range_specification ani strany pouzivam [Nestr.]")

            if strana is None:
                data['s'] = '[Nestr.]'
            else:
                data['s'] = strana
            if range_spec is not None and strana is not None:
                data['s'] += ", " + range_spec
            if range_spec is not None and strana is None:
                data['s'] = range_spec

        # ziskanie databazy
        if citation_cat in ["01", "02"]:
            data['t'] = self.get_database(record591, id591)

        # nastavenie \w
        data['w'] = id591
        return reference(id=id591, field035="oai:crepc.sk:biblio/" + id035, data=data)

    def get_type(self, record, id):
        akt = self.handler.parse_type(record)
        if akt is None:
            raise MissingDataException(f'Nemozno ziskat typ z xml pre ohlas id:{id}')
        return akt

    def get_name(self, record, id591):
        akt = self.handler.parse_full_name(record)
        if akt is None:
            raise MissingDataException(f"Nemozno ziskat nazov ohlasu s id:{id591}")
        return akt

    def get_year(self, record, id591):
        akt = self.handler.parse_year(record)
        if akt is None:
            raise MissingDataException(f"K ohlasu id591{id591} sa nepodarilo ziskat rok.")
        return akt

    def get_author(self, record, id591):
        at = self.handler.parse_authors_ids(record)
        vys = ""
        if len(at) == 0:
            self.logger.log_warning(f"Ohlas id:{id591} nema autora pouzivam '[Anon]'.")
            return "[Anon]"
        for id in at:
            akt = self.connector.get_author_for(id)
            meno = self.handler.parse_author_name(akt)
            if meno['priezvisko'] is None:
                raise MissingDataException(f"Nemozno ziskat cele meno autora s id{id} v ohlase s id591:{id591}.")
            cele = ""
            cele += meno['priezvisko']
            if meno['meno'] is not None:
                cele += ", "+meno['meno']
            else:
                self.logger.log_warning(f"Autor id {id} nema zadane krstne meno v ohlase s id591{id591}")
            vys += " - " + cele
        return vys[3:]

    def get_source(self, record, id591):
        id = self.handler.parse_source_id(record)
        so = self.connector.get_biblio(id)
        akt = self.handler.parse_source_name(so)
        if akt is None:
            raise MissingDataException(f"K ohlasu s id591:{id591} nemozno ziskat nazov zdroja.")
        return akt

    def get_source_additional(self, record, id591):
        akt = self.handler.parse_source_additional(record)
        ret = ""
        if akt["rocnik"] is not None:
            ret += ", Roč. " + akt["rocnik"]
        if akt["cislo"] is not None:
            ret += ", Č. " + akt["cislo"]
        if akt["rok"] is not None:
            ret += ", " + akt["rok"]
        return ret

    def get_publisher(self, record, id591):
        id = self.handler.parse_publisher_id(record)
        publisher = None
        miesto = self.handler.parse_location(record)
        rok = self.handler.parse_published_year(record)
        if id is not None:
            publisher = self.handler.parse_institution_name(self.connector.get_institution(id))
        if publisher is None:
            self.logger.log_warning(f"Ohlas id591:{id591} nema vydavatela pouzivam [s.n.]")
            publisher="[s.n.]"
        if miesto is None:
            self.logger.log_warning(f"Ohlas id591:{id591} nema miesto vydanie pouzivam [S.l.]")
            miesto="[s.l.]"
        if rok is None:
            self.logger.log_warning(f"Ohlas id591:{id591} nema rok vydania pouzivam [s.a.]")
            rok="[s.a.]"
        return miesto + " : " + publisher + ", " + rok

    def get_database(self, record, id591):
        databazy = self.handler.parse_databeses_ids(record)
        ret = ""
        if len(databazy) == 0:
            raise MissingDataException(f"Pre ohlas id591:{id591} chyba spon jedna databaza.")
        for i in databazy:
            akt = self.handler.parse_database_name(self.connector.get_database_for(i))
            if akt["nazov"] is None:
                raise MissingDataException(f"Nemozno ziskat nazov databazy s id:{i} v ohlase id591:{id591}")
            if not akt["je_short"]:
                self.logger.log_warning(
                    f"K databaze id:{i} v ohlase id591:{id591} nie je short name pouzivam {akt['typ']} = '{akt['nazov']}'")
            ret += "; " + akt["nazov"]
        return ret[2:]

    def test_affiliation(self, record):
        aff = self.handler.parse_affiliation_ids(record)
        for i in aff:
            if self.test_institution_affiliation(i):
                return True
        return False

    def get_page(self, record):
        od = self.handler.parse_page(record)
        do = self.handler.parse_page_to(record)
        if od is None:
            return None
        if do is not None:
            od ="S "+ od + " - " + do
        return od

    def get_page_range_spec(self, record):
        return self.handler.parse_page_range_spec(record)

    def get_doi(self, record):
        return self.handler.parse_doi(record)

    def test_institution_affiliation(self, id):
        if id in self.known_inst:
            return True
        if id == "24712":
            return True
        par = self.handler.parse_parent_institution_id(self.connector.get_institution(id))
        if par is not None:
            if self.test_institution_affiliation(par):
                self.known_inst.add(id)
                return True
        return False
