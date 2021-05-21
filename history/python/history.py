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
        super().__init__(takenAt, takenBy, "created_entity")

class CreateNewVersionAction(Action):
    def __init__(self, takenAt, takenBy, reference, fileName):
        super().__init__(takenAt, takenBy, "created_new_version")

        self.reference = reference 
        self.fileName = fileName 

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "version")
        e2.text = self.reference 

        e3 = XMLSubelement(e1, "file_name")
        e3.text = self.fileName 

        return e1 

class ChangeWorkflowAction(Action):
    def __init__(self, takenAt, takenBy, newWorkflowReference):
        super().__init__(takenAt, takenBy, "changed_workflow")

        self.newWorkflowReference = newWorkflowReference 

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "new_workflow")
        e2.text = self.newWorkflowReference 

        return e1 

class ChangeWorkflowStatusAction(Action):
    def __init__(self, takenAt, takenBy, transition, newWorkflowStatusReference):
        super().__init__(takenAt, takenBy, "changed_workflow_status")

        self.transition = transition
        self.newWorkflowStatusReference = newWorkflowStatusReference 

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "transition")
        e2.text = self.transition 

        e3 = XMLSubelement(e1, "new_workflow_status")
        e3.text = self.newWorkflowStatusReference 

        return e1 

class ChangeAssigneeAction(Action):
    def __init__(self, takenAt, takenBy, newAssignee):
        super().__init__(takenAt, takenBy, "changed_assignee")

        self.newAssignee = newAssignee 

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "new_assignee")
        e2.text = self.newAssignee 

        return e1 

class ChangePriorityAction(Action):
    def __init__(self, takenAt, takenBy, newPriority):
        super().__init__(takenAt, takenBy, "changed_priority")

        self.newPriority = newPriority 

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "new_priority")
        e2.text = self.newPriority 

        return e1 

class AddCommentAction(Action):
    def __init__(self, takenAt, takenBy, commentReference, commentText):
        super().__init__(takenAt, takenBy, "add_comment")

        self.commentReference = commentReference
        self.commentText = commentText 

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "comment_reference")
        e2.text = self.commentReference 

        e3 = XMLSubelement(e1, "comment_text")
        e3.text = self.commentText 

        return e1 
