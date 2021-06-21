import logging 
import schemata 
import glob 
from lxml.etree import parse, XMLSchema 

SCHEMAS = [
    "roles",
    "workflow",
    "history"
]

def generate():
    parser = schemata.Parser()

    for s in SCHEMAS:
        fp1 = "{}/{}.schema".format(s, s)
        fp2 = "{}/{}.xsd".format(s, s)
        fp3 = "generated_schema_files/{}.xsd".format(s)

        with open(fp1, "r") as fileObject:
            logging.info("Generating an XSD file from {}.".format(fp1))

            text = fileObject.read()
            schema = parser.parseSchema(text)

            schemata.exportSchemaAsXSD(schema, fp2)
            schemata.exportSchemaAsXSD(schema, fp3)

def validate():
    for s in SCHEMAS:
        fp1 = "{}/{}.xsd".format(s, s)

        xsdDocument = parse(fp1)
        schema = XMLSchema(xsdDocument)

        fps = glob.glob("{}/examples/*".format(s))

        for fp in fps:
            xmlDocument = parse(fp)
            logging.info("Validating {} ... {}.".format(fp, schema.validate(xmlDocument)))

            schema.assertValid(xmlDocument)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    generate()
    validate()
