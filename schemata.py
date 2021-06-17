import logging 

logger = logging.getLogger(__name__)

class Schema(object):
    def __init__(self):
        self.structures = []

class Structure(object):
    def __init__(self, reference = ""):
        self.reference = reference

class DataStructure(Structure):
    def __init__(self, reference = ""):
        super().__init__(reference)

        self.pattern = ""
        self.values = []

class ElementStructure(Structure):
    def __init__(self, reference = ""):
        super().__init__(reference)

        self.elementName = ""
        self.canBeRootElement = False 
        self.attributes = []

class AttributeStructure(Structure):
    def __init__(self, reference = ""):
        super().__init__(reference)

        self.attributeName = ""
        self.dataType = None 



class Marker(object):
    def __init__(self):

        self.position = 0

    def copy(self):
        marker = Marker()

        marker.position = self.position

        return marker



def cut(text, startIndex, length=1):
    a = startIndex
    b = startIndex + length
    return text[a:b]

class SchemataParsingError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Parser(object):
    def __init__(self):
        pass 

    def parseSchema(self, inputText):
        marker = Marker()

        schema = Schema()

        while marker.position < len(inputText):
            structure = self.parseStructure(inputText, marker)

            schema.structures.append(structure)

        return schema 

    def parseStructure(self, inputText, marker):

        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 8) == "dataType":
            marker.position += 8

            dataStructure = DataStructure()

            self.parseWhiteSpace(inputText, marker)
            reference = self.parseReference(inputText, marker)
            self.parseWhiteSpace(inputText, marker)

            dataStructure.reference = reference 

            if cut(inputText, marker.position, 1) == "{":
                marker.position += 1
            else:
                raise SchemataParsingError("Expected '{{' at {}.".format(marker.position))

            while marker.position < len(inputText):
                p = self.parseProperty(inputText, marker)

                if p == None:
                    break
                else:
                    if p[0] == "pattern":
                        dataStructure.pattern = p[1]
                    if p[0] == "values":
                        dataStructure.values = p[1] 

            self.parseWhiteSpace(inputText, marker)

            if cut(inputText, marker.position, 1) == "}":
                marker.position += 1
            else:
                raise SchemataParsingError("Expected '}}' at {}.".format(marker.position))

            return dataStructure 

    def parseProperty(self, inputText, marker):

        self.parseWhiteSpace(inputText, marker)
        propertyName = self.parsePropertyName(inputText, marker)

        if propertyName == None:
            return None 


        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position) == ":":
            marker.position += 1
        else:
            return None 

        self.parseWhiteSpace(inputText, marker)

        value = None 

        if propertyName == "pattern":
            value = self.parseString(inputText, marker)
        
        if propertyName == "values":
            value == self.parseList(inputText, marker)

        if value == None:
            return None 

        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position) == ";":
            marker.position += 1
        else:
            return None 

        return (propertyName, value)       

    def parsePropertyName(self, inputText, marker):
        t = ""

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-":
                t += c
                marker.position += 1
            else:
                break

        if len(t) == 0:
            return None

        return t 

    def parseString(self, inputText, marker):
        t = ""
        quoteMarkType = ""

        if cut(inputText, marker.position) == "'":
            quoteMarkType = "single"
            marker.position += 1
        elif cut(inputText, marker.position) == "\"":
            quoteMarkType = "double"
            marker.position += 1
        else:
            return None 

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if (quoteMarkType == "single" and c != "'") or (quoteMarkType == "double" and c != "\""):
                t += c
                marker.position += 1
            else:
                marker.position += 1
                break

        return t 

    def parseList(self, inputText, marker):
        items = []
        n = 0

        while marker.position < len(inputText):
            self.parseWhiteSpace(inputText, marker)

            if n > 0:
                if cut(inputText, marker.position) != ",":
                    break
            
            self.parseWhiteSpace(inputText, marker)

            item = self.parseString(inputText, marker)

            if item == None:
                break 

            items.append(item)

            n += 1

        if n == 0:
            return None 

        return items 

    def parseReference(self, inputText, marker):
        t = ""

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-":
                t += c
                marker.position += 1
            else:
                break

        if len(t) == 0:
            return None

        return t 

    def parseWhiteSpace(self, inputText, marker):
        t = ""

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if c in " \t\n":
                t += c
                marker.position += 1
            else:
                break

        if len(t) == 0:
            return None

        return t 
