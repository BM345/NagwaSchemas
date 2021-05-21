from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, indent, parse
import re 
import datetime 

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

class History(object):
    def __init__(self):
        self.contentEntityType = ""
        self.contentEntityId = ""
        self.state = State() 
        self.actions = []

    def toXML(self):
        e1 = XMLElement("history")
        e1.set("for_content_entity", "{}/{}".format(self.contentEntityType, self.contentEntityId))

        e1.append(self.state.toXML())

        e2 = XMLSubelement(e1, "actions")

        for action in self.actions:
            e2.append(action.toXML())

        return e1 

    def save(self, filePath):
        tree = XMLElementTree(self.toXML())
        indent(tree, space = "    ")
        tree.write(filePath, xml_declaration = True, encoding = "utf-8", pretty_print = True)


class State(object):
    def __init__(self):
        self.workflowReference = ""
        self.workflowStatusReference = ""
        self.developers = []
        self.assignee = ""
        self.priority = ""
        self.labels = []
        self.watchers = []
        self.versions = []

    def toXML(self):
        e1 = XMLElement("state")

        e2 = XMLSubelement(e1, "workflow")
        e2.text = self.workflowReference 

        e3 = XMLSubelement(e1, "workflow_status")
        e3.text = self.workflowStatusReference 

        e4 = XMLSubelement(e1, "developers")

        for developer in self.developers:
            e4.append(developer.toXML())

        e5 = XMLSubelement(e1, "assignee")
        e5.text = self.assignee 

        e6 = XMLSubelement(e1, "priority")
        e6.text = self.priority  

        e7 = XMLSubelement(e1, "labels")

        for label in self.labels:
            e8 = XMLSubelement(e7, "label")
            e8.text = label  

        e9 = XMLSubelement(e1, "watchers")

        for watcher in self.watchers:
            e10 = XMLSubelement(e9, "watcher")
            e10.text = watcher  

        e11 = XMLSubelement(e1, "versions")

        for version in self.versions:
            e11.append(version.toXML())

        return e1 

class Developer(object):
    def __init__(self):
        self.workflowReference = ""
        self.role = ""
        self.emailAddress = ""

    def toXML(self):
        e1 = XMLElement("developer")
        e1.set("workflow", self.workflowReference)
        e1.set("role", self.role)
        e1.text = self.emailAddress 

        return e1 

class Version(object):
    def __init__(self):
        self.reference = ""
        self.fileName = ""

    def toXML(self):
        e1 = XMLElement("version")
        e1.set("file_name", self.fileName)
        e1.text = self.reference 

        return e1 

class Action(object):
    def __init__(self, takenAt, takenBy, _type):
        self.takenAt = takenAt 
        self.takenBy = takenBy 
        self.type = _type 

    def toXML(self):
        e1 = XMLElement("action")
        e1.set("taken_at", self.takenAt.strftime(DATETIME_FORMAT))
        e1.set("taken_by", self.takenBy)
        e1.set("type", self.type)

        return e1 

class CreateEntityAction(Action):
    def __init__(self, takenAt, takenBy):
        super(CreateEntityAction, self).__init__(takenAt, takenBy, "created_entity")
