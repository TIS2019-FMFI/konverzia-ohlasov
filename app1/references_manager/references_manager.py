import datetime

from app1.reference.exceptions import *
from app1.reference.reference import reference
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
        since = "2019-12-01T07:00:00.000Z"  # zatial dummy value neskor self.initializer.since
        to = "2019-12-20T07:00:00.000Z"  # zatial dummy value neskor self.initializer.to
        start = datetime.datetime.strptime(since, '%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.datetime.strptime(to, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta = end - start

        try:
            references = set()
            while start < end:
                aktend = start + delta
                if aktend > end:
                    aktend = end
                all_xml = connector.get_references(since=start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                                   to=aktend.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
                ohlasy_list = handler.parse_references(all_xml)
                if len(ohlasy_list) == 100:
                    delta = delta * 0.5
                else:
                    references.update(self.create_references(ohlasy_list))
                    start = aktend

            zoskupene_referencie = self.group_references(references)

            for r in zoskupene_referencie:
                self.writer.write_record(pole035=r[0], pole008=r[1], references=zoskupene_referencie[r])


        except (CrepConnectionError, WrongXmlDataToParse, MissingDataException) as e:
            self.logger.log_error(e)
        finally:
            self.logger.close()
            self.writer.close()

    def create_references(self, ref):
        ret = set()
        for r in ref:
            try:
                set.add(reference(r))
            except (CrepConnectionError, WrongXmlDataToParse, MissingDataException) as e:
                self.logger.log_error(e)
        return ret

    def group_references(self, ref):
        ret = {}
        for r in ref:
            if (r.pole035, r.pole008) not in ret:
                ret[(r.pole035, r.pole008)] = set()
            ret[(r.pole035, r.pole008)].add(r)
        return ret
