from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, indent, parse
import re 
import datetime 

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

class History(object):
    def __init__(self, contentEntityType = "", contentEntityId = ""):
        self.contentEntityType = contentEntityType
        self.contentEntityId = contentEntityId
        self.state = State() 
        self.actions = []

    def addAction(self, action, updateState = True):
        self.actions.append(action)

        if updateState:
            if isinstance(action, CreateNewVersionAction):
                self.state.versions.append(Version(action.reference, action.fileName))
            if isinstance(action, ChangeWorkflowAction):
                self.state.workflowReference = action.newWorkflowReference 
            if isinstance(action, ChangeWorkflowStatusAction):
                self.state.workflowStatusReference = action.newWorkflowStatusReference 
            if isinstance(action, ChangeAssigneeAction):
                self.state.assignee = action.newAssignee 
            if isinstance(action, ChangePriorityAction):
                self.state.priority = action.newPriority 
            if isinstance(action, AddLabelAction):
                self.state.labels.append(action.label) 
            if isinstance(action, RemoveLabelAction):
                self.state.labels.remove(action.label) 
            if isinstance(action, AddWatcherAction):
                self.state.watchers.append(action.watcher) 
            if isinstance(action, RemoveWatcherAction):
                self.state.watchers.remove(action.watcher)

    def getComments(self):
        actions = [action for action in self.actions if action.type == "added_comment"]
        comments = [Comment(action.takenAt, action.takenBy, action.commentReference, action.commentText) for action in actions]

        return comments 

    def toXML(self):
        e1 = XMLElement("history")
        e1.set("for_entity", "{}/{}".format(self.contentEntityType, self.contentEntityId))

        e1.append(self.state.toXML())

        e2 = XMLSubelement(e1, "actions")

        for action in self.actions:
            e2.append(action.toXML())

        return e1 

    def save(self, filePath):
        tree = XMLElementTree(self.toXML())
        indent(tree, space = "    ")
        tree.write(filePath, xml_declaration = True, encoding = "utf-8", pretty_print = True)

    @staticmethod
    def load(filePath):
        return loadHistoryFromXML(filePath)


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
    def __init__(self, reference = "", fileName = ""):
        self.reference = reference
        self.fileName = fileName

    def toXML(self):
        e1 = XMLElement("version")
        e1.set("file_name", self.fileName)
        e1.text = self.reference 

        return e1 

class Comment(object):
    def __init__(self, madeAt, madeBy, reference, text):
        self.madeAt = madeAt 
        self.madeBy = madeBy 
        self.reference = reference 
        self.text = text 

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

class AddLabelAction(Action):
    def __init__(self, takenAt, takenBy, label):
        super().__init__(takenAt, takenBy, "add_label")

        self.label = label

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "label")
        e2.text = self.label 

        return e1 

class RemoveLabelAction(Action):
    def __init__(self, takenAt, takenBy, label):
        super().__init__(takenAt, takenBy, "remove_label")

        self.label = label

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "label")
        e2.text = self.label 

        return e1 

class AddWatcherAction(Action):
    def __init__(self, takenAt, takenBy, watcher):
        super().__init__(takenAt, takenBy, "add_watcher")

        self.watcher = watcher

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "watcher")
        e2.text = self.watcher 

        return e1 

class RemoveWatcherAction(Action):
    def __init__(self, takenAt, takenBy, watcher):
        super().__init__(takenAt, takenBy, "remove_watcher")

        self.watcher = watcher

    def toXML(self):
        e1 = super().toXML()

        e2 = XMLSubelement(e1, "watcher")
        e2.text = self.watcher 

        return e1 

def loadHistoryFromXML(filePath):
    tree = parse(filePath)
    root = tree.getroot()

    if root.tag != "history":
        raise ValueError("The XML document provided is not a History XML document.")

    history = History()

    uei = tree.xpath("/history/@for_entity")[0]
    entityType = uei[:uei.find("/")]
    entityId = uei[uei.find("/"):]

    history.contentEntityType = entityType 
    history.contentEntityId = entityId 
    history.state.workflowReference = tree.xpath("/history/state/workflow")[0].text 
    history.state.workflowStatusReference = tree.xpath("/history/state/workflow_status")[0].text 
    history.state.assignee = tree.xpath("/history/state/assignee")[0].text 
    history.state.priority = tree.xpath("/history/state/priority")[0].text 

    developers = tree.xpath("/history/state/developers/developer")
    labels = tree.xpath("/history/state/labels/label")
    watchers = tree.xpath("/history/state/watchers/watcher")
    versions = tree.xpath("/history/state/versions/version")

    for developer in developers:
        d = Developer()

        d.workflowReference = developer.xpath("./@workflow")[0]
        d.role = developer.xpath("./@role")[0]
        d.emailAddress = developer.text 

        history.state.developers.append(d)

    for label in labels:
        history.state.labels.append(label.text)

    for watcher in watchers:
        history.state.watchers.append(watcher.text)

    for version in versions:
        v = Version()

        v.fileName = version.xpath("./@file_name")[0]
        v.reference = version.text 

        history.state.versions.append(v)

    actions = tree.xpath("/history/actions/action")

    for action in actions:
        taken_at = datetime.datetime.strptime(action.xpath("./@taken_at")[0], DATETIME_FORMAT)
        taken_by =  action.xpath("./@taken_by")[0]
        t = action.xpath("./@type")[0]

        a = None 

        if t == "created_entity":
            a = CreateEntityAction(taken_at, taken_by)
        if t == "created_new_version":
            a = CreateNewVersionAction(taken_at, taken_by, "", "")
            a.reference = action.xpath("./version")[0].text 
            a.fileName = action.xpath("./file_name")[0].text 
        if t == "changed_workflow":
            a = ChangeWorkflowAction(taken_at, taken_by, "")
            a.newWorkflowReference = action.xpath("./new_workflow")[0].text 
        if t == "changed_workflow_status":
            a = ChangeWorkflowStatusAction(taken_at, taken_by, "", "")
            a.transition = action.xpath("./transition")[0].text 
            a.newWorkflowStatusReference = action.xpath("./new_workflow_status")[0].text 
        if t == "changed_assignee":
            a = ChangeAssigneeAction(taken_at, taken_by, "")
            a.newAssignee = action.xpath("./new_assignee")[0].text 
        if t == "changed_priority":
            a = ChangePriorityAction(taken_at, taken_by, "")
            a.newPriority = action.xpath("./new_priority")[0].text 
        if t == "added_comment":
            a = AddCommentAction(taken_at, taken_by, "", "")
            a.commentReference = action.xpath("./comment_reference")[0].text 
            a.commentText = action.xpath("./comment_text")[0].text 
        if t == "added_label":
            a = AddLabelAction(taken_at, taken_by, "")
            a.label = action.xpath("./label")[0].text 
        if t == "removed_label":
            a = RemoveLabelAction(taken_at, taken_by, "")
            a.label = action.xpath("./label")[0].text 
        if t == "added_watcher":
            a = AddWatcherAction(taken_at, taken_by, "")
            a.watcher = action.xpath("./watcher")[0].text 
        if t == "removed_watcher":
            a = RemoveWatcherAction(taken_at, taken_by, "")
            a.watcher = action.xpath("./watcher")[0].text 

        if a != None:
            history.actions.append(a)

    return history 


