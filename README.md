# Nagwa Schemas

This repository gives the specifications and schemas for the various different XML formats that underpin Nagwa content.

## Schemas

The table below gives links to the various different resources available for the different XML formats described in this repository.

| XML Format | Example XML File | Specification | XSD File | Usage |
|---|---|---|---|---|
| Workflow XML | [Link](workflow/examples/new_explainer.workflow.xml) | [Link](workflow/workflow_xml_specification.md) | [Link](workflow/workflow.xsd) | Defining the workflows used in the development of Nagwa content. |
| History XML | [Link](history/examples/000000000000.history.xml) | [Link](history/history_xml_specification.md) | [Link](history/history.xsd) | Recording the history of work done and actions taken on content entities. |
| Roles XML | [Link](roles/examples/cds.roles.xml) | [Link](roles/roles_xml_specification.md) | [Link](roles/roles.xsd) | Defining the user roles that exist on a system. |
| Scope XML | [Link](scope/examples/189151468269.scope.xml) | [Link](scope/scope_xml_specification.md) | [Link](scope/scope.xsd) | Outlining the skills that are and are not included in a lesson. |


## Entity Types

The table below gives the references for the different types of entity that we have in Nagwa content. These references are used throughout the different XML formats defined in this repository.

| Type | Reference | Description | 
|---|---|---|
| Question | `question` | A question. | 
| Explainer | `explainer` | A piece of written content, similar to a textbook chapter, that teaches the student what they need to know for a lesson. |
| Question Video | `question_video` | A video taking the student through the solution to a question. |
| Lesson Video | `lesson_video` | A video that teaches the student what they need to know for a lesson. |
| Scope | `scope` | A document that defines what skills are and are not covered by a given lesson. |
| Lesson | `lesson` | An entity that connects together all of the other entities that are needed for a lesson. |
| Image | `image` | An image (of any format: PNG, JPEG, SVG, et cetera). |

## Commands

### Building the XSD files from the Schemata files

```bash
python generate.py generate_xsd_files
```

### Running the Schemata unit tests

```bash
python -m unittest discover
```

