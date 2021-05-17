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



<br /><br />

## The &lt;assignee&gt; element

The `<assignee>` element denotes who, if anyone, the content entity is currently assigned to. The text of this element should be the email address of the assignee.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<assignee>` element.

```xml
<assignee>example.user.3@nagwa.com</assignee>
```



<br /><br />

## The &lt;priority&gt; element

The `<priority>` element denotes what, if anything, the current priority of the content entity is.

The text of the `<priority>` element should be one of a set of values indicating the priority: `high`, `very_high`, `low`, `very_low`, or nothing if the priority has not been set. 

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<priority>` element.

```xml
<priority>high</priority>
```



<br /><br />

## The &lt;labels&gt; element

The `<labels>` element contains the list of labels that have been added to this content entity.

### Attributes

None

### Possible Subelements

- `<label>`

### Examples

Below is shown an example of a `<labels>` element.

```xml
<labels>
    <label>Images need updating</label>
    <label>Showcase</label>
    <label>Electromagnetism</label>
</labels>
```



<br /><br />

## The &lt;label&gt; element

The `<label>` element denotes a label that has been added to the content entity. A label can be anything - they are used by content developers to mark and search through content entities.

### Attributes

None

### Possible Subelements

None 

### Examples

Below is shown an example of a `<label>` element.

```xml
<label>Showcase</label>
```



<br /><br />

## The &lt;watchers&gt; element

The `<watchers>` element contains the list of people who are watching this content entity. When a content entity is updated in certain ways, everyone who is watching the content entity should be notified.

### Attributes

None

### Possible Subelements

- `<watcher>`

### Examples

Below is shown an example of a `<watchers>` element.

```xml
<watchers>
    <watcher>example.user.1@nagwa.com</watcher>
    <watcher>example.user.2@nagwa.com</watcher>
    <watcher>example.user.3@nagwa.com</watcher>
</watchers>
```



<br /><br />

## The &lt;watcher&gt; element

A `<watcher>` element denotes a user who is 'watching' a certain content entity. This means that when the content entity is updated in certain ways, they will be notified. The text of this element should be the email address of the user.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<watcher>` element.

```xml
<watcher>example.user.1@nagwa.com</watcher>
```
