import logging 
from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, QName, indent 

logger = logging.getLogger(__name__)

class Schema(object):
    def __init__(self):
        self.structures = []

    def getPossibleRootElements(self):
        return [s for s in self.structures if isinstance(s, ElementStructure) and s.canBeRootElement]

class Structure(object):
    def __init__(self, reference = ""):
        self.reference = reference

class DataStructure(Structure):
    def __init__(self, reference = ""):
        super().__init__(reference)

        self.baseStructure = None 
        self.allowedPattern = ""
        self.allowedValues = []

class ElementStructure(Structure):
    def __init__(self, reference = ""):
        super().__init__(reference)

        self.elementName = ""
        self.canBeRootElement = False 
        self.attributes = []
        self.allowedContent = ""
        self.subelements = []
        self.elementCloseType = ""

class AttributeUsageReference(object):
    def __init__(self):
        self.attributeReference = ""
        self.isOptional = False 

class ElementUsageReference(object):
    def __init__(self):
        self.elementReference = ""
        self.numberExpression = ""

class TextElement(object):
    def __init__(self):
        pass

class UnorderedSubelementList(object):
    def __init__(self):
        self.elements = []

class OrderedSubelementList(object):
    def __init__(self):
        self.elements = []

class AttributeStructure(Structure):
    def __init__(self, reference = ""):
        super().__init__(reference)

        self.attributeName = ""
        self.dataStructure = None 


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
    _propertyNameCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    _referenceCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    _keywordCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
    _operators = ["=", ">", ">=", "<", "<=", "/="]

    def __init__(self):
        pass 

    def parseSchema(self, inputText):
        logging.debug("Attempting to parse schema.")

        marker = Marker()

        schema = Schema()

        while marker.position < len(inputText):
            structure = self.parseStructure(inputText, marker)

            schema.structures.append(structure)

        return schema 

    def parseStructure(self, inputText, marker):
        logging.debug("Attempting to parse structure.")

        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 8) == "dataType":
            marker.position += 8

            logging.debug("Found data structure.")

            dataStructure = self.parseDataStructure(inputText, marker)

            return dataStructure 

        if cut(inputText, marker.position, 4) == "root":
            marker.position += 4 

            self.parseWhiteSpace(inputText, marker)

            if cut(inputText, marker.position, 7) == "element":
                marker.position += 7

                elementStructure = self.parseElementStructure(inputText, marker)
                elementStructure.canBeRootElement = True 

                return elementStructure 
            else:
                raise SchemataParsingError("Expected 'element' keyword at position {}.".format(marker.position))

        if cut(inputText, marker.position, 7) == "element":
            marker.position += 7

            elementStructure = self.parseElementStructure(inputText, marker)

            return elementStructure 

        if cut(inputText, marker.position, 9) == "attribute":
            marker.position += 9

            attributeStructure = self.parseAttributeStructure(inputText, marker)

            return attributeStructure 

    def parseDataStructure(self, inputText, marker):
        dataStructure = DataStructure()

        self.parseWhiteSpace(inputText, marker)
        reference = self.parseReference(inputText, marker)
        self.parseWhiteSpace(inputText, marker)

        dataStructure.reference = reference 

        if cut(inputText, marker.position, 1) == "{":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '{{' at position {}.".format(marker.position))

        while marker.position < len(inputText):
            p = self.parseProperty(inputText, marker)

            if p == None:
                break
            else:
                if p[0] == "pattern":
                    dataStructure.allowedPattern = p[1]
                if p[0] == "values":
                    dataStructure.allowedValues = p[1] 

        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 1) == "}":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '}}' at position {}.".format(marker.position))

        return dataStructure

    def parseElementStructure(self, inputText, marker):
        elementStructure = ElementStructure()

        self.parseWhiteSpace(inputText, marker)
        reference = self.parseReference(inputText, marker)
        self.parseWhiteSpace(inputText, marker)

        elementStructure.reference = reference 

        if cut(inputText, marker.position, 1) == "{":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '{{' at position {}.".format(marker.position))

        while marker.position < len(inputText):
            p = self.parseProperty(inputText, marker)

            if p == None:
                break
            else:
                if p[0] == "tagName":
                    elementStructure.elementName = p[1]
                if p[0] == "allowedContent":
                    elementStructure.allowedContent = p[1]
                if p[0] == "subelements":
                    elementStructure.subelements = p[1]

        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 1) == "}":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '}}' at position {}.".format(marker.position))

        return elementStructure 

    def parseAttributeStructure(self, inputText, marker):
        attributeStructure = AttributeStructure()

        self.parseWhiteSpace(inputText, marker)
        reference = self.parseReference(inputText, marker)
        self.parseWhiteSpace(inputText, marker)

        attributeStructure.reference = reference 

        if cut(inputText, marker.position, 1) == "{":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '{{' at position {}.".format(marker.position))

        while marker.position < len(inputText):
            p = self.parseProperty(inputText, marker)

            if p == None:
                break
            else:
                if p[0] == "tagName":
                    attributeStructure.attributeName = p[1]

        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 1) == "}":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '}}' at position {}.".format(marker.position))

        return attributeStructure 

    def parseProperty(self, inputText, marker):
        logging.debug("Attempting to parse structure property.")

        self.parseWhiteSpace(inputText, marker)
        propertyName = self.parsePropertyName(inputText, marker)

        if propertyName == None:
            return None 

        self.parseWhiteSpace(inputText, marker)

        logging.debug("Found property name '{}'.".format(propertyName))

        if cut(inputText, marker.position) == ":":
            marker.position += 1
        else:
            return None 

        self.parseWhiteSpace(inputText, marker)
        
        propertyValue = None 

        if propertyName == "baseType":
            propertyValue = self.parseReference(inputText, marker)

        if propertyName == "tagName":
            propertyValue = self.parseString(inputText, marker)

        if propertyName == "allowedContent":
            self.parseWhiteSpace(inputText, marker)

            keyword = self.parseKeyword(inputText, marker)
            allowedKeywords = ["elements only", "text only", "elements and text"]

            if keyword not in allowedKeywords:
                raise SchemataParsingError("Expected one of {} at position {}.".format(", ".join(allowedKeywords), marker.position))

            propertyValue = keyword 

        if propertyName == "attributes":
            propertyValue = self.parseList(inputText, marker, "attributeUsageReference")

        if propertyName == "subelements":
            propertyValue = self.parseList(inputText, marker, "elementUsageReference")

        if propertyName == "pattern":
            propertyValue = self.parseString(inputText, marker)
        
        if propertyName == "values":
            propertyValue = self.parseList(inputText, marker)
        
        if propertyName == "valueType":
            propertyValue = self.parseReference(inputText, marker)

        if propertyValue == None:
            return None 

        self.parseWhiteSpace(inputText, marker)

        logging.debug("Found property value '{}'.".format(propertyValue))

        if cut(inputText, marker.position) == ";":
            marker.position += 1
        else:
            return None 

        return (propertyName, propertyValue)       

    def parsePropertyName(self, inputText, marker):
        logging.debug("Attempting to parse property name.")

        t = ""

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if c in Parser._propertyNameCharacters:
                t += c
                marker.position += 1
            else:
                break

        if len(t) == 0:
            return None

        return t 

    def parseString(self, inputText, marker):
        logging.debug("Attempting to parse string.")

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

    def parseList(self, inputText, marker, objectType = "string"):
        logging.debug("Attempting to parse list.")

        items = []
        n = 0

        while marker.position < len(inputText):
            self.parseWhiteSpace(inputText, marker)

            if n > 0:
                if cut(inputText, marker.position) == ",":
                    marker.position += 1
                else:
                    break
            
            self.parseWhiteSpace(inputText, marker)

            item = None

            if objectType == "string":
                item = self.parseString(inputText, marker)
            if objectType == "attributeUsageReference":
                item = self.parseAttributeUsageReference(inputText, marker)
            if objectType == "elementUsageReference":
                item = self.parseElementUsageReference(inputText, marker)

            if item == None:
                break 

            items.append(item)

            n += 1

        if n == 0:
            return None 

        return items 

    def parseAttributeUsageReference(self, inputText, marker):
        logging.debug("Attempting to parse attribute usage reference.")

        self.parseWhiteSpace(inputText, marker)

        attributeReference = self.parseReference(inputText, marker)

        if attributeReference == None:
            return None 

        self.parseWhiteSpace(inputText, marker)

        attributeUsageReference = AttributeUsageReference()
        attributeUsageReference.attributeReference = attributeReference 

        if cut(inputText, marker.position) == "(":
            marker.position += 1

            self.parseWhiteSpace(inputText, marker)

            if cut(inputText, marker.position, 8) == "optional":
                marker.position += 8

                self.parseWhiteSpace(inputText, marker)

                if cut(inputText, marker.position) == ")":
                    marker.position += 1

                    attributeUsageReference.isOptional = True 
                else:
                    raise SchemataParsingError("Expected ')' at position {}.".format(marker.position))
            else:
                raise SchemataParsingError("Expected keyword at position {}.".format(marker.position))

        return attributeUsageReference 

    def parseElementUsageReference(self, inputText, marker):
        logging.debug("Attempting to parse element usage reference.")

        self.parseWhiteSpace(inputText, marker)

        elementReference = self.parseReference(inputText, marker)

        if elementReference == None:
            return None 

        self.parseWhiteSpace(inputText, marker)

        elementUsageReference = ElementUsageReference()
        elementUsageReference.elementReference = elementReference 

        if cut(inputText, marker.position) == "(":
            marker.position += 1

            self.parseWhiteSpace(inputText, marker)

            if cut(inputText, marker.position, 8) == "optional":
                marker.position += 8

                self.parseWhiteSpace(inputText, marker)

                if cut(inputText, marker.position) == ")":
                    marker.position += 1

                else:
                    raise SchemataParsingError("Expected ')' at position {}.".format(marker.position))
            else:
                raise SchemataParsingError("Expected keyword at position {}.".format(marker.position))

        return elementUsageReference 

    def parseReference(self, inputText, marker):
        logging.debug("Attempting to parse reference.")

        t = ""

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if c in Parser._referenceCharacters:
                t += c
                marker.position += 1
            else:
                break

        if len(t) == 0:
            return None

        logging.debug("Found reference '{}'.".format(t))

        return t 

    def parseKeyword(self, inputText, marker):
        logging.debug("Attempting to parse keyword.")

        t = ""

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if c in Parser._keywordCharacters:
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

class XSDExporter(object):
    def __init__(self):
        pass 

    def exportSchema(self, schema, filePath):

        xs = "http://www.w3.org/2001/XMLSchema"

        e1 = XMLElement(QName(xs, "schema"))
        e1.set("targetNamespace", "https://github.com/BM345/NagwaSchemas")
        e1.set("xmlns", "https://github.com/BM345/NagwaSchemas")
        e1.set("elementFormDefault", "qualified")

        roots = schema.getPossibleRootElements()

        for root in roots:
            e2 = XMLElement(QName(xs, "element"))
            e2.set("name", root.elementName)

            if root.allowedContent == "elements and text" or root.allowedContent == "elements only":
                e3 = XMLElement(QName(xs, "complexType"))

                if root.allowedContent == "elements and text":
                    e3.set("mixed", True)

                e4 = XMLElement(QName(xs, "sequence"))

                for subelement in root.subelements:
                    e5 = XMLElement(QName(xs, "element"))
                    e5.set("name", subelement.elementReference)
                    e5.set("maxOccurs", "unbounded")

                    e4.append(e5)

                e3.append(e4)
                e2.append(e3)

            e1.append(e2)

        tree = XMLElementTree(e1)
        indent(tree, space="    ")
        tree.write(filePath, xml_declaration=True, encoding="utf-8", pretty_print=True)

xsdExporter = XSDExporter()

def exportSchemaAsXSD(schema, filePath):
    xsdExporter.exportSchema(schema, filePath)

