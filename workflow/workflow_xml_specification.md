# Workflow XML Specification

## Table of Contents

- [The &lt;workflow&gt; element](#the-workflow-element)
- [The &lt;statuses&gt; element](#the-statuses-element)
- [The &lt;status&gt; element](#the-status-element)
- [The &lt;name&gt; element](#the-name-element)
- [The &lt;description&gt; element](#the-description-element)
- [The &lt;transitions&gt; element](#the-transitions-element)
- [The &lt;transition&gt; element](#the-transition-element)
- [The &lt;button_text&gt; element](#the-button_text-element)
- [The &lt;rules&gt; element](#the-rules-element)
- [The &lt;rule&gt; element](#the-rule-element)



<br /><br />

## The &lt;workflow&gt; element

The `<workflow>` element is the root element of a Workflow XML file.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `reference` | Required | any | A string that's used by the system to identify this workflow. |

### Possible Subelements

- `<name>`
- `<description>`
- `<statuses>`
- `<transitions>`

### Examples

Below is shown an example of the `<workflow>` element.

```xml
<workflow reference="workflow1">
    <name>...</name>
    <description>...</description>
    <statuses>
        ...
    </statuses>
    <transitions>
        ...
    </transitions>
</workflow>
```



<br /><br />

## The &lt;statuses&gt; element

The `<statuses>` element contains the set of statuses that exist in this workflow. It also defines the initial and final statuses for the workflow.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `initial` | Required | any | The reference of the status that marks the entry point of the workflow. Content entities should be set to this status by the system when they first go into the workflow. |
| `final` | Required | any | The reference of the status that marks the exit point of the workflow. Content entities with this status should be taken out of the workflow by the system. |

### Possible Subelements

- `<status>`

### Examples

Below is shown an example of the `<statuses>` element.

```xml
<statuses initial="status1" final="status10">
    <status>
        ...
    </status>
    <status>
        ...
    </status>
    <status>
        ...
    </status>    
</statuses>
```


<br /><br />

## The &lt;status&gt; element

A `<status>` element defines a possible status within a workflow.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `reference` | Required | any | A string that uniquely identifies this status within this workflow. |
| `category` | | any | A string that identifies what category or group of statuses this status is part of. This is used to automatic colour-coding of similar statuses. |
| `type` | | `automated_processing` | If a `<status>` element has `type="automated_processing"`, then content items with this status must be processed by a script, rather than by a user. |

### Possible Subelements

- `<name>`
- `<description>`

### Examples

Below is shown an example of a `<status>` element.

```xml
<status reference="status1" category="copyediting">
    <name>...</name>
    <description>...</description>
</status>
```


<br /><br />

## The &lt;name&gt; element

A `<name>` element defines the name of a workflow, status, or transition. It can be a direct subelement of a `<workflow>`, `<status>`, or `<transition>` element.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<name>` element.

```xml
<name>New Explainer Workflow</name>
```


<br /><br />

## The &lt;description&gt; element

A `<description>` element defines the description of a workflow, status, or transition. It can be a direct subelement of a `<workflow>`, `<status>`, or `<transition>` element. It is always optional, but it is a good idea to include it, as it can clarify to users what must be done with a content item that has a given status.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<description>` element.

```xml
<description>This workflow is used for creating new explainers.</description>
```


<br /><br />

## The &lt;transitions&gt; element

The `<transitions>` element contains the set of transitions that exist in this workflow.

### Attributes

None

### Possible Subelements

- `<transition>`

### Examples

Below is shown an example of the `<transitions>` element.

```xml
<transitions>
    <transition>
        ...
    </transition>
    <transition>
        ...
    </transition>
    <transition>
        ...
    </transition>
</transitions>
```


<br /><br />

## The &lt;transition&gt; element

A `<transition>` element defines a possible transition within a workflow.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `reference` | Required | any | A string that uniquely identifies this transition within this workflow. |
| `from` | Required | any | The reference of one of the two statuses that this transition links. This is the status that content entities are coming _from_. |
| `to` | Required | any | The reference of one of the two statuses that this transition links. This is the status that content entities are coming _to_. |
| `type` | | one of: `submit`, `approve`, `reject`, `pass`, `fail`, `error` | This attribute gives information on what _kind_ of transition this is. This affects both how buttons on the user interface are coloured, and how automated processes interact with the workflow. |
| `comment_required` | | boolean | Denotes whether or not the user must add a comment to this content entity before executing this transition. For transitions that represent rejections, generally a comment must be added. |
| `auto_assign_to` | | predicate | Denotes who the content entity should be assigned to once it undergoes this transition. If this attribute is omitted, the content entity will not be automatically assigned to anyone. |

### Possible Subelements

- `<name>`
- `<button_text>`
- `<description>`
- `<rules>`

### Examples

Below is shown an example of a `<transition>` element.

```xml
<transition reference="transition1" from="status1" to="status2" type="..." comment_required="..." auto_assign_to="...">
    <name>...</name>
    <button_text>...</button_text>
    <description>...</description>
    <rules>
        ...
    </rules>
</transition>
```


<br /><br />

## The &lt;button_text&gt; element

The `<button_text>` element can be a direct subelement of a `<transition>` element. It defines the text that should appear on the button that activates this transition in the front-end.

This is useful because generally the name of a transition will be something longer, such as 'Submit to Course Review', so that the transition can be easily identified when the Workflow XML is being edited (either directly or via a graphical interface). But generally we want to show something shorter and simpler on the actual button that the user presses to activate the transition, such as 'Submit'.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<button_text>` element.

```xml
<button_text>Submit</button_text>
```


<br /><br />

## The &lt;rules&gt; element

The `<rules>` element can be a direct subelement of a `<transition>` element. It contains the set of rules that apply to the transition.

The rules within a `<rules>` element combine with a logical AND. This means that all conditions specified by the rules must be met in order for a transition to be allowed.

If there are no rules associated with a transition, then the transition is always allowed.

### Attributes

None

### Possible Subelements

- `<rule>`

### Examples

Below is shown an example of a `<rules>` element.

```xml
<rules>
    <rule />
    <rule />
    <rule />
</rules>
```


<br /><br />

## The &lt;rule&gt; element

A `<rule>` element defines a rule that applies to a transition.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `allow_if` | Required | predicate | A predicate that describes a condition that must be met for the transition to be allowed. See below for the syntax of this predicate. |

### Possible Subelements

None

### Predicate Syntax

The predicate syntax closely follows the syntax of Python, defining lists in the same way, and using keywords such as `in`.

Parsing Python syntax is complicated for a general programming language. However, because there are, to begin with at least, relatively few distinct rules that we want to make possible in our workflows, it will be easy to parse the predicates using Regular Expressions.

There are, to begin with, 3 distinct types of rule that we want to make possible. The first is one that places a limitation on the role that a user must have in order to activate a transition. An example of this rule is shown below.

```xml
<rule allow_if="role in ['content_writer']" />
```

What this rule says is 'Allow this transition if the **role** of the current user is **in** the list **['content_writer']**'.

The list could have multiple roles in it, as shown below.

```xml
<rule allow_if="role in ['content_writer', 'course_designer', 'subject_reviewer']" />
```

In this case, if the current user has any of the roles given in the list, then the transition would be allowed (assuming all other conditions are also met).

The predicate could also be negated, as shown below.

```xml
<rule allow_if="role not ['content_writer']" />
```

This would allow anyone who **does not** have the role of `content_writer` to activate the transition.

The second type of rule is one that allows or disallows a transition based on whether the content entity has had a given status before. An example of this rule is shown below.

```xml
<rule allow_if="'course_review' not in pastStatuses" />
```

What this rule says is 'Allow this transition if the status with the reference **'course_review'** is **not in** the list of **past statuses**'.

The third type of rule is one that allows or disallows a transition based on whether the content entity has undergone a given transition before. An example of this is shown below.

```xml
<rule allow_if="'drafting_to_course_review' not in pastTransitions" />
```

What this rule says is 'Allow this transition if the transition with the reference **'drafting_to_course_review'** is **not in** the list of **past transitions**.

It should be possible to parse these three types of rule using RegEx.

### Examples

Below is shown an example of a `<rule>` element.

```xml
<rule allow_if="role in ['content_writer']" />
```