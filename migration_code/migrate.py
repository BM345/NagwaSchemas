import os
import glob
import requests 
import logging 
import csv
import re 
import argparse
import datetime 
from headers import headers 
import questions 
from lxml import etree 

logger = logging.getLogger(__name__)

CDS_BASE_URL = "https://cds.nagwa.com"

def downloadQuestionFiles(numberOfQuestions = 100):

    #files = glob.glob("questions_data/*")

    #for f in files:
    #    os.remove(f)

    questionIds = []

    with open("question_ids_data/2021-04-21 Physics - All Data - All Data - Questions.csv", "r") as fileObject:
        csvReader = csv.reader(fileObject)

        for row in csvReader:
            questionIds.append(row[0])

    url1 = CDS_BASE_URL + "/{}/files/"

    session = requests.Session()

    for questionId in questionIds[4090:numberOfQuestions]:

        logger.info("Finding the latest version of {}.".format(questionId))

        r = session.get(url1.format(questionId), headers = headers)
        t = r.text
        m = re.findall(r"(\/super\.admin\/single\/\d{12}\/view\/\d{12}\.(question|single)\.xml\/(\d+)\/)", t)
        versions = [(match[0], int(match[2])) for match in m]
        versions = sorted(versions, key = lambda v: v[1], reverse=True)
        latestVersion = versions[0]

        logger.info("Found the latest version, {}, at {}.".format(latestVersion[1], latestVersion[0]))
        logger.info("Downloading question XML for {}, version {}.".format(questionId, latestVersion[1]))

        r = session.get(CDS_BASE_URL + latestVersion[0], headers = headers)
        r.encoding = "utf-8-sig"

        with open(os.path.join("questions_data", "{}.{}.question.xml".format(questionId, latestVersion[1])), "w", encoding="utf-8") as fileObject:
            fileObject.write(r.text)

def migrate():

    files = glob.glob("migrated_questions_data/*")

    for f in files:
        os.remove(f)

    files = glob.glob("questions_data/*")

    for f in files:
        m = re.search("(\d{12})\.(\d+)\.question\.xml", f)
        version = int(m.group(2))

        tree = etree.parse(f)

        question_id = tree.xpath("/*")[0].get("id")
        sourceId = tree.xpath("/*/source_id")[0].text
        developerName = tree.xpath("/*/developer_name")[0].text 
        developerEmailAddress = tree.xpath("/*/developer_email")[0].text
        language = tree.xpath("/*")[0].get("language")
        dialect = tree.xpath("/*")[0].get("dialect")
        calendar = tree.xpath("/*")[0].get("calendar")
        currency = tree.xpath("/*")[0].get("currency")
        unitSystem = tree.xpath("/*")[0].get("unit_system")
        title = ""

        if len(tree.xpath("/*/title")) > 0:
            title = tree.xpath("/*/title")[0].text 

        parts = [e for e in tree.xpath("/*/*") if e.tag in ["statement", "mcq", "mrq", "frq"]]

        question = questions.Question()
        question.id = question_id 
        question.version = version 
        question.lastModificationDate = datetime.datetime.now()
        question.attribution.sourceId = sourceId
        question.addDeveloper("writer", developerName, developerEmailAddress)

        if language == "en":
            question.language.name = "English"

        if dialect == "american":
            question.addDialect("American")
        if dialect == "british":
            question.addDialect("British")
        if dialect == "american british":
            question.addDialect("American")
            question.addDialect("British")

        if unitSystem == "si":
            question.addUnitSystem("SI")
        if unitSystem == "usc":
            question.addUnitSystem("USC")
        if unitSystem == "si usc":
            question.addUnitSystem("SI")
            question.addUnitSystem("USC")

        question.title = title 

        partMap = {
            "statement": "information",
            "mcq": "mcq",
            "mrq": "mcq",
            "frq": "frq"
        }

        for part in parts:
            p = question.addPart(partMap.get(part.tag, ""))

            if part.tag == "mcq" or part.tag == "mrq":
                rp = p.addChoicesResponseFormat()

                keysAndDistractors = [e for e in part.xpath("./*") if e.tag in ["key", "distractor"]]

                for kd in keysAndDistractors:
                    choice = rp.addChoice()
                    choice.isCorrectAnswer = True if kd.tag == "key" else False 




        


        question.save("migrated_questions_data/" + question.id + ".question.xml")




if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("action")

    arguments = parser.parse_args()

    if arguments.action == "download_question_files":
        downloadQuestionFiles()
    if arguments.action == "migrate":
        migrate()
