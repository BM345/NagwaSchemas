from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, indent 

def makeReference(name):
    name = name.strip()
    name = name.lower()
    name = name.replace(" ", "_")

    return name 


class Workflow(object):
    def __init__(self, name, description = "", reference = ""):
        self.reference = reference
        self.name = name 
        self.description = description 
        self.statuses = []
        self.transitions = []

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
            tr = makeReference(transition._from.reference + "_to_" + transition._to.reference)
            n = 1

            while tr in trs:
                n += 1
                tr = "{}_{}".format(makeReference(transition._from.reference + "_to_" + transition._to.reference), n)

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


