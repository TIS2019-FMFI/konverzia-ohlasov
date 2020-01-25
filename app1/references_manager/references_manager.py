import datetime

from app1.reference.exceptions import *
from app1.reference.reference import reference
from app1.reference.reference_factory import reference_factory
from app1.references_manager.crepc_connector.crepc_connector import crepc_connector
from app1.references_manager.exceptions import *
from app1.references_manager.xml_handler.xml_handler import xml_handler


class references_manager:
    """
    Poskytuje moznosti na ziskanie ohlasov.
    """

    def __init__(self, initializer, logger, writer):
        """
        Arguments:
            initializer {app1_initializer} -- initializer obsahujuci argumenty zo spustenia 
            logger {progress_logger} -- logger do ,ktoreho sa bude zapisovat priebeh
            writer {file_writer} -- writer do ktoreho sa zapisu ohlasy
        """
        self.initializer = initializer
        self.logger = logger
        self.writer = writer

    def get_references(self):
        """Do writeru zadanom pri inicializacii
        zapise vzniknute ohlasy pricom pouzije argumenty z initializer
        """
        connector = crepc_connector()
        handler = xml_handler()
        start = self.initializer.from_date
        end = self.initializer.to_date


        try:
            all_xml = connector.get_references(since=start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                               to=aktend.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            ohlasy_list = handler.parse_references(all_xml)
            references = set()
            references.update(ohlasy_list)
            token=handler.parse_token(all_xml)
            while  token is not None:
                all_xml = connector.get_references_with_token(token)
                ohlasy_list=handler.parse_references(all_xml)
                references.update(ohlasy_list)
                token=handler.parse_token()


            zoskupene_referencie = self.group_references(self.create_references(references))

            for r in zoskupene_referencie:
                self.writer.write_record(pole035=r[0], references=zoskupene_referencie[r])


        except (CrepConnectionError, WrongXmlDataToParse, MissingDataException) as e:
            self.logger.log_error(e)
        finally:
            self.logger.close()
            self.writer.close()

    def create_references(self, ref):
        ret = set()
        fact=reference_factory()
        for r in ref:
            try:
                set.add(fact.get_reference(r))
            except (CrepConnectionError, WrongXmlDataToParse, MissingDataException) as e:
                self.logger.log_error(e)
        return ret

    def group_references(self, ref):
        ret = {}
        for r in ref:
            if r.pole035 not in ret:
                ret[r.pole035] = set()
            ret[r.pole035].add(r)
        return ret
