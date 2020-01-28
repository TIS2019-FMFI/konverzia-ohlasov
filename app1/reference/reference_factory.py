from app1.reference.reference_in_not_registered_magazine import reference_in_not_registered_magazine
from app1.reference.reference_in_registered_magazine import reference_in_registered_magazine
from app1.reference.reference_in_publication import reference_in_publication
from app1.references_manager.xml_handler.xml_handler import  xml_handler
from app1.references_manager.crepc_connector.crepc_connector import crepc_connector

class reference_factory:
    """factory pre ziskavanie instancii ohlasov
    """
    def init(self):
        self.handler = xml_handler()
        self.connector = crepc_connector()
    def get_reference(self, id591="", id035="", citation_cat="01",page="1"):
        """
        returns:
            reference: ohlas vyrobeny podla slovniku data
        """
        data={}
        record591=self.connector.get_biblio(id591)
        record035=self.connector.get_biblio(id035)
        if not self.test_affiliation(record035):
            return None
        data['name']=self.get_name(record591)
        data['category']=citation_cat
        data['year']=self.get_year(record591)
        data['author']=self.get_author(record591)
        data['source']=self.get_source(record591)
        data['page']=page
        data['field035']="oai:crepc.sk:biblio/"+id035
        if citation_cat in ["04"]:
            return reference_in_not_registered_magazine(data=data)

        if citation_cat in["01","02"]:
            data['referenceDatabase']=self.get_database(record591)
            return reference_in_registered_magazine(data=data)

        if citation_cat in["03","05","06","07","08"]:
            data['publisher']=self.get_publisher(record591)
            return reference_in_publication(data=data)



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


    def get_publisher(self,record):
        return self.handler.parse_institution_name(self.connector.get_institution(self.handler.parse_parent_institution_id(record)))

    def get_database(self,record):
        databazy=self.handler.parse_databeses_ids(record)
        ret=""
        for i in databazy:
            akt=self.handler.parse_database_name(self.connector.get_database_for(i))
            ret+=";"+akt
        return ret[1:]

    def test_affiliation(self,record):
        aff=self.handler.parse_affiliation_ids(record)
        for i in aff:
            if self.test_institution_affiliation(i):
                return True
        return False

    def test_institution_affiliation(self,id):
        if id=="24712":
            return True
        par=self.handler.parse_parent_institution_id(self.connector.get_institution(id))
        if par is not None:
            return self.test_institution_affiliation(par)
        return False