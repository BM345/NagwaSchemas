import logging 
from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, QName, indent 

logger = logging.getLogger(__name__)

class Schema(object):
    def __init__(self):
        self.structures = []

    def getDataStructures(self):
        return [s for s in self.structures if isinstance(s, DataStructure)]

    def getDataStructureByReference(self, reference):
        return [s for s in self.getDataStructures() if s.reference == reference][0]

    def getPossibleRootElements(self):
        return [s for s in self.structures if isinstance(s, ElementStructure) and s.canBeRootElement]

    def getNonRootElements(self):
        return [s for s in self.structures if isinstance(s, ElementStructure) and not s.canBeRootElement]

    def getElementStructures(self):
        return [s for s in self.structures if isinstance(s, ElementStructure)]

    def getElementStructureByReference(self, reference):
        return [s for s in self.getElementStructures() if s.reference == reference][0]

    def getAttributeStructures(self):
        return [s for s in self.structures if isinstance(s, AttributeStructure)]

    def getAttributeStructureByReference(self, reference):
        return [s for s in self.getAttributeStructures() if s.reference == reference][0]

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
        self.minimumNumberOfOccurrences = 1
        self.maximumNumberOfOccurrences = 1

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
    _negatedOperators = ["=", "<", "<=", ">", ">=", "/="]

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
                if p[0] == "attributes":
                    elementStructure.attributes = p[1]
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
                if p[0] == "valueType":
                    attributeStructure.dataStructure = p[1]

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

            numericExpression = self.parseNumericExpression(inputText, marker)

            if numericExpression != None:
                elementUsageReference.numberExpression = numericExpression 

                if cut(inputText, marker.position) == ")":
                    marker.position += 1

                else:
                    raise SchemataParsingError("Expected ')' at position {}.".format(marker.position))
            elif cut(inputText, marker.position, 8) == "optional":
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

    def parseNumericExpression(self, inputText, marker):

        self.parseWhiteSpace(inputText, marker)
        n1 = self.parseInteger(inputText, marker)
        o1 = None 
        self.parseWhiteSpace(inputText, marker)

        if n1 != None:
            o1 = self.parseOperator(inputText, marker)

            if o1 == None:
                raise SchemataParsingError("Expected an operator at position {}.".format(marker.position))

        self.parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position) == "n":
            marker.position += 1
        else:
            if n1 == None and o1 == None:
                return None 
            else:
                raise SchemataParsingError("Expected 'n' at position {}.".format(marker.position))

        self.parseWhiteSpace(inputText, marker)

        o2 = self.parseOperator(inputText, marker)

        if o2 == None:
            raise SchemataParsingError("Expected an operator at position {}.".format(marker.position))

        self.parseWhiteSpace(inputText, marker)
        n2 = self.parseInteger(inputText, marker)

        e = []

        if o1 != None and n1 != None:
            i = self._operators.find(o1)
            o1b = self._negatedOperators[i]
            e += [(o1b, n1)]

        e += [(o2, n2)]

        return e       

    def parseOperator(self, inputText, marker):
        operators = sorted(self._operators, key= lambda o: len(o), reverse=True)

        for operator in operators:
            if cut(inputText, marker.position, len(operator)) == operator:
                marker.position += len(operator)

                return operator

        return None 

    def parseInteger(self, inputText, marker):
        t = ""

        while marker.position < len(inputText):
            c = cut(inputText, marker.position)

            if c in "0123456789":
                t += c 
                marker.position += 1
            else:
                break 

        if len(t) == 0:
            return None 

        return int(t)

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
        self._xs = "http://www.w3.org/2001/XMLSchema"
        pass 

    def exportSchema(self, schema, filePath):
        xs = self._xs

        e1 = XMLElement(QName(xs, "schema"))
        e1.set("targetNamespace", "https://github.com/BM345/NagwaSchemas")
        e1.set("xmlns", "https://github.com/BM345/NagwaSchemas")
        e1.set("elementFormDefault", "qualified")

        self.exportDataStructures(schema, e1)
        self.exportElementStructures(schema, e1)

        roots = schema.getPossibleRootElements()

        for root in roots:
            e2 = XMLElement(QName(xs, "element"))
            e2.set("name", root.elementName)
            e2.set("type", "__type__" + root.reference)

            e1.append(e2)

        tree = XMLElementTree(e1)
        indent(tree, space="    ")
        tree.write(filePath, xml_declaration=True, encoding="utf-8", pretty_print=True)

    def exportDataStructures(self, schema, xsdElement):
        xs = self._xs 

        dataStructures = schema.getDataStructures()

        for dataStructure in dataStructures:
            e1 = XMLElement(QName(xs, "simpleType"))
            e1.set("name", "__type__" + dataStructure.reference)

            if dataStructure.allowedPattern != "":
                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:string")

                e3 = XMLElement(QName(xs, "pattern"))
                e3.set("value", dataStructure.allowedPattern)

                e2.append(e3)
                e1.append(e2)

            xsdElement.append(e1)
    
    def exportElementStructures(self, schema, xsdElement):
        xs = self._xs 

        elementStructures = schema.getElementStructures()

        for elementStructure in elementStructures:
            if elementStructure.allowedContent == "elements and text" or elementStructure.allowedContent == "elements only":
                e1 = XMLElement(QName(xs, "complexType"))
                e1.set("name", "__type__" + elementStructure.reference)

                if elementStructure.allowedContent == "elements and text":
                    e1.set("mixed", "true")
                else:
                    e1.set("mixed", "false")

                e2 = XMLElement(QName(xs, "sequence"))

                for subelement in elementStructure.subelements:
                    e3 = XMLElement(QName(xs, "element"))
                    e3.set("name", subelement.elementReference)
                    e3.set("type", "__type__" + subelement.elementReference)
                    p =  subelement.minimumNumberOfOccurrences
                    q = subelement.maximumNumberOfOccurrences 

                    if p != 1:
                        e3.set("minOccurs", str( p))

                    if q != 1:
                        e3.set("maxOccurs", "unbounded" if q == -1 else str( q) )

                    e2.append(e3)

                e1.append(e2)

                for attribute in elementStructure.attributes:
                    a = schema.getAttributeStructureByReference(attribute.attributeReference)

                    e4 = XMLElement(QName(xs, "attribute"))
                    e4.set("name", a.attributeName)
                    e4.set("type", "__type__" + a.dataStructure)
                    e4.set("use", "optional" if attribute.isOptional else "required")

                    e1.append(e4)

                xsdElement.append(e1)

            elif elementStructure.attributes == [] and elementStructure.allowedContent == "text only":
                e1 = XMLElement(QName(xs, "simpleType"))
                e1.set("name", "__type__" + elementStructure.reference)

                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:string")

                e1.append(e2)
                xsdElement.append(e1)


xsdExporter = XSDExporter()

def exportSchemaAsXSD(schema, filePath):
    xsdExporter.exportSchema(schema, filePath)

