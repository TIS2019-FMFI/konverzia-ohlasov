from app2.data_fetcher import data_fetcher

class app2_initializer:
    """Zabezpecuje inicializaciu a spustenie app2."""
    def __init__(self, params):
        """Ako parameter dostane argumenty zadane pri spusteni,
        tie spracuje a ulozi do vnutornej reprezentacie.
        Pri nezadani alebo nespravnom zadani argumentov vypise
        moznosti spustenia.
        Arguments:
            params {list[str]} --  argumenty pri spusteni
        """ 
        raise NotImplementedError

    def run_app(self):
        """
        Vyrobi instanciu data_fetcher 
        nasledne spusti vkladanie.
        """ 
        raise NotImplementedError