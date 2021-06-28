import logging 
import schemata 
import glob 
import argparse 
from lxml.etree import parse, XMLSchema 

SCHEMAS = [
    "roles",
    "workflow",
    "history",
    "scope"
]

REPOSITORY_VERSION_NUMBER = "v1.2.0"

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

            schemata.exportSchemaAsXSD(schema, REPOSITORY_VERSION_NUMBER, fp2)
            schemata.exportSchemaAsXSD(schema, REPOSITORY_VERSION_NUMBER, fp3)

def validate():
    for s in SCHEMAS:
        fp1 = "{}/{}.xsd".format(s, s)

        xsdDocument = parse(fp1)
        schema = XMLSchema(xsdDocument)

        logging.info("Checking that all valid examples pass when validated against the XSD file.")

        fps = glob.glob("{}/examples/*.xml".format(s))

        for fp in fps:
            xmlDocument = parse(fp)
            isValid = schema.validate(xmlDocument)

            if isValid == True:
                logging.info(" - {} passes.".format(fp))
            else:
                logging.info(" - {} does not pass.".format(fp))

                schema.assertValid(xmlDocument)

        logging.info("Checking that all invalid examples fail when validated against the XSD file.")

        fps = glob.glob("{}/invalid_examples/*.xml".format(s))

        for fp in fps:
            xmlDocument = parse(fp)
            isValid = schema.validate(xmlDocument)

            if isValid == False:
                logging.info(" - {} fails.".format(fp))
            else:
                logging.info(" - {} does not fail.".format(fp))

                raise Exception("{} should fail validation, but doesn't.".format(fp))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("action", default="generate_xsd_files")
    
    arguments = argumentParser.parse_args()

    if arguments.action == "generate_specification":
        parser = schemata.Parser()
        schema = parser.parseSchemaFromFile("semantic_tags/semantic_tags.schema")
        schemata.generateSpecification(schema, "semantic_tags/semantic_tags_xml_specification.md")
        schema = parser.parseSchemaFromFile("reading_activity/reading_activity.schema")
        schemata.generateSpecification(schema, "reading_activity/reading_activity_xml_specification.md")
    else:
        generate()
        validate()
