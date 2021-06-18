from schemata import * 
import logging 

logging.basicConfig(level=logging.DEBUG)

with open("test1.schema", "r") as fileObject:
    text = fileObject.read()

    parser = Parser()

    schema = parser.parseSchema(text)

    print(len(schema.structures))
    print(schema.structures[0].reference)
    print(schema.structures[0].allowedPattern)
    print(schema.structures[2].reference)
    print(schema.structures[2].allowedValues)

    exportSchemaAsXSD(schema, "test1.xsd")