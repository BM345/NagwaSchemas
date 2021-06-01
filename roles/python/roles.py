from lxml.etree import ElementTree as XMLElementTree, Element as XMLElement, SubElement as XMLSubelement, indent, parse
import re


def makeReference(name):
    name = name.strip()
    name = name.lower()
    name = name.replace(" ", "_")

    return name


class RoleSet(object):
    def __init__(self):
        self.roles = []

    def getRoleByReference(self, reference):
        return [role for role in self.roles if role.reference == reference][0]

    def addRole(self, name, description=""):
        role = Role()

        role.name = name
        role.description = description

        self.roles.append(role)

    def setAllReferences(self):
        for role in self.roles:
            role.reference = makeReference(role.name)

    def toXML(self):
        e1 = XMLElement("roles")

        for role in self.roles:
            e1.append(role.toXML())

        return e1

    def save(self, filePath, setAllReferences=True):
        if setAllReferences:
            self.setAllReferences()

        tree = XMLElementTree(self.toXML())
        indent(tree, space="    ")
        tree.write(filePath, xml_declaration=True, encoding="utf-8", pretty_print=True)

    @staticmethod
    def load(filePath):
        return loadRolesFromXML(filePath)


class Role(object):
    def __init__(self):
        self.reference = ""
        self.name = ""
        self.description = ""

    def toXML(self):
        e1 = XMLElement("role")
        e1.set("reference", self.reference)

        e2 = XMLElement("name")
        e2.text = self.name
        e1.append(e2)

        e3 = XMLElement("description")
        e3.text = self.description
        e1.append(e3)

        return e1


def loadRolesFromXML(filePath):
    tree = parse(filePath)
    root = tree.getroot()

    if root.tag != "roles":
        raise ValueError("The XML document provided is not a Roles XML document.")

    roleSet = RoleSet()

    rolesElements = tree.xpath("/roles/role")

    for e1 in rolesElements:
        role = Role()

        role.reference = e1.get("reference")
        role.name = e1.xpath("./name")[0].text

        if e1.xpath("./description"):
            role.description = e1.xpath("./description")[0].text

        roleSet.roles.append(role)

    return roleSet
