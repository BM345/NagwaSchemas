import logging 
import schemata 
import glob 
from lxml.etree import parse, XMLSchema 

SCHEMA_FILE_PATHS = [
    ("roles/roles.schema", "roles/roles.xsd", "roles/examples/*"),
]

def generate():
    parser = schemata.Parser()

    for filePath in SCHEMA_FILE_PATHS:
        with open(filePath[0], "r") as fileObject:
            text = fileObject.read()
            schema = parser.parseSchema(text)

            schemata.exportSchemaAsXSD(schema, filePath[1])

def validate():
    for filePath in SCHEMA_FILE_PATHS:
        xsdDocument = parse(filePath[1])
        schema = XMLSchema(xsdDocument)

        fps = glob.glob(filePath[2])

        for fp in fps:
            xmlDocument = parse(fp)
            logging.info("Validating {} ... {}.".format(fp, schema.validate(xmlDocument)))

            schema.assertValid(xmlDocument)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    generate()
    validate()
