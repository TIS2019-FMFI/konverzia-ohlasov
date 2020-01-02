from app1.references_manager.exceptions import CrepConnectionError
import requests

class crepc_connector:
    """trieda zabezpecujuca komunikaciu s centralnym
    registrom publikacnej cinnosti
    """    
    def __init__(self):
        pass

    def get_references(self,since,to=""):
        """ 
        Ziska novo vzniknute ohlasy       
        Arguments:
            since {str} -- datum od ktoreho sa budu ziskavat ohlasy
        
        Keyword Arguments:
            to {str} -- datum po ktory sa budu ziskavat ohlasy (default: {""})
        Returns:
            Str -- retazec obsahujuci XML so zoznamom ohlasov
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """        
        url="https://app.crepc.sk/oai/citation"
        params={"from":since,
        "verb":"ListRecords",
        "metadataPrefix":"xml-crepc2",
        "set":"24712"
        }
        if to:
            params["until"]=to
        try:
            r = requests.get(url = url, params = params)
            return r.content
        except:
            raise CrepConnectionError


    def get_author_for(self, id):
        """" 
        Ziska cele meno autora pre zadane id.      
        Arguments:
            id {str} -- id autora
        Returns:
            Str -- xml obsahujuce cele meno autora
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """
        url="https://app.crepc.sk/oai"
        params={"verb":"GetRecord",
        "metadataPrefix":"xml-crepc2",
        "identifier":"oai:crepc.sk:person/"+id
        }
        try:
            r = requests.get(url = url, params = params)
            return r.content
        except:
            raise CrepConnectionError
        
    
    def get_database_for(self, id):
        """" 
        Ziska nazov databazy pre zadane id.      
        Arguments:
            id {str} -- id databazy
        Returns:
            Str --xml obsahujuce nazov databazy
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """
        url="https://app.crepc.sk/oai"
        params={"verb":"GetRecord",
        "metadataPrefix":"xml-crepc2",
        "identifier":"oai:crepc.sk:database/"+id
        }
        try:
            r = requests.get(url = url, params = params)
            return r.content
        except:
            raise CrepConnectionError
    
    def get_source_for(self,id):
        """" 
        Ziska cely nazov zdroja pre zadane id.      
        Arguments:
            id {str} -- id zdroja
        Returns:
            Str -- xml obsahujuce cely nazov zdroja
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """
        url="https://app.crepc.sk/oai"
        params={"verb":"GetRecord",
        "metadataPrefix":"xml-crepc2",
        "identifier":"oai:crepc.sk:biblio/"+id
        }
        try:
            r = requests.get(url = url, params = params)
            return r.content
        except:
            raise CrepConnectionError
    
    def get_full_name_for(self,id):
        """" 
        Ziska cely nazov publikacie pre zadane id.      
        Arguments:
            id {str} -- id publikacie
        Returns:
            Str -- xml obsahujuce cely nazov publikacie
        Raises:
            CrepConnectionError -- ak sa neda pripojit
        """
        url="https://app.crepc.sk/oai"
        params={"verb":"GetRecord",
        "metadataPrefix":"xml-crepc2",
        "identifier":"oai:crepc.sk:biblio/"+id
        }
        try:
            r = requests.get(url = url, params = params)
            return r.content
        except:
            raise CrepConnectionError
