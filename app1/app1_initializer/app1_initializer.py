from app1.references_manager.references_manager import references_manager
from app1.progress_logger.progress_logger import progress_logger
from app1.file_writer.file_writer import file_writer
import sys
import getopt
from datetime import datetime

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
        self.output_file = "output"
        self.output_path = ""
        self.log_file = "log"
        self.log_path = ""
        self.from_date = None
        self.to_date = datetime.today()
        
        to = None
        fr = None

        try:
            opts, args = getopt.getopt(params,"hf:t:",["help","from=","to=","log-file=","out-file=","log-path=","out-path="])
        except getopt.GetoptError as err:
           print(err.msg)
           print("Pre viac informacii napiste 'python app1_initializer --help'")
           sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.usage()
                sys.exit(0)
            elif opt in ("-f", "--from"):
                fr = arg
            elif opt in ("-t", "--to"):
                to = arg
            elif opt == "--out-file":
                self.output_file = arg
            elif opt == "--out-path":
                self.output_path = arg
            elif opt == "--log-file":
                self.log_file = arg
            elif opt == "--log-path":
                self.log_path = arg

        if fr is None:
            print("Parameter from musi byt nastaveny")
            print("Pre viac informacii napiste 'python app1_initializer --help'")
            sys.exit(2)

        to = self.changeTimeToFinalFormat(to) 
        fr = self.changeTimeToFinalFormat(fr)
        if to is not None:
            self.to_date = to
        if fr is not None:
            self.from_date = fr

        self.run_app()

        '''#TODO zmazat
        #kontrolny vypis
        print('od :', self.from_date, self.from_date.tzinfo)
        print('do :', self.to_date)
        print('Output file is :', self.output_file)
        print('Output file path is :',  self.output_path)
        print('log file is :', self.log_file)
        print('log file path is :',  self.log_path)'''

    def changeTimeToFinalFormat(self, time):
        if time is None:
            return None
        if len(time) < 8:
            print("Zle zadany datum", time)
            sys.exit(2)
        d = time[:2]
        m = time[2:4]
        y = time[4:]
        return datetime(int(y),int(m),int(d)) 


    def usage(self):
        print("Usage: python app1_initializer -f DDMMYYYY [-h | --help] [-t <date> | --to=<date> ]")
        print("                               [--out-file=<file>] [--out-path=<path>]")
        print("                               [--log-file=<file>] [--log-path=<path>]")
        print()
        print("Povinny argument:") 
        print("  -f <date>, --from=<date> Datum od ktoreho ziskava ohlasy, date musi byt vo formate DDMMYYYY")
        print("Volitelne argumenty:")
        print("  -t <date>, --to=<date>   Datum po ktory ziskava ohlasy, date musi byt vo formate DDMMYYYY,")
        print("                           default je dnesny datum")
        print("  --out-file=<file>        Nazov suboru do ktoreho sa uklada vystup,")
        print("                           default nazov je 'output'. V pripade ze subor neexistuje, vytvori sa novy")
        print("  --out-path=<path>        Cesta k vystupnemu suboru, defaultna cesta je ./output/")
        print("  --log-file=<file>        Nazov suboru do ktoreho sa vypisuje priebeh aplikacie,")
        print("                           default nazov je 'log'. V pripade ze subor neexistuje, vytvori sa novy")
        print("  --log-path=<path>        Cesta k log suboru default je ./output/")


    def run_app(self):
        """
        Vyrobi instanciu progress_logger a file_writer
        nasledne aj instanciu references_manager na ktorej zavola
        pozadovanu metodu.
        """
        logger=progress_logger(output_file_name=self.log_file,output_file_path=self.log_path)
        writer= file_writer(name=self.output_file,path=self.output_path)
        manager=references_manager(self,logger,writer)
        manager.get_references()


if __name__ == "__main__":
    x =  app1_initializer(sys.argv[1:])
