from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, indent, parse
import re 

def makeReference(name):
    name = name.strip()
    name = name.lower()
    name = name.replace(" ", "_")

    return name 


class Workflow(object):
    def __init__(self, name = "", description = "", reference = ""):
        self.reference = reference
        self.name = name 
        self.description = description 
        self.initialStatus = None 
        self.finalStatus = None 
        self.statuses = []
        self.transitions = []

    def getStatusByReference(self, reference):
        return [status for status in self.statuses if status.reference == reference][0]

    def getTransitionByReference(self, reference):
        return [transition for transition in self.transitions if transition.reference == reference][0]

    def addStatus(self, name, description = "", reference = "", category = "", _type = ""):
        status = Status()

        status.name = name 
        status.description = description 
        status.reference = reference 
        status.category = category 
        status.type = _type 

        self.statuses.append(status)

        return status 

    def addTransition(self, _from, _to, name, buttonText, description = "", reference = "", _type = "send", commentRequired = False, autoAssignTo = ""):
        transition = Transition()

        transition._from = _from 
        transition._to = _to 
        transition.name = name 
        transition.buttonText = buttonText 
        transition.description = description 
        transition.reference = reference 
        transition.type = _type 
        transition.commentRequired = commentRequired
        transition.autoAssignTo = autoAssignTo 

        self.transitions.append(transition)

        return transition 

    def setAllReferences(self):
        self.reference = makeReference(self.name)

        srs = []

        for status in self.statuses:
            sr = makeReference(status.name)
            n = 1

            while sr in srs:
                n += 1
                sr = "{}_{}".format(makeReference(status.name), n)

            srs.append(sr)

            status.reference = sr 

        trs = [] 

        for transition in self.transitions:
            tr = makeReference(transition.name)
            n = 1

            while tr in trs:
                n += 1
                tr = "{}_{}".format(makeReference(transition.name), n)

            trs.append(tr)

            transition.reference = tr

    def toXML(self):
        e1 = XMLElement("workflow")
        e1.set("reference", self.reference)

        e2 = XMLElement("name")
        e2.text = self.name 
        e1.append(e2)

        if self.description != "":
            e3 = XMLElement("description")
            e3.text = self.description 
            e1.append(e3)

        e4 = XMLElement("statuses")
        e4.set("initial", self.initialStatus.reference)
        e4.set("final", self.finalStatus.reference)
        
        for status in self.statuses:
            e4.append(status.toXML())

        e1.append(e4)

        e5 = XMLElement("transitions")

        for transition in self.transitions:
            e5.append(transition.toXML())

        e1.append(e5)

        return e1 

    def save(self, filePath, setAllReferences = True):
        if setAllReferences:
            self.setAllReferences()

        tree = XMLElementTree(self.toXML())
        indent(tree, space = "    ")
        tree.write(filePath, xml_declaration = True, encoding = "utf-8", pretty_print = True)

    @staticmethod 
    def load(filePath):
        return loadWorkflowFromXML(filePath)


class Status(object):
    def __init__(self):
        self.reference = ""
        self.category = ""
        self.type = ""
        self.name = ""
        self.description = ""

    def toXML(self):
        e1 = XMLElement("status")
        e1.set("reference", self.reference)

        if self.category != "":
            e1.set("category", self.category)

        if self.type == "automated_processing":
            e1.set("type", self.type)

        e2 = XMLElement("name")
        e2.text = self.name 
        e1.append(e2)

        if self.description != "":
            e3 = XMLElement("description")
            e3.text = self.description 
            e1.append(e3)

        return e1 


class Transition(object):
    def __init__(self):
        self.reference = ""
        self._from = None 
        self._to = None 
        self.type = ""
        self.commentRequired = False 
        self.autoAssignTo = ""
        self.name = ""
        self.buttonText = ""
        self.description = ""
        self.rules = []

    def toXML(self):
        e1 = XMLElement("transition")
        e1.set("reference", self.reference)
        e1.set("from", self._from.reference)
        e1.set("to", self._to.reference)
        e1.set("type", self.type)

        if self.commentRequired:
            e1.set("comment_required", "true")

        if self.autoAssignTo != "":
            e1.set("auto_assign_to", self.autoAssignTo)

        e2 = XMLElement("name")
        e2.text = self.name 
        e1.append(e2)

        if self.buttonText != "":
            e3 = XMLElement("button_text")
            e3.text = self.buttonText 
            e1.append(e3)

        if self.description != "":
            e4 = XMLElement("description")
            e4.text = self.description 
            e1.append(e4)

        if self.rules:
            e5 = XMLElement("rules")

            for rule in self.rules:
                e5.append(rule.toXML())

            e1.append(e5)

        return e1 


