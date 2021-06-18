from schemata import * 
import logging 
from lxml.etree import parse, XMLSchema

logging.basicConfig(level=logging.DEBUG)

with open("test1.schema", "r") as fileObject:
    text = fileObject.read()

    parser = Parser()

    schema = parser.parseSchema(text)

    exportSchemaAsXSD(schema, "test1.xsd")

with open("roles/roles.schema", "r") as fileObject:
    text = fileObject.read()

    parser = Parser()

    schema = parser.parseSchema(text)

    #exportSchemaAsXSD(schema, "roles.xsd")

    xsd = parse("roles.xsd")
    xsd2 = XMLSchema(xsd)

    d = parse("roles/examples/cds.roles.xml")

    print(xsd2.validate(d))
    xsd2.assertValid(d)

