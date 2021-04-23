from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, indent 

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

class Question(object):
    def __init__(self):
        self.id = ""
        self.version = ""
        self.uploadDate = None 
        self.lastModificationDate = None 
        self.attribution = Attribution()
        self.title = ""
        self.developers = []
        self.language = Language()
        self.dialects = []
        self.calendars = []
        self.currencies = []
        self.unitSystems = []
        self.parameters = []
        self.parts = []

    def addDeveloper(self, role = "", name = "", emailAddress = ""):
        self.developers.append(Developer(role, name, emailAddress))

    def addDialect(self, name = "", code = ""):
        self.dialects.append(Dialect(name, code))

    def addCalendar(self, name = "", code = ""):
        self.calendars.append(Calendar(name, code))

    def addCurrency(self, name = "", code = ""):
        self.currencies.append(Currency(name, code))

    def addUnitSystem(self, name = "", code = ""):
        self.unitSystems.append(UnitSystem(name, code))

    def addPart(self, _type = "", reference = ""):
        if reference == "":
            reference = "part{}".format(len(self.parts) + 1)

        part = QuestionPart()
        part.type = _type 
        part.reference = reference 

        self.parts.append(part)

        return part 

    def toXML(self):
        e1 = XMLElement("question")
        e1.set("id", self.id)
        e1.set("version", str(self.version))
        
        e10 = XMLSubelement(e1, "upload_date")
        e10.text = self.uploadDate.strftime(DATETIME_FORMAT) if self.uploadDate != None else ""

        e11 = XMLSubelement(e1, "last_modification_date")
        e11.text = self.lastModificationDate.strftime(DATETIME_FORMAT) if self.lastModificationDate != None else ""

        e1.append(self.attribution.toXML())

        e3 = XMLSubelement(e1, "developers")

        for developer in self.developers:
            e3.append(developer.toXML())

        e1.append(self.language.toXML())

        e4 = XMLSubelement(e1, "dialects")

        for dialect in self.dialects:
            e4.append(dialect.toXML())

        e5 = XMLSubelement(e1, "calendars")

        for calendar in self.calendars:
            e5.append(calendar.toXML())

        e6 = XMLSubelement(e1, "currencies")

        for currency in self.currencies:
            e6.append(currency.toXML())

        e7 = XMLSubelement(e1, "unit_systems")

        for unitSystem in self.unitSystems:
            e7.append(unitSystem.toXML())

        e2 = XMLSubelement(e1, "title")
        e2.text = self.title

        e8 = XMLSubelement(e1, "parameters")

        for parameterSet in self.parameters:
            e8.append(parameterSet.toXML())

        e9 = XMLSubelement(e1, "parts")

        for part in self.parts:
            e9.append(part.toXML())

        return e1 

    def save(self, filePath):
        tree = XMLElementTree(self.toXML())
        indent(tree, space="    ")
        tree.write(filePath, xml_declaration=True, encoding="utf-8", pretty_print=True)

class Attribution(object):
    def __init__(self):
        self.sourceId = ""
        self.pages = ""

    def toXML(self):
        e1 = XMLElement("attribution")
        e1.set("source_id", self.sourceId)

        if self.pages != "":
            e1.set("pages", self.pages)

        return e1 

class Developer(object):
    def __init__(self, role = "", name = "", emailAddress = ""):
        self.role = role 
        self.name = name 
        self.emailAddress = emailAddress

    def toXML(self):
        e1 = XMLElement("developer")
        e1.set("role", self.role)

        e2 = XMLSubelement(e1, "name")
        e2.text = self.name 

        e3 = XMLSubelement(e1, "email_address")
        e3.text = self.emailAddress 

        return e1

class Language(object):
    def __init__(self, name = "", code = ""):
        self.name = name 
        self.code = code 

    def toXML(self):
        e1 = XMLElement("language")

        if self.name != "":
            e1.set("name", self.name)

        if self.code != "":
            e1.set("code", self.code)

        return e1 

class Dialect(object):
    def __init__(self, name = "", code = ""):
        self.name = name 
        self.code = code 

    def toXML(self):
        e1 = XMLElement("dialect")

        if self.name != "":
            e1.set("name", self.name)

        if self.code != "":
            e1.set("code", self.code)

        return e1 

class Calendar(object):
    def __init__(self, name = "", code = ""):
        self.name = name 
        self.code = code 

    def toXML(self):
        e1 = XMLElement("calendar")

        if self.name != "":
            e1.set("name", self.name)

        if self.code != "":
            e1.set("code", self.code)

        return e1 

class Currency(object):
    def __init__(self, name = "", code = ""):
        self.name = name 
        self.code = code 

    def toXML(self):
        e1 = XMLElement("currency")

        if self.name != "":
            e1.set("name", self.name)

        if self.code != "":
            e1.set("code", self.code)

        return e1 

class UnitSystem(object):
    def __init__(self, name = "", code = ""):
        self.name = name 
        self.code = code 

    def toXML(self):
        e1 = XMLElement("unit_system")

        if self.name != "":
            e1.set("name", self.name)

        if self.code != "":
            e1.set("code", self.code)

        return e1 

class QuestionPart(object):
    def __init__(self):
        self.type = ""
        self.reference = ""
        self.responseFormats = []

    def addChoicesResponseFormat(self):
        responseFormat = ChoicesResponseFormat()

        self.responseFormats.append(responseFormat)

        return responseFormat 

    def toXML(self):
        e1 = XMLElement("part")

        e1.set("type", self.type)
        e1.set("reference", self.reference)

        e2 = XMLSubelement(e1, "layout")

        e3 = XMLSubelement(e1, "response_formats")

        for responseFormat in self.responseFormats:
            e3.append(responseFormat.toXML())

        return e1

class ChoicesResponseFormat(object):
    def __init__(self):
        self.choices = []

    def addChoice(self, reference = "", isCorrectAnswer = False, orderIndex = -1):
        choice = Choice(reference, isCorrectAnswer, orderIndex)

        self.choices.append(choice)

        return choice 

    def toXML(self):
        e1 = XMLElement("response_format")
        e1.set("type", "choices")

        e2 = XMLSubelement(e1, "choices")

        for choice in self.choices:
            e2.append(choice.toXML())

        return e1

class Choice(object):
    def __init__(self, reference = "", isCorrectAnswer = False, orderIndex = -1):
        self.reference = reference
        self.isCorrectAnswer = isCorrectAnswer 
        self.orderIndex = orderIndex

    def toXML(self):
        e1 = XMLElement("choice")
        e1.set("reference", self.reference)

        if self.isCorrectAnswer == True:
            e1.set("is_correct_answer", "true")

        if self.orderIndex >= 0:
            e1.set("order_index", self.orderIndex)

        return e1

class InputTextResponseFormat(object):
    def __init__(self):
        pass


    def toXML(self):
        e1 = XMLElement("response_format")
        e1.set("type", "input_text")

        return e1

class TextElement(object):
    def __init__(self):
        self.text = ""

    def toXML(self):
        pass

class ContentElement(object):
    def __init__(self, name = ""):
        self.name = name
        self.subelements = []

class Paragraph(object):
    def __init__(self):
        super.__init__("p")

    

