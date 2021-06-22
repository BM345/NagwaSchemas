import logging 
import re
from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, QName, indent 

logger = logging.getLogger(__name__)

class Schema(object):
    def __init__(self):
        self.structures = []

    def getDataStructures(self):
        return [s for s in self.structures if isinstance(s, DataStructure)]

    def getDataStructureByReference(self, reference):
        return [s for s in self.getDataStructures() if s.reference == reference][0]

    def getPossibleRootElementStructures(self):
        return [s for s in self.structures if isinstance(s, ElementStructure) and s.canBeRootElement]

    def getNonRootElementStructures(self):
        return [s for s in self.structures if isinstance(s, ElementStructure) and not s.canBeRootElement]

    def getElementStructures(self):
        return [s for s in self.structures if isinstance(s, ElementStructure)]

    def getElementStructureByReference(self, reference):
        return [s for s in self.getElementStructures() if s.reference == reference][0]

    def getAttributeStructures(self):
        return [s for s in self.structures if isinstance(s, AttributeStructure)]

    def getAttributeStructureByReference(self, reference):
        ss = [s for s in self.getAttributeStructures() if s.reference == reference]

        if len(ss) == 0:
            raise Exception("Could not find attribute structure with the reference '{}'.".format(reference))

        return ss[0]

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
        self.allowedContent = "text only"
        self.subelements = []
        self.elementCloseType = ""

class AttributeUsageReference(object):
    def __init__(self):
        self.attributeReference = ""
        self.isOptional = False 

class ElementUsageReference(object):
    def __init__(self):
        self.elementReference = ""
        self.nExpression = ""
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

    def parseSchemaFromFile(self, filePath):
        with open(filePath, "r") as fileObject:
            text = fileObject.read()

            schema = self.parseSchema(text)

            return schema 

    def parseSchema(self, inputText):
        logging.debug("Attempting to parse schema.")

        marker = Marker()

        schema = Schema()

        while marker.position < len(inputText):
            structure = self._parseStructure(inputText, marker)

            schema.structures.append(structure)

        return schema 

    def _parseStructure(self, inputText, marker):
        logging.debug("Attempting to parse structure.")

        self._parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 8) == "dataType":
            marker.position += 8

            logging.debug("Found data structure.")

            dataStructure = self._parseDataStructure(inputText, marker)

            return dataStructure 

        if cut(inputText, marker.position, 4) == "root":
            marker.position += 4 

            self._parseWhiteSpace(inputText, marker)

            if cut(inputText, marker.position, 7) == "element":
                marker.position += 7

                logging.debug("Found root element structure.")

                elementStructure = self._parseElementStructure(inputText, marker)
                elementStructure.canBeRootElement = True 

                return elementStructure 
            else:
                raise SchemataParsingError("Expected 'element' keyword at position {}.".format(marker.position))

        if cut(inputText, marker.position, 7) == "element":
            marker.position += 7

            logging.debug("Found element structure.")

            elementStructure = self._parseElementStructure(inputText, marker)

            return elementStructure 

        if cut(inputText, marker.position, 9) == "attribute":
            marker.position += 9

            logging.debug("Found attribute structure.")

            attributeStructure = self._parseAttributeStructure(inputText, marker)

            return attributeStructure 

    def _parseDataStructure(self, inputText, marker):
        dataStructure = DataStructure()

        self._parseWhiteSpace(inputText, marker)        
        reference = self._parseReference(inputText, marker)
        self._parseWhiteSpace(inputText, marker)

        dataStructure.reference = reference 

        if cut(inputText, marker.position, 1) == "{":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '{{' at position {}.".format(marker.position))

        while marker.position < len(inputText):
            p = self._parseProperty(inputText, marker)

            if p == None:
                break
            else:
                if p[0] == "baseType":
                    dataStructure.baseStructure = p[1]
                if p[0] == "pattern":
                    dataStructure.allowedPattern = p[1]
                if p[0] == "allowedValues":
                    dataStructure.allowedValues = p[1] 

        self._parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 1) == "}":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '}}' at position {}.".format(marker.position))

        return dataStructure

    def _parseElementStructure(self, inputText, marker):
        elementStructure = ElementStructure()

        self._parseWhiteSpace(inputText, marker)
        reference = self._parseReference(inputText, marker)
        self._parseWhiteSpace(inputText, marker)

        elementStructure.reference = reference 

        if cut(inputText, marker.position, 1) == "{":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '{{' at position {}.".format(marker.position))

        while marker.position < len(inputText):
            p = self._parseProperty(inputText, marker)

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

        self._parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 1) == "}":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '}}' at position {}.".format(marker.position))

        if elementStructure.elementName == "":
            elementStructure.elementName = elementStructure.reference 

        return elementStructure 

    def _parseAttributeStructure(self, inputText, marker):
        attributeStructure = AttributeStructure()

        self._parseWhiteSpace(inputText, marker)
        reference = self._parseReference(inputText, marker)
        self._parseWhiteSpace(inputText, marker)

        attributeStructure.reference = reference 

        if cut(inputText, marker.position, 1) == "{":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '{{' at position {}.".format(marker.position))

        while marker.position < len(inputText):
            p = self._parseProperty(inputText, marker)

            if p == None:
                break
            else:
                if p[0] == "tagName":
                    attributeStructure.attributeName = p[1]
                if p[0] == "valueType":
                    attributeStructure.dataStructure = p[1]

        self._parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position, 1) == "}":
            marker.position += 1
        else:
            raise SchemataParsingError("Expected '}}' at position {}.".format(marker.position))

        if attributeStructure.attributeName == "":
            attributeStructure.attributeName = attributeStructure.reference 

        return attributeStructure 

    def _parseProperty(self, inputText, marker):
        logging.debug("Attempting to parse structure property.")

        self._parseWhiteSpace(inputText, marker)
        propertyName = self._parsePropertyName(inputText, marker)

        if propertyName == None:
            return None 

        self._parseWhiteSpace(inputText, marker)

        logging.debug("Found property name '{}'.".format(propertyName))

        if cut(inputText, marker.position) == ":":
            marker.position += 1
        else:
            return None 

        self._parseWhiteSpace(inputText, marker)
        
        propertyValue = None 

        if propertyName == "baseType":
            propertyValue = self._parseReference(inputText, marker)

        if propertyName == "tagName":
            propertyValue = self._parseString(inputText, marker)

        if propertyName == "allowedContent":
            self._parseWhiteSpace(inputText, marker)

            keyword = self._parseKeyword(inputText, marker)
            allowedKeywords = ["elements only", "text only", "elements and text", "none"]

            if keyword not in allowedKeywords:
                raise SchemataParsingError("Expected one of {} at position {}.".format(", ".join(allowedKeywords), marker.position))

            propertyValue = keyword 

        if propertyName == "attributes":
            propertyValue = self._parseList(inputText, marker, "attributeUsageReference")

        if propertyName == "subelements":
            propertyValue = self._parseList(inputText, marker, "elementUsageReference")

        if propertyName == "pattern":
            propertyValue = self._parseString(inputText, marker)
        
        if propertyName == "allowedValues":
            propertyValue = self._parseList(inputText, marker)
        
        if propertyName == "valueType":
            propertyValue = self._parseReference(inputText, marker)

        if propertyValue == None:
            return None 

        self._parseWhiteSpace(inputText, marker)

        logging.debug("Found property value '{}'.".format(propertyValue))

        if cut(inputText, marker.position) == ";":
            marker.position += 1
        else:
            return None 

        return (propertyName, propertyValue)       

    def _parsePropertyName(self, inputText, marker):
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

    def _parseString(self, inputText, marker):
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

    def _parseList(self, inputText, marker, objectType = "string"):
        logging.debug("Attempting to parse list.")

        items = []
        n = 0

        while marker.position < len(inputText):
            self._parseWhiteSpace(inputText, marker)

            if n > 0:
                if cut(inputText, marker.position) == ",":
                    marker.position += 1
                else:
                    break
            
            self._parseWhiteSpace(inputText, marker)

            item = None

            if objectType == "string":
                item = self._parseString(inputText, marker)
            if objectType == "attributeUsageReference":
                item = self._parseAttributeUsageReference(inputText, marker)
            if objectType == "elementUsageReference":
                item = self._parseElementUsageReference(inputText, marker)

            if item == None:
                break 

            items.append(item)

            n += 1

        if n == 0:
            return None 

        return items 

    def _parseAttributeUsageReference(self, inputText, marker):
        logging.debug("Attempting to parse attribute usage reference.")

        self._parseWhiteSpace(inputText, marker)
        attributeReference = self._parseReference(inputText, marker)

        if attributeReference == None:
            return None 

        self._parseWhiteSpace(inputText, marker)

        attributeUsageReference = AttributeUsageReference()
        attributeUsageReference.attributeReference = attributeReference 

        if cut(inputText, marker.position) == "(":
            marker.position += 1

            self._parseWhiteSpace(inputText, marker)

            if cut(inputText, marker.position, 8) == "optional":
                marker.position += 8

                attributeUsageReference.isOptional = True 

                self._parseWhiteSpace(inputText, marker)

                if cut(inputText, marker.position) == ")":
                    marker.position += 1
                else:
                    raise SchemataParsingError("Expected ')' at position {}.".format(marker.position))
            else:
                raise SchemataParsingError("Expected keyword at position {}.".format(marker.position))

        return attributeUsageReference 

    def _parseElementUsageReference(self, inputText, marker):
        logging.debug("Attempting to parse element usage reference.")

        self._parseWhiteSpace(inputText, marker)
        elementReference = self._parseReference(inputText, marker)

        if elementReference == None:
            return None 

        self._parseWhiteSpace(inputText, marker)

        elementUsageReference = ElementUsageReference()
        elementUsageReference.elementReference = elementReference 

        if cut(inputText, marker.position) == "(":
            marker.position += 1

            self._parseWhiteSpace(inputText, marker)

            elementUsageReference.minimumNumberOfOccurrences = 0
            elementUsageReference.maximumNumberOfOccurrences = -1

            nExpression = self._parseNExpression(inputText, marker)

            if nExpression != None:
                elementUsageReference.nExpression = nExpression 

                if cut(inputText, marker.position) == ")":
                    marker.position += 1
                else:
                    raise SchemataParsingError("Expected ')' at position {}.".format(marker.position))
            elif cut(inputText, marker.position, 8) == "optional":
                marker.position += 8

                elementUsageReference.nExpression = [(">=", 0), ("<=", 1)]

                self._parseWhiteSpace(inputText, marker)

                if cut(inputText, marker.position) == ")":
                    marker.position += 1
                else:
                    raise SchemataParsingError("Expected ')' at position {}.".format(marker.position))
            else:
                raise SchemataParsingError("Expected expression or keyword at position {}.".format(marker.position))

        for comparison in elementUsageReference.nExpression:
            if comparison[0] == ">=":
                elementUsageReference.minimumNumberOfOccurrences = comparison[1]
            if comparison[0] == ">":
                elementUsageReference.minimumNumberOfOccurrences = comparison[1] + 1
            if comparison[0] == "<=":
                elementUsageReference.maximumNumberOfOccurrences = comparison[1]
            if comparison[0] == "<":
                elementUsageReference.maximumNumberOfOccurrences = comparison[1] - 1
            if comparison[0] == "=":
                elementUsageReference.minimumNumberOfOccurrences = comparison[1]
                elementUsageReference.maximumNumberOfOccurrences = comparison[1]

        return elementUsageReference 

    def _parseReference(self, inputText, marker):
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

    def _parseKeyword(self, inputText, marker):
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

    def _parseNExpression(self, inputText, marker):

        self._parseWhiteSpace(inputText, marker)
        n1 = self._parseInteger(inputText, marker)
        o1 = None 
        self._parseWhiteSpace(inputText, marker)

        if n1 != None:
            o1 = self._parseOperator(inputText, marker)

            if o1 == None:
                raise SchemataParsingError("Expected an operator at position {}.".format(marker.position))

        self._parseWhiteSpace(inputText, marker)

        if cut(inputText, marker.position) == "n":
            marker.position += 1
        else:
            if n1 == None and o1 == None:
                return None 
            else:
                raise SchemataParsingError("Expected 'n' at position {}.".format(marker.position))

        self._parseWhiteSpace(inputText, marker)
        o2 = self._parseOperator(inputText, marker)

        if o2 == None:
            raise SchemataParsingError("Expected an operator at position {}.".format(marker.position))

        self._parseWhiteSpace(inputText, marker)
        n2 = self._parseInteger(inputText, marker)

        e = []

        if n1 != None and o1 != None:
            i = self._operators.find(o1)
            o1b = self._negatedOperators[i]
            e += [(o1b, n1)]

        e += [(o2, n2)]

        return e       

    def _parseOperator(self, inputText, marker):
        operators = sorted(self._operators, key= lambda o: len(o), reverse=True)

        for operator in operators:
            if cut(inputText, marker.position, len(operator)) == operator:
                marker.position += len(operator)

                return operator

        return None 

    def _parseInteger(self, inputText, marker):
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

    def _parseWhiteSpace(self, inputText, marker):
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
        self._typePrefix = "__type__"

    def _getXSDTypeName(self, structure):
        if isinstance(structure, DataStructure):
            return self._typePrefix + "d__" + structure.reference 
        if isinstance(structure, ElementStructure):
            return self._typePrefix + "e__" + structure.reference 
        if isinstance(structure, AttributeStructure):
            return self._typePrefix + "a__" + structure.reference 

        raise Exception("Cannot create XSD type name for {}.".format(structure.reference))

    def exportSchema(self, schema, filePath):
        xs = self._xs

        e1 = XMLElement(QName(xs, "schema"))
        e1.set("elementFormDefault", "qualified")

        self._exportDataStructures(schema, e1)
        self._exportElementStructures(schema, e1)

        roots = schema.getPossibleRootElementStructures()

        for root in roots:
            e2 = XMLElement(QName(xs, "element"))
            e2.set("name", root.elementName)
            e2.set("type", self._getXSDTypeName(root))

            e1.append(e2)

        tree = XMLElementTree(e1)
        indent(tree, space="    ")
        tree.write(filePath, xml_declaration=True, encoding="utf-8", pretty_print=True)

    def _exportDataStructures(self, schema, xsdElement):
        xs = self._xs 

        dataStructures = schema.getDataStructures()

        for dataStructure in dataStructures:
            e1 = XMLElement(QName(xs, "simpleType"))
            e1.set("name", self._getXSDTypeName( dataStructure))

            if dataStructure.allowedPattern != "":
                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:string")

                e3 = XMLElement(QName(xs, "pattern"))
                e3.set("value", dataStructure.allowedPattern)

                e2.append(e3)
                e1.append(e2)
            elif dataStructure.allowedValues:
                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:string")

                for value in dataStructure.allowedValues:
                    e3 = XMLElement(QName(xs, "enumeration"))
                    e3.set("value", value)

                    e2.append(e3)

                e1.append(e2)
            else:
                e2 = XMLElement(QName(xs, "restriction"))
                if dataStructure.baseStructure == "string":
                    e2.set("base", "xs:string")
                elif dataStructure.baseStructure == "boolean":
                    e2.set("base", "xs:boolean")

                e1.append(e2)

            xsdElement.append(e1)
    
    def _exportElementStructures(self, schema, xsdElement):
        xs = self._xs 

        elementStructures = schema.getElementStructures()

        for elementStructure in elementStructures:
            if elementStructure.allowedContent == "elements and text" or elementStructure.allowedContent == "elements only":
                e1 = XMLElement(QName(xs, "complexType"))
                e1.set("name",  self._getXSDTypeName( elementStructure))

                if elementStructure.allowedContent == "elements and text":
                    e1.set("mixed", "true")
                else:
                    e1.set("mixed", "false")

                e2 = XMLElement(QName(xs, "sequence"))

                for subelement in elementStructure.subelements:
                    e = schema.getElementStructureByReference(subelement.elementReference)

                    e3 = XMLElement(QName(xs, "element"))
                    e3.set("name", e.elementName)
                    e3.set("type", self._getXSDTypeName(e))
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
                    d = schema.getDataStructureByReference(a.dataStructure)

                    e4 = XMLElement(QName(xs, "attribute"))
                    e4.set("name", a.attributeName)
                    e4.set("type",  self._getXSDTypeName(d))
                    e4.set("use", "optional" if attribute.isOptional else "required")

                    e1.append(e4)

                xsdElement.append(e1)

            elif elementStructure.attributes == [] and elementStructure.allowedContent == "text only":
                e1 = XMLElement(QName(xs, "simpleType"))
                e1.set("name",  self._getXSDTypeName( elementStructure))

                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:string")

                e1.append(e2)
                xsdElement.append(e1)

            elif elementStructure.allowedContent == "text only":
                e1 = XMLElement(QName(xs, "complexType"))
                e1.set("name",  self._getXSDTypeName( elementStructure))

                e2 = XMLElement(QName(xs, "simpleContent"))

                e3 = XMLElement(QName(xs, "extension"))
                e3.set("base", "xs:string")

                e2.append(e3)
                e1.append(e2)

                for attribute in elementStructure.attributes:
                    a = schema.getAttributeStructureByReference(attribute.attributeReference)
                    d = schema.getDataStructureByReference(a.dataStructure)

                    e4 = XMLElement(QName(xs, "attribute"))
                    e4.set("name", a.attributeName)
                    e4.set("type",  self._getXSDTypeName(d))
                    e4.set("use", "optional" if attribute.isOptional else "required")

                    e3.append(e4)

                xsdElement.append(e1)

            elif elementStructure.allowedContent == "none":
                e1 = XMLElement(QName(xs, "complexType"))
                e1.set("name",  self._getXSDTypeName( elementStructure))

                for attribute in elementStructure.attributes:
                    a = schema.getAttributeStructureByReference(attribute.attributeReference)
                    d = schema.getDataStructureByReference(a.dataStructure)

                    e4 = XMLElement(QName(xs, "attribute"))
                    e4.set("name", a.attributeName)
                    e4.set("type", self._getXSDTypeName(d))
                    e4.set("use", "optional" if attribute.isOptional else "required")

                    e1.append(e4)

                xsdElement.append(e1)


xsdExporter = XSDExporter()

def exportSchemaAsXSD(schema, filePath):
    xsdExporter.exportSchema(schema, filePath) 

def generateSpecification(schema, filePath):
    with open(filePath, "w") as fileObject:

        rootElements = schema.getPossibleRootElementStructures()
        nonRootElements = schema.getNonRootElementStructures()
        elements = rootElements + nonRootElements 

        fileObject.write("## Table of Contents\n\n")

        for element in elements:
            fileObject.write("- [The &lt;{}&gt; element](#the-{}-element)\n".format(element.elementName, re.sub("_", "-", element.elementName)))

        for element in elements:
            fileObject.write("\n\n<br /><br />\n\n")
            fileObject.write("## The &lt;{}&gt; element\n\n".format(element.elementName))
            fileObject.write("### Attributes\n\n")

            aa = []

            if element.attributes:
                fileObject.write("| Name | Required | Allowed Values | Description |\n")
                fileObject.write("|---|---|---|---|\n")

                for attribute in element.attributes:
                    a = schema.getAttributeStructureByReference(attribute.attributeReference)
                    aa.append(a)

                    fileObject.write("| `{}` | {} | {} |  |\n".format(a.attributeName, "Required" if not attribute.isOptional else "Optional", ""))

                fileObject.write("\n")

            else:
                fileObject.write("None\n\n")

            fileObject.write("### Possible Subelements\n\n")

            ee = []

            if element.subelements:
                for subelement in element.subelements:
                    e = schema.getElementStructureByReference(subelement.elementReference)
                    ee.append(e)

                    fileObject.write("- &lt;{}&gt;\n".format(e.elementName))

                fileObject.write("\n")

            else:
                fileObject.write("None\n\n")

            fileObject.write("### Examples\n\n")
            fileObject.write("Below is shown an example of the `<{}>` element.\n\n".format(element.elementName))
            fileObject.write("```xml\n")

            attributeString = " ".join(["{}=\"...\"".format(a.attributeName) for a in aa])

            fileObject.write("<{} {}>\n".format(element.elementName, attributeString))

            for e in ee:
                fileObject.write("    <{}></{}>\n".format(e.elementName, e.elementName))

            fileObject.write("</{}>\n".format(element.elementName))
            fileObject.write("```\n\n")

