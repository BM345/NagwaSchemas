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
| `for_content_entity` | Required | entity identifier | A combination of an entity type name and an entity id to uniquely identify the piece of content in the system that this history file pertains to, i.e. `explainer/000000000000` or `question/000000000000`. |

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



<br /><br />

## The &lt;state&gt; element

The `<state>` element contains information about the current state of the content entity. This makes it possible to look-up the current state of the entity without having to read and interpret the entire list of actions.

### Attributes

None

### Possible Subelements

- `<workflow>`
- `<workflow_status>`
- `<developers>`
- `<assignee>`
- `<priority>`
- `<labels>`
- `<watchers>`

### Examples

Below is shown an example of the `<state>` element.

```xml
<state>
    <workflow>...</workflow>
    <workflow_status>...</workflow_status>
    <developers>
        ...
    </developers>
    <assignee>...</assignee>
    <priority>...</priority>
    <labels>
        ...
    </labels>
    <watchers>
        ...
    </watchers>
</state>
```



<br /><br />

## The &lt;workflow&gt; element

The `<workflow>` element contains the reference of the workflow that this content entity is currently in.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<workflow>` element.

```xml
<workflow>new_explainer</workflow>
```



<br /><br />

## The &lt;workflow_status&gt; element

The `<workflow_status>` element contains the reference of the status that this content entity currently has.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<workflow_status>` element.

```xml
<workflow_status>subject_review</workflow_status>
```



<br /><br />

## The &lt;developers&gt; element

The `<developers>` element contains the list of all of the developers who have worked on a content entity. This is needed for auto-assignment of content entities.

### Attributes

None

### Possible Subelements

- `<developer>`

### Examples

Below is shown an example of the `<developers>` element.

```xml
<developers>
    <developer role="content_writer">example.user.1@nagwa.com</developer>
    <developer role="course_reviewer">example.user.2@nagwa.com</developer>
    <developer role="subject_reviewer">example.user.3@nagwa.com</developer>
</developers>
```



<br /><br />

## The &lt;developer&gt; element

A `<developer>` element records that a certain developer in a certain role has worked on a content entity. The text of a `<developer>` element should be the email address of the user.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `role` | Required | a user role | The role that the user acted in when they worked on this item. |

### Possible Subelements

None

### Examples

Below is shown an example of a `<developer>` element.

```xml
<developer role="content_writer">example.user.1@nagwa.com</developer>
```
