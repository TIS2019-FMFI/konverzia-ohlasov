class MissingDataException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg=msg

class CrepConnectionError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg=msg

class WrongXmlDataToParse(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg=msg