class Rule(object):
    def __init__(self):
        self.allowIf = None 

    def toXML(self):
        e1 = XMLElement("rule")
        e1.set("allow_if", "")

        return e1 

class RolesRule(Rule):
    def __init__(self, roles = []):
        self.roles = roles 

    def toXML(self):
        e1 = XMLElement("rule")
        e1.set("allow_if", "role in {}".format(self.roles))

        return e1 

class InPastStatusesRule(Rule):
    def __init__(self, status):
        self.status = status 

    def toXML(self):
        e1 = XMLElement("rule")
        e1.set("allow_if", "'{}' in pastStatuses".format(self.status.reference))

        return e1 

class InPastTransitionsRule(Rule):
    def __init__(self, transition):
        self.transition = transition 

    def toXML(self):
        e1 = XMLElement("rule")
        e1.set("allow_if", "'{}' in pastTransitions".format(self.transition.reference))

        return e1 

def loadWorkflowFromXML(filePath):
    tree = parse(filePath)
    root = tree.getroot()

    if root.tag != "workflow":
        raise ValueError("The XML document provided is not a Workflow XML document.")

    workflow = Workflow()

    workflow.reference = tree.xpath("/workflow")[0].get("reference")
    workflow.name = tree.xpath("/workflow/name")[0].text 

    if tree.xpath("/workflow/description"):
        workflow.description = tree.xpath("/workflow/description")[0].text 

    statusElements = tree.xpath("/workflow/statuses/status")
    transitionElements = tree.xpath("/workflow/transitions/transition")

    for e1 in statusElements:
        status = Status()

        status.reference = e1.get("reference")
        status.category = e1.get("category")
        status.type = "automated_processing" if e1.get("type") == "automated_processing" else ""
        status.name = e1.xpath("./name")[0].text 

        if e1.xpath("./description"):
            status.description = e1.xpath("./description")[0].text 

        workflow.statuses.append(status)

    workflow.initialStatus = workflow.getStatusByReference(tree.xpath("/workflow/statuses")[0].get("initial"))
    workflow.finalStatus = workflow.getStatusByReference(tree.xpath("/workflow/statuses")[0].get("final"))

    for e1 in transitionElements:
        transition = Transition()

        transition.reference = e1.get("reference")
        transition._from = workflow.getStatusByReference(e1.get("from"))
        transition._to = workflow.getStatusByReference(e1.get("to"))
        transition.type = e1.get("type")
        transition.commentRequired = True if e1.get("comment_required") == "true" else False 
        transition.autoAssignTo = e1.get("auto_assign_to")
        transition.name = e1.xpath("./name")[0].text 

        if e1.xpath("./button_text"):
            transition.buttonText = e1.xpath("./button_text")[0].text 

        if e1.xpath("./description"):
            transition.description = e1.xpath("./description")[0].text 

        ruleElements = e1.xpath("./rules/rule")

        for e2 in ruleElements:
            allowIf = e2.get("allow_if")

            m1 = re.match(r"role in \[((\s*'[A-Za-z0-9_\-]+'\s*)(,\s*'[A-Za-z0-9_\-]+'\s*)*)\]", allowIf)

            if m1:
                rule = RolesRule()
                roles = m1.group(1).split(",")
                roles = [role.strip("'") for role in roles]
                rule.roles = roles 

                transition.rules.append(rule)

            m2 = re.match(r"'([A-Za-z0-9_\-]+)' in pastStatuses", allowIf)

            if m2:
                rule = InPastStatusesRule()
                rule.status = workflow.getStatusByReference(m2.group(1))

                transition.rules.append(rule)

            m3 = re.match(r"'([A-Za-z0-9_\-]+)' in pastTransitions", allowIf)

            if m3:
                rule = InPastTransitionsRule()
                rule.transition = workflow.getTransitionByReference(m3.group(1))

                transition.rules.append(rule)

        workflow.transitions.append(transition)

    return workflow 






