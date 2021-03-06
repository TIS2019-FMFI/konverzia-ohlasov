from references_manager import references_manager
from progress_logger import progress_logger
from file_writer import file_writer
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
        self.output_file = "output.rec"
        self.output_path = ""
        self.log_file = "log.txt"
        self.log_path = ""
        self.from_date = None
        self.to_date = datetime.today()
        self.debug=False
        
        to = None
        fr = None

        try:
            opts, args = getopt.getopt(params,"hf:t:d",["debug","help","from=","to=","log-file=","out-file=","log-path=","out-path="])
        except getopt.GetoptError as err:
           print(err.msg)
           print("Pre viac informacii napiste 'python app1_initializer --help'")
           sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.usage()
                sys.exit(0)
            elif opt in ("-d","--debug"):
                self.debug=True
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
        print("Usage: ./startup.sh -f DDMMYYYY [-h | --help] [-t <date> | --to=<date> ]")
        print("                           [--out-file=<file>] [--out-path=<path>]")
        print("                           [--log-file=<file>] [--log-path=<path>]")
        print()
        print("Povinny argument:") 
        print("  -f <date>, --from=<date> Datum od ktoreho ziskava ohlasy, date musi byt vo formate DDMMYYYY")
        print("Volitelne argumenty:")
        print("  -t <date>, --to=<date>   Datum po ktory ziskava ohlasy, date musi byt vo formate DDMMYYYY,")
        print("                           default je dnesny datum")
        print("  --out-file=<file>        Nazov suboru do ktoreho sa uklada vystup,")
        print("                           default nazov je 'output'. V pripade ze subor neexistuje, vytvori sa novy")
        print("  --out-path=<path>        Cesta k vystupnemu suboru, default je priecinok odkial sa aplikacia spusta ")
        print("  --log-file=<file>        Nazov suboru do ktoreho sa vypisuje priebeh aplikacie,")
        print("                           default nazov je 'log'. V pripade ze subor neexistuje, vytvori sa novy")
        print("  --log-path=<path>        Cesta k log suboru, default je priecinok odkial sa aplikacia spusta")
        print("  -d, --debug              Spustenie debug modu aby sa vypisovalo aj info a warningy")


    def run_app(self):
        """
        Vyrobi instanciu progress_logger a file_writer
        nasledne aj instanciu references_manager na ktorej zavola
        pozadovanu metodu.
        """
        logger=progress_logger(output_file_name=self.log_file,output_file_path=self.log_path,debug=self.debug)
        writer= file_writer(name=self.output_file,path=self.output_path)
        manager=references_manager(self,logger,writer)
        manager.get_references()


if __name__ == "__main__":
    x =  app1_initializer(sys.argv[1:])
    x=input("pre pokracovanie stlacte enter")
