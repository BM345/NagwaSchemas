from migrate import * 
import logging
import argparse 
import csv

def survey():

    files = glob.glob("questions_data/*")

    multipart_question_ids = []
    issues = []

    for f in files:

        tree = etree.parse(f)

        question_id = tree.xpath("/*")[0].get("id")
        number_of_parts = len(tree.xpath("/*/mcq | /*/mrq | /*/frq"))
        is_multipart = "Multipart" if number_of_parts > 1 else ""

        #print("{}, {} {}".format(question_id, number_of_parts, is_multipart))

        multipart_question_ids.append([question_id, number_of_parts])

        with open(f, "r") as fileObject:
            text = fileObject.read()

        if text.find("categories of energy") >= 0:
            issues.append(question_id)
            print(question_id)

    print(len(issues))



    return 

    with open("multipart_question_ids.csv", "w") as fileObject:
        csvWriter = csv.writer(fileObject)

        for row in multipart_question_ids:
            csvWriter.writerow(row)



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("action")

    arguments = parser.parse_args()

    if arguments.action == "download_question_files":
        downloadQuestionFiles(10000)
    if arguments.action == "survey":
        survey()