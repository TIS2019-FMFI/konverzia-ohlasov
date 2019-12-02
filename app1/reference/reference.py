from abc import ABC, abstractmethod
from app1.reference.exceptions import MissingDataException
class reference(ABC):
    """abstractna trieda uchovavajuca jeden ohlas
    """    
    @abstractmethod
    def __init__(self, data):
        """Nastavi si hodnoty z data. Chybajuce hodnoty sa pokusi ziskat.        
        Arguments:
            data {dict{str:str}} -- slovnik hodnot pre vytvorenie ohlasu.(spresnuje odvodena trieda)
        Raises:
            MissingDataException - ak ohlas nema vsetky potrbene data a nedaju sa dohladatrekurzivne
        """        
        pass

    @abstractmethod
    def is_valid(self):
        """Returns:
            Bool -- vrati True ak je ohlas kompletny a je mozne ho zapisat. 
        """        
        pass

    @abstractmethod
    def to_iso2709_string(self):
        """
        Returns:
            [str] -- retazec reprezentujuci ohlas v tvare iso2709
        """        
    
    @abstractmethod
    def __str__(self):
        """
         Returns:
            [str] -- retazec reprezentujuci ohlas v zrozumitelnom tvrare
        """        
        pass