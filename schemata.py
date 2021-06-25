import logging 
import re
from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, Comment as XMLComment, QName, indent 

logger = logging.getLogger(__name__)

class Schema(object):
    def __init__(self):
        self.formatName = ""
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
        self.minimumValue = None
        self.maximumValue = None 

class ElementStructure(Structure):
    def __init__(self, reference = ""):
        super().__init__(reference)

        self.elementName = ""
        self.canBeRootElement = False 
        self.attributes = []
        self.allowedContent = "text only"
        self.subelements = None 
        self.elementCloseType = ""
        self.valueType = None 

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

        self._parseWhiteSpace(inputText, marker)

        metadata = self._parseComment(inputText, marker)

        if metadata != None:
            m = re.search(r"Format Name:\s*([.\s]+)\n", metadata)

            if m != None:
                schema.formatName = m.group(1).strip()

        self._parseWhiteSpace(inputText, marker)

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
                if p[0] == "minimumValue":
                    dataStructure.minimumValue = p[1]
                if p[0] == "maximumValue":
                    dataStructure.maximumValue = p[1]

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

        self._parseWhiteSpace(inputText, marker)

        metadata = self._parseComment(inputText, marker)

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
                if p[0] == "valueType":
                    elementStructure.valueType = p[1]

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
            propertyValue = self._parseSubelementList(inputText, marker)

        if propertyName == "pattern":
            propertyValue = self._parseString(inputText, marker)
        
        if propertyName == "allowedValues":
            propertyValue = self._parseList(inputText, marker)

        if propertyName == "minimumValue":
            propertyValue = self._parseInteger(inputText, marker)

        if propertyName == "maximumValue":
            propertyValue = self._parseInteger(inputText, marker)
        
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

            if item == None:
                break 

            items.append(item)

            n += 1

        if n == 0:
            return None 

        return items

    def _parseSubelementUsages(self, inputText, marker):

        item = self._parseElementUsageReference(inputText, marker)

        if item != None:
            return item 

        logging.debug("Didn't find element usage reference.")

        item = self._parseSubelementList(inputText, marker)

        if item != None:
            return item 

        logging.debug("Didn't find subelement list.")

        return None 

    def _parseSubelementList(self, inputText, marker):
        logging.debug("Attempting to parse a subelement list.")

        m = marker.copy()

        self._parseWhiteSpace(inputText, m)

        bracketType = ""
        separatorType = "comma"

        if cut(inputText, m.position) == "{":
            bracketType = "recurve"
            m.position += 1
        elif cut(inputText, m.position) == "[":
            bracketType = "square"
            m.position += 1
        else:
            return None 

        logging.debug("Identified bracket type: {}.".format(bracketType))

        self._parseWhiteSpace(inputText, m)

        items = []
        n = 0

        while m.position < len(inputText):
            self._parseWhiteSpace(inputText, m)

            if n > 0:
                c = cut(inputText, m.position)

                if n == 1:
                    if c == ",":
                        separatorType = "comma"
                        m.position += 1
                    elif c == "/":
                        separatorType = "slash"

                        if bracketType == "square":
                            raise SchemataParsingError("Expected ',' at position {}.".format(m.position))

                        m.position += 1

                elif n > 1:
                    if (separatorType == "comma" and c == ",") or (separatorType == "slash" and c == "/"):
                        m.position += 1
                    elif (separatorType == "comma" and c == "/") or (separatorType == "slash" and c == ","):
                        raise SchemataParsingError("Separators must be the same throughout a list (position {}).".format(m.position))
                    else:
                        break
            
            self._parseWhiteSpace(inputText, m)

            item = self._parseSubelementUsages(inputText, m)

            if item == None:
                break 

            items.append(item)

            n += 1

        logging.debug("Separator type: {}.".format(separatorType))
        logging.debug("List: {}.".format(items))

        if n == 0:
            return None 

        self._parseWhiteSpace(inputText, m)

        c = cut(inputText, m.position)

        if bracketType == "recurve" and c == "}":
            m.position += 1
        elif bracketType == "square" and c == "]":
            m.position += 1
        else:
            raise SchemataParsingError("Expected closing bracket at position {}.".format(m.position))

        if bracketType == "square" and separatorType == "comma":
            l = OrderedSubelementList()
            l.elements = items 
        elif bracketType == "recurve" and separatorType == "comma":
            l = UnorderedSubelementList()
            l.elements = items 
        else:
            return None 

        logging.debug("Found subelement list {}.".format(l))

        marker.position = m.position

        return l

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
            i = self._operators.index(o1)
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

    def _parseComment(self, inputText, marker):

        if cut(inputText, marker.position, 2) == "/*":
            marker.position += 2
            t = ""
            foundClosingTag = False 

            while marker.position < len(inputText):
                if cut(inputText, marker.position, 2) == "*/":
                    marker.position += 2
                    foundClosingTag = True 
                    break 
                else:
                    t += cut(inputText, marker.position)
                    marker.position += 1

            if not foundClosingTag:
                raise SchemataParsingError("Expected '*/' at position {}.".format(marker.position))

            return t.strip()
        else:
            return None 

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

    def exportSchema(self, schema, versionNumber, filePath):
        xs = self._xs

        logging.debug("Exporting schema for {} as XSD.".format(schema.formatName))

        e1 = XMLElement(QName(xs, "schema"))
        e1.set("elementFormDefault", "qualified")

        if schema.formatName != "":
            c1 = XMLComment(" An XSD file for {} ({}). ".format(schema.formatName, versionNumber))

            e1.append(c1)

        self._exportDataStructures(schema, e1)
        self._exportElementStructures(schema, e1)

        logging.debug("Exporting root elements.")

        roots = schema.getPossibleRootElementStructures()

        for root in roots:
            logging.debug("Exporting element <{}>.".format(root.elementName))

            e2 = XMLElement(QName(xs, "element"))
            e2.set("name", root.elementName)
            e2.set("type", self._getXSDTypeName(root))

            e1.append(e2)

        tree = XMLElementTree(e1)
        indent(tree, space="    ")
        tree.write(filePath, xml_declaration=True, encoding="utf-8", pretty_print=True)

    def _exportDataStructures(self, schema, xsdElement):
        xs = self._xs 

        logging.debug("Exporting data structures.")

        dataStructures = schema.getDataStructures()

        for dataStructure in dataStructures:
            logging.debug("Exporting data structure '{}'.".format(dataStructure.reference))

            e1 = XMLElement(QName(xs, "simpleType"))
            e1.set("name", self._getXSDTypeName(dataStructure))

            if dataStructure.baseStructure == "string":
                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:string")

                if dataStructure.allowedPattern != "":
                    e3 = XMLElement(QName(xs, "pattern"))
                    e3.set("value", dataStructure.allowedPattern)

                    e2.append(e3)

                elif dataStructure.allowedValues:
                    for value in dataStructure.allowedValues:
                        e3 = XMLElement(QName(xs, "enumeration"))
                        e3.set("value", value)

                        e2.append(e3)

                e1.append(e2)

            elif dataStructure.baseStructure == "integer":
                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:integer")

                if dataStructure.minimumValue != None:
                    e3 = XMLElement(QName(xs, "minInclusive"))
                    e3.set("value", str(dataStructure.minimumValue))

                    e2.append(e3)

                if dataStructure.maximumValue != None:
                    e3 = XMLElement(QName(xs, "maxInclusive"))
                    e3.set("value", str(dataStructure.maximumValue))

                    e2.append(e3)

                e1.append(e2)

            elif dataStructure.baseStructure == "boolean":
                e2 = XMLElement(QName(xs, "restriction"))
                e2.set("base", "xs:boolean")

                e1.append(e2)


            xsdElement.append(e1)
    
    def _exportElementStructures(self, schema, xsdElement):
        xs = self._xs 

        logging.debug("Exporting element structures.")

        elementStructures = schema.getElementStructures()

        for elementStructure in elementStructures:
            logging.debug("Exporting element '{}' <{}>.".format(elementStructure.reference, elementStructure.elementName))

            hasAttributes = len(elementStructure.attributes) > 0
            xsdType = "simpleType" if not hasAttributes and elementStructure.allowedContent == "text only" else "complexType"

            e1 = XMLElement(QName(xs, xsdType))
            e1.set("name", self._getXSDTypeName(elementStructure))

            if elementStructure.allowedContent == "elements and text" or elementStructure.allowedContent == "elements only":

                if elementStructure.allowedContent == "elements and text":
                    e1.set("mixed", "true")
                else:
                    e1.set("mixed", "false")

                self._exportSubelements(schema, elementStructure.subelements, e1)
                self._exportAttributes(schema, elementStructure.attributes, e1)

            elif elementStructure.attributes == [] and elementStructure.allowedContent == "text only":
                e2 = XMLElement(QName(xs, "restriction"))
                if elementStructure.valueType != None:
                    if elementStructure.valueType == "integer":
                        e2.set("base", "xs:integer")
                    elif elementStructure.valueType == "boolean":
                        e2.set("base", "xs:boolean")
                    else:
                        d = schema.getDataStructureByReference(elementStructure.valueType)
                        e2.set("base", self._getXSDTypeName(d))
                else:
                    e2.set("base", "xs:string")

                e1.append(e2)

            elif elementStructure.allowedContent == "text only":
                e2 = XMLElement(QName(xs, "simpleContent"))

                e3 = XMLElement(QName(xs, "extension"))
                if elementStructure.valueType != None:
                    if elementStructure.valueType == "integer":
                        e3.set("base", "xs:integer")
                    elif elementStructure.valueType == "boolean":
                        e3.set("base", "xs:boolean")
                    else:
                        d = schema.getDataStructureByReference(elementStructure.valueType)
                        e3.set("base", self._getXSDTypeName(d))
                else:
                    e3.set("base", "xs:string")

                e2.append(e3)
                e1.append(e2)

                self._exportAttributes(schema, elementStructure.attributes, e3)

            elif elementStructure.allowedContent == "none":
                self._exportAttributes(schema, elementStructure.attributes, e1)

            xsdElement.append(e1)

    def _exportSubelements(self, schema, elements, xsdElement):
        xs = self._xs 

        xsdIndicatorType = "sequence"

        if isinstance(elements, OrderedSubelementList):
            e1 = XMLElement(QName(xs, "sequence"))
        if isinstance(elements, UnorderedSubelementList):
            xsdIndicatorType = "choice"

            e1 = XMLElement(QName(xs, "choice"))
            e1.set("minOccurs", "0")
            e1.set("maxOccurs", "unbounded")
        if elements == None:
            return 

        for element in elements.elements:
            e = schema.getElementStructureByReference(element.elementReference)

            e3 = XMLElement(QName(xs, "element"))
            e3.set("name", e.elementName)
            e3.set("type", self._getXSDTypeName(e))
            p = element.minimumNumberOfOccurrences
            q = element.maximumNumberOfOccurrences 

            if xsdIndicatorType == "sequence":
                if p != 1:
                    e3.set("minOccurs", str(p))

                if q != 1:
                    e3.set("maxOccurs", "unbounded" if q == -1 else str(q))

            e1.append(e3)

        xsdElement.append(e1)

    def _exportAttributes(self, schema, attributes, xsdElement):
        xs = self._xs 
        baseTypes = ["string", "integer", "boolean"]

        for attribute in attributes:
            a = schema.getAttributeStructureByReference(attribute.attributeReference)

            e1 = XMLElement(QName(xs, "attribute"))
            e1.set("name", a.attributeName)

            if a.dataStructure in baseTypes:
                if a.dataStructure == "string":
                    e1.set("type", "xs:string")
                if a.dataStructure == "integer":
                    e1.set("type", "xs:integer")
                if a.dataStructure == "boolean":
                    e1.set("type", "xs:boolean")
            else:
                d = schema.getDataStructureByReference(a.dataStructure)
                e1.set("type", self._getXSDTypeName(d))

            e1.set("use", "optional" if attribute.isOptional else "required")

            xsdElement.append(e1)



xsdExporter = XSDExporter()

def exportSchemaAsXSD(schema, versionNumber, filePath):
    xsdExporter.exportSchema(schema, versionNumber, filePath) 

def generateSpecification(schema, filePath):
    with open(filePath, "w") as fileObject:

        rootElements = schema.getPossibleRootElementStructures()
        nonRootElements = schema.getNonRootElementStructures()
        elements = rootElements + nonRootElements 

        fileObject.write("# {} Specification\n\n".format(schema.formatName))
        fileObject.write("This document gives the specification for {}.\n\n".format(schema.formatName))

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
                for subelement in element.subelements.elements:
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

            if aa:
                fileObject.write("<{} {}>\n".format(element.elementName, attributeString))
            else:
                fileObject.write("<{}>\n".format(element.elementName))

            for e in ee:
                fileObject.write("    <{}></{}>\n".format(e.elementName, e.elementName))

            fileObject.write("</{}>\n".format(element.elementName))
            fileObject.write("```\n\n")

