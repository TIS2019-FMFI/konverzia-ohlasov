from app1.references_manager.references_manager import references_manager
from app1.progress_logger.progress_logger import progress_logger
class app1_initializer:
    """
    Zabezpecuje inicializaciu a spustenie app1.
    """        
    def __init__(self,params):
        """Ako parameter dostane argumenty zadane pri spusteni,
        tie spracuje a ulozi do vnutornej reprezentacie.
        Pri nezadani alebo nespravnom zadani argumentov vypise
        moznosti spustenia.
        Arguments:
            params {list[str]} --  argumenty pri spusteni
        """        
        self.file_path=None
        self.since=None
        self.to=None
        self.log_path=None
        raise NotImplementedError

    def run_app(self):
        """
        Vyrobi instanciu progress_logger a file_writer
        nasledne aj instanciu references_manager na ktorej zavola
        pozadovanu metodu.
        """        
        raise NotImplementedError
