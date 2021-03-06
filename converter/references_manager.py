import datetime

from exceptions import *
from reference import reference
from reference_factory import reference_factory
from crepc_connector import crepc_connector
from exceptions import *
from xml_handler import xml_handler


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
        self.connector = crepc_connector()
        self.handler = xml_handler()
        self.counter_zapisanych = 0

    def get_references(self):
        """Do writeru zadanom pri inicializacii
        zapise vzniknute ohlasy pricom pouzije argumenty z initializer
        """

        start = self.initializer.from_date
        end = self.initializer.to_date


        try:
            all_xml = self.connector.get_references(since=start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                               to=end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            ohlasy_list = self.handler.parse_references(all_xml)
            references = set()
            references.update(ohlasy_list)
            token=self.handler.parse_token(all_xml)
            while  token is not None:
                all_xml = self.connector.get_references_with_token(token)
                ohlasy_list=self.handler.parse_references(all_xml)
                references.update(ohlasy_list)
                token=self.handler.parse_token(all_xml)


            zoskupene_referencie = self.group_references(self.create_references(references))

            for r in zoskupene_referencie:
                    self.writer.write_record(zoskupene_referencie[r],field035=r )
                    for j in zoskupene_referencie[r]:
                        self.logger.log_step(j)
            self.logger.log_status(f"Zapisalo sa {self.counter_zapisanych} ohlasov.")


        except (CrepConnectionError, WrongXmlDataToParse, MissingDataException) as e:
            self.logger.log_error(e)
        finally:
            self.logger.log_info(f"Konverzia ukoncena")
            self.logger.close()
            self.writer.close()

    def create_references(self, ref):
        ret = set()
        fact=reference_factory(self.logger)
        counter=0

        for r in ref:
            counter+=1
            self.logger.log_info(f'Overujem prislusnost a ziskavam data k referencii {counter} z {len(ref)}. [id591={r[0]}, id035={r[1]}]')
            try:
                akt=fact.get_reference(id035=r[1], id591=r[0], citation_cat=r[3],page=r[2])
                if akt is not None:
                    ret.add(akt)
                    self.counter_zapisanych+=1
            except (CrepConnectionError, WrongXmlDataToParse, MissingDataException) as e:
                self.logger.log_error(e)
        return ret

    def group_references(self, ref):
        ret = {}
        for r in ref:
            if r.field035 not in ret:
                ret[r.field035] = set()
            ret[r.field035].add(r)
        return ret
