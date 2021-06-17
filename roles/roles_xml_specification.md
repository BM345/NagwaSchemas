# Roles XML Specification

This document gives the specification for Roles XML.

A full example Roles XML document can be viewed [here](examples/cds.roles.xml).

## Table of Contents

- [The &lt;roles&gt; element](#the-roles-element)
- [The &lt;role&gt; element](#the-role-element)
- [The &lt;name&gt; element](#the-name-element)
- [The &lt;description&gt; element](#the-description-element)



<br /><br />

## The &lt;roles&gt; element

The `<roles>` element is the root element of a Roles XML file. It contains the set of possible roles that users of a system can have.

### Attributes

None

### Possible Subelements

- `<role>`

### Examples

Below is shown an example of the `<roles>` element.

```xml
<roles>
    <role reference="...">
        <name>...</name>
        <description>...</description>
    </role>
    <role reference="...">
        <name>...</name>
        <description>...</description>
    </role>
    <role reference="...">
        <name>...</name>
        <description>...</description>
    </role>
</roles>
```



<br /><br />

## The &lt;role&gt; element

A `<role>` element defines a role that users of a system can have. Each role has a unique reference, which is used to refer to the role in other XML files.

`<role>` elements can have `<name>` and `<description>` subelements. The `<name>` subelement is required, and the `<description>` subelement is optional. However, it is a very good idea to have a description for each role, as this clarifies to software developers what permissions a role will likely need, and to content developers what they will need to do if they have a given role for a given workflow.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `reference` | Required | any | A string that is used by the system to identify this role. This must be unique. |

### Possible Subelements

- `<name>`
- `<description>`

### Examples

Below is shown an example of a `<role>` element.

```xml
<role reference="...">
    <name>...</name>
    <description>...</description>
</role>
```



<br /><br />

## The &lt;name&gt; element

A `<name>` element gives the name of a role. All `<role>` elements must have a `<name>` subelement.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<name>` element.

```xml
<name>Copyeditor</name>
```



<br /><br />

## The &lt;description&gt; element

A `<description>` element gives a description of a role. `<description>` elements are optional, but highly advisable. They can make it clear to software developers why a role exists, and to content developers what they must do if they have a given role for a given workflow.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<description>` element.

```xml
<description>A copyeditor is someone who checks a piece of content for correct use of non-subject-specific language. This includes checking: that there are no mistakes of spelling, punctuation, or grammar, that the wording chosen is correct for the specified dialect, and that the piece of content follows the conventions of the chosen style guide.</description>
```