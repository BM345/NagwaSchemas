# History XML Specification

## Table of Contents

- [The &lt;history&gt; element](#the-history-element)
- []()
- []()
- []()
- []()
- []()
- []()
- []()



<br /><br />

## The &lt;history&gt; element

The `<history>` element is the root element of a History XML file.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `for_content_entity` | Required | entity identifier | A combination of an entity type name and an entity id to uniquely identify the piece of content in the system that this history file pertains to. |

### Possible Subelements

- `<state>`
- `<actions>`

### Examples

Below is shown an example of the `<history>` element.

```xml
<history for_content_entity="explainer/000000000000">
    <state>
        ...
    </state>
    <actions>
        ...
    </actions>
</history>
```