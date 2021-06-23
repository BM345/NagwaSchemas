# Release 1.1 - Release Notes

## Summary of New Features and Changes

This release includes:

- model code (in Python) for reading and writing History XML (much like the code in Release 1.0 for reading and writing Workflow XML)
- XSD schemas for both Workflow XML and History XML
- an example Roles XML file
- a specification for Roles XML
- an XSD schema for Roles XML
- model code (in Python) for reading and writing Roles XML
- example Scope XML files
- a specification for Scope XML
- two new attributes on `<workflow>` elements in Workflow XML - `type` and `limit_to_entity_types`
- the attribute `for_content_entity` on the `<history>` element in History XML has been renamed to `for_entity`, for consistency with other attribute names

XSD files now exist for Workflow XML, History XML, and Roles XML. These are ready to be used. Bear in mind that the specifications for these XML formats may change slightly over time, and hence the XSD files will change too.

An XSD file does exist for Scope XML; however, it is incomplete. At the moment it has no support for sublists, and formatting such as bold and italic. These features are all part of the semantic tags feature. The semantic tags require a lot of development, because they will also be used by other content entities; hence, they will be included in a future release. At the moment, only the example Scope XML files and the specification should be used as a guide for how Scope XML files will be structured.

All of the XSD files can be found in the folder `generated_schema_files`.

All XSD files in this repository are generated from `.schema` files using a Python module that has been specially developed for this project, called Schemata (`schemata.py`). This code parses the custom format used in the `.schema` files, and produces the corresponding XSD file.

There are several reasons for doing this. Firstly, the XSD format is extremely verbose, taking up a lot of characters to do simple things. This makes it very annoying to edit XSD files manually. XSD is also not very human-readable - it's very difficult to figure out what an XSD file is doing if it hasn't been structured very well.

The Schemata syntax and code can also be used to export to multiple more standard schema syntaxes (such as Schematron). It can also automatically generate a markdown specification document outline, leaving only a few details to be filled in manually.

The Schemata code in this release, while feature-rich, is not yet complete. The Schemata syntax may be updated in future releases - perhaps drastically - and the Schemata Python code will be optimised and expanded.