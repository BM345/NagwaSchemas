# History XML Specification

This document gives the specification for History XML.

A full example History XML document can be viewed [here](examples/000000000000.history.xml).

## Table of Contents

- [Overview](#overview)
- [The &lt;history&gt; element](#the-history-element)
- [The &lt;state&gt; element](#the-state-element)
- [The &lt;workflow&gt; element](#the-workflow-element)
- [The &lt;workflow_status&gt; element](#the-workflow_status-element)
- [The &lt;developers&gt; element](#the-developers-element)
- [The &lt;developer&gt; element](#the-developer-element)
- [The &lt;assignee&gt; element](#the-assignee-element)
- [The &lt;priority&gt; element](#the-priority-element)
- [The &lt;labels&gt; element](#the-labels-element)
- [The &lt;label&gt; element](#the-label-element)
- [The &lt;watchers&gt; element](#the-watchers-element)
- [The &lt;watcher&gt; element](#the-watcher-element)
- [The &lt;versions&gt; element](#the-versions-element)
- [The &lt;version&gt; element](#the-version-element)
- [The &lt;actions&gt; element](#the-actions-element)
- [The &lt;action&gt; element](#the-action-element)



<br /><br />

## Overview

A History XML file consists of two parts: a state, and a list of actions.

The list of actions provides a full history of the content entity. What workflows the entity has been in, who has worked on it, what comments have been added to it, and more, can all be traced by looking through the list of actions.

The state provides data for the current state of the content item. It exists to provide an easy way of looking-up the current state - i.e., you don't have to process the entire list of actions to work out the current state - you can just look in the 'cached' values in the state. This also makes the XML very human-readable.

As actions are taken on the content entity, they should be added to the list of actions, and the state should be updated accordingly.



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
- `<versions>`

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
    <versions>
        ...
    </versions>
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
    <developer workflow="new_explainer" role="content_writer">example.user.1@nagwa.com</developer>
    <developer workflow="new_explainer" role="course_reviewer">example.user.2@nagwa.com</developer>
    <developer workflow="new_explainer" role="subject_reviewer">example.user.3@nagwa.com</developer>
</developers>
```



<br /><br />

## The &lt;developer&gt; element

A `<developer>` element records that a certain developer in a certain role has worked on a content entity. The text of a `<developer>` element should be the email address of the user.

A new `<developer>` element should be added to the `<developers>` tag every time a content entity is assigned to a new user, as long as that user in that role hasn't been added before for that workflow (i.e., there must be no duplicates in the list).

`<developer>` elements should never be removed from the `<developers>` element.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `workflow` | Required | a reference | The reference to the workflow that this developer worked on this content entity in with the given role. This is needed because, for example, different copyeditors may work on an explainer when it is in an explainer update workflow to when it is in the new explainer workflow. This attribute is needed to be able to work out which copyeditor to auto-assign it to. |
| `role` | Required | a user role | The role that the user acted in when they worked on this item. |

### Possible Subelements

None

### Examples

Below is shown an example of a `<developer>` element.

```xml
<developer workflow="new_explainer" role="content_writer">example.user.1@nagwa.com</developer>
```



<br /><br />

## The &lt;assignee&gt; element

The `<assignee>` element denotes who, if anyone, the content entity is currently assigned to. The text of this element should be the email address of the assignee.

When a content entity is taken out of a workflow, it should be unassigned from anyone.

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

When a content entity is taken out of a workflow (because it has reached the final status of the workflow), its priority should be set back to nothing (because if the entity goes into another workflow later, it may not need the same priority).

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

The list of labels should not be changed in any way upon a change of workflow or workflow status.

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

The list of watchers should not be changed in any way upon a change in workflow or workflow status.

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



<br /><br />

## The &lt;versions&gt; element

The `<versions>` element contains the list of all of the different versions of the content item.

### Attributes

None

### Possible Subelements

- `<version>`

### Examples

Below is shown an example of the `<versions>` element.

```xml
<versions>
    <version file_name="000000000000.1.xml">1</version>
    <version file_name="000000000000.2.xml">2</version>
    <version file_name="000000000000.3.xml">3</version>
</versions>
```



<br /><br />

## The &lt;version&gt; element

A `<version>` element records that a particular version of the content entity exists.

The text of this element should just be the reference of the version (which is usually just a number).

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `file_name` | Required | file name | The name of the file that contains this version of the content entity. |

### Possible Subelements

None

### Examples

Below is shown an example of a `<version>` element.

```xml
<version file_name="000000000000.1.xml">1</version>
```



<br /><br />

## The &lt;actions&gt; element

The `<actions>` element contains the list of actions that have been taken on this content entity. The list of actions should provide a complete picture of the history of this content entity.

### Attributes

None

### Possible Subelements

- `<action>`

### Examples

Below is shown an example of the `<actions>` element.

```xml
<actions>
    <action taken_at="..." taken_by="..." type="...">
        ...
    </action>
    <action taken_at="..." taken_by="..." type="...">
        ...
    </action>
    <action taken_at="..." taken_by="..." type="...">
        ...
    </action>
</actions>
```



<br /><br />

## The &lt;action&gt; element

An `<action>` element is a record of an action taken on a content entity. An `<action>` element records when an action was taken, who it was taken by, what kind of action it was, and any other necessary data about the action. Actions cover all types of interaction with the content entity: adding a comment or a label is an action, as is changing the status, priority, or assignee.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `taken_at` | Required | timestamp | The date and time of when this action was taken. |
| `taken_by` | Required | email address / `system` | The email address of the user who took this action. Some actions are not taken by a user, but by the system - in such cases, this attribute should just have the value `system`. |
| `type` | Required | one of a set of values; see below | The type of action this was - i.e., whether it was a status change, or a new comment, et cetera. |

### Type Values

The table below gives the set of possible values for the `type` attribute, and what they mean. This list will likely be expanded in future versions of this specification, to allow for an even more detailed history of a content entity.

The 'Notify Watchers' column denotes whether a notification should be sent to each of the watchers when an action of that type is added to the history file.

Note that comments can never be edited or deleted. (In the case where a comment must be deleted because it accidentally includes some GDPR-restricted data, then this must be done manually by developers.)

| Value | Notify Watchers | Meaning |
|---|---|---|
| `created_entity` | No | An action of this type should be added when the entity is first created. |
| `created_new_version` | No | An action of this type should be added when a new version of the content entity is created. |
| `changed_workflow` | Yes | An action of this type should be added when the entity is put into a new workflow or taken out of a workflow. |
| `changed_workflow_status` | Yes | An action of this type should be added when the status of the entity is changed (except when it is changed to none). |
| `changed_assignee` | Yes | An action of this type should be added when the assignee for an entity is changed (except when it is changed to none). |
| `changed_priority` | Yes | An action of this type should be added when the priority for an entity is changed (except when it is changed to none). |
| `added_comment` | Yes | An action of this type should be added when a user adds a comment to the entity. |
| `added_label` | Yes | An action of this type should be added when a user adds a label to the entity. |
| `removed_label` | Yes | An action of this type should be added when a user removes a label from the entity. |
| `added_watcher` | No | An action of this type should be added when a user adds a watcher (either themselves or someone else) to the entity. |
| `removed_watcher` | No | An action of this type should be added when a user removes a watcher (either themselves or someone else) to the entity. |

### Possible Subelements

The possible subelements for an `<action>` element are different depending on the value of the `type` attribute. The table below gives the possible subelements for each different `type` value.

| Value | Possible Subelements |
|---|---|
| `created_entity` | None |
| `created_new_version` | A `<version>` element, containing the reference of the new version (which is usually just a number), and a `<file_name>` element, containing the file name. |
| `changed_workflow` | A `<new_workflow>` element, the text of which is the reference for the workflow that this entity has been put into. |
| `changed_workflow_status` | A `<new_workflow_status>` element, the text of which is the reference for the workflow status that this entity has been given. |
| `changed_assignee` | A `<new_assignee>` element, the text of which is the email address of the user that this entity has been assigned to. |
| `changed_priority` | A `<new_priority>` element, the text of which is the priority that this entity has been given. |
| `added_comment` | A `<comment_reference>` element, the text of which is a unique reference for this comment. This can be anything, as long as it is unique for this content entity. Also a `<comment_text>` element for the text of the comment. |
| `added_label` | A `<label>` element, the text of which is the text of the label. |
| `removed_label` | A `<label>` element, the text of which is the text of the label. |
| `added_watcher` | A `<watcher>` element, the text of which is the email address of the watcher. |
| `removed_watcher` | A `<watcher>` element, the text of which is the email address of the watcher. |

### Examples

Below are shown some examples of the `<action>` element.

```xml
<action taken_at="2021-04-26T10:00:00" taken_by="system" type="changed_workflow">
    <new_workflow>new_explainer</new_workflow>
</action>
```

```xml
<action taken_at="2021-04-26T10:30:00" taken_by="example.user.1@nagwa.com" type="added_comment">
    <comment_reference>c1</comment_reference>
    <comment_text>This is my comment.</comment_text>
</action>
```
