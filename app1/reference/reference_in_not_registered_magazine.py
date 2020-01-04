from app1.references_manager.crepc_connector import crepc_connector
from app1.references_manager.xml_handler import xml_handler
from app1.reference.exceptions import MissingDataException
from app1.reference.reference import reference


class reference_in_not_registered_magazine(reference):
    """Odvodena trieda od reference uchovavajuca ohlas
        z neregistrovaneho casopisu.
    """

    def __init__(self, data):
        if "name" not in data:
            raise MissingDataException("Reference without name")
        else:
            self.name = data["name"]

        if "category" in data and "year" in data and "author" in data and "source" in data and "page" in data and "field008" in data and "field035" in data:
            self.category = data["category"]
            self.year = data["year"]
            self.author = data["author"]
            self.source = data["source"]
            self.page = data["page"]
            self.field008 = data["field008"]
            self.field035 = data["field035"]

        else:
            raise MissingDataException(self.name)

    def is_valid(self):
        for i in self.category, self.year, self.author, self.name, self.source, self.page, self.field008, self.field035:
            if i is None:
                return False
        return True

    def to_iso2709_string(self):
        return f"\9 [o{self.category}] \d {self.year} \m {self.author} \\n {self.name} \p {self.source} \s s. {self.page}"

    def __str__(self):
        return f"{self.name}. {self.author}. {self.year}"


