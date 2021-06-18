import logging 
import schemata 
import glob 
from lxml.etree import parse, XMLSchema 

SCHEMAS = [
    "roles"
]

def generate():
    parser = schemata.Parser()

    for s in SCHEMAS:
        with open("{}/{}.schema".format(s, s), "r") as fileObject:
            text = fileObject.read()
            schema = parser.parseSchema(text)

            schemata.exportSchemaAsXSD(schema, "{}/{}.xsd".format(s, s))
            schemata.exportSchemaAsXSD(schema, "generated_schema_files/{}.xsd".format(s))

def validate():
    for s in SCHEMAS:
        xsdDocument = parse("{}/{}.xsd".format(s, s))
        schema = XMLSchema(xsdDocument)

        fps = glob.glob("{}/examples/*".format(s))

        for fp in fps:
            xmlDocument = parse(fp)
            logging.info("Validating {} ... {}.".format(fp, schema.validate(xmlDocument)))

            schema.assertValid(xmlDocument)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    generate()
    validate()
