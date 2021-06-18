from schemata import * 
import logging 
from lxml.etree import parse, XMLSchema

logging.basicConfig(level=logging.DEBUG)

with open("test1.schema", "r") as fileObject:
    text = fileObject.read()

    parser = Parser()

    schema = parser.parseSchema(text)

    exportSchemaAsXSD(schema, "test1.xsd")

