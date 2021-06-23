# Scope XML Specification

This document gives the specification for Scope XML.

A full example Scope XML file can be viewed [here](examples/189151468269.scope.xml).

## Table of Contents

- [The &lt;scope&gt; element](#the-scope-element)
- [The &lt;language&gt; element](#the-language-element)
- [The &lt;dialects&gt; element](#the-dialects-element)
- [The &lt;dialect&gt; element](#the-dialect-element)
- [The &lt;objectives&gt; element](#the-objectives-element)
- [The &lt;prerequisites&gt; element](#the-prerequisites-element)
- [The &lt;exclusions&gt; element](#the-exclusions-element)
- [The &lt;skill&gt; element](#the-skill-element)
- [The &lt;item&gt; element](#the-item-element)


<br /><br />

## The &lt;scope&gt; element

The `<scope>` element is the root element of a Scope XML document.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `id` | Required | a 12-digit entity id | The id of this scope.  |
| `derivative_of` | Optional | a 12-digit entity id | If this scope has been translated or localised from another scope, this is the id of that scope.  |
| `derivative_type` | Optional | one of `translation`, `localization` | If this scope is a translation of another scope, then this should be set to `translation`. If this scope is a localisation of another scope, then this should be set to `localisation`. |
| `version` | Required | a integer | The version number of this scope. |

### Possible Subelements

- &lt;language&gt;
- &lt;dialects&gt;
- &lt;objectives&gt;
- &lt;prerequisites&gt;
- &lt;exclusions&gt;

### Examples

Below is shown an example of the `<scope>` element.

```xml
<scope id="000000000000" version="1">
    <language />
    <dialects>...</dialects>
    <objectives>...</objectives>
    <prerequisites>...</prerequisites>
    <exclusions>...</exclusions>
</scope>
```



<br /><br />

## The &lt;language&gt; element

The `<language>` element defines the language that this scope has been written in.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `code` | Required | an ISO 639-1 language code | The ISO 639-1 language code of this language. |
| `name` | Optional | string | The name of this language *in the language*. This attribute is optional, and exists simply to help with the human-readability of the XML. |
| `name_in_english` | Optional | string | The name of this language *in English*. This attribute is optional, and exists simply to help with the human-readability of the XML. |

### Possible Subelements

None

### Examples

Below is shown an example of the `<language>` element.

```xml
<language code="en" name_in_english="English" />
```



<br /><br />

## The &lt;dialects&gt; element

The `<dialects>` element contains the set of dialects that this scope has been written in. It's possible to write a piece of text in a language that is considered correct in multiple dialects, hence why this element can contain multiple `<dialect>` elements.

### Attributes

None

### Possible Subelements

- &lt;dialect&gt;

### Examples

Below is shown an example of the `<dialects>` element.

```xml
<dialects>
    <dialect />
</dialects>
```



<br /><br />

## The &lt;dialect&gt; element

A `<dialect>` element defines a dialect that this scope has been written in. It is possible for a piece of text to be valid in multiple dialects, thus there can be many `<dialect>` tags in a scope file.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `code` | Required | a dialect code | The code used to reference this dialect. |
| `name` | Optional | string | The name of this dialect *in the corresponding language*. This attribute is optional, and exists simply to help with the human-readability of the XML. |
| `name_in_english` | Optional | string | The name of this dialect *in English*. This attribute is optional, and exists simply to help with the human-readability of the XML. |

### Possible Subelements

None

### Examples

Below is shown an example of a `<dialect>` element.

```xml
<dialect code="en_GB" name_in_english="British English" />
```



<br /><br />

## The &lt;objectives&gt; element

The `<objectives>` element contains the list of skills that the student should have learned by the end of this lesson.

### Attributes

None

### Possible Subelements

- &lt;skill&gt;

### Examples

Below is shown an example of the `<objectives>` element.

```xml
<objectives>
    <skill>...</skill>
    <skill>...</skill>
    <skill>...</skill>
</objectives>
```



<br /><br />

## The &lt;prerequisites&gt; element

The `<prerequisites>` element contains the list of skills that the student should already have learned before starting this lesson.

### Attributes

None

### Possible Subelements

- &lt;item&gt;

### Examples

Below is shown an example of the `<prerequisites>` element.

```xml
<prerequisites>
    <item>...</item>
    <item>...</item>
    <item>...</item>
</prerequisites>
```



<br /><br />

## The &lt;exclusions&gt; element

The `<exclusions>` element contains the list of skills, topics, and concepts that are not covered by this lesson.

### Attributes

None

### Possible Subelements

- &lt;item&gt;

### Examples

Below is shown an example of the `<exclusions>` element.

```xml
<exclusions>
    <item>...</item>
    <item>...</item>
    <item>...</item>
</exclusions>
```



<br /><br />

## The &lt;skill&gt; element

A `<skill>` element defines a skill that is the objective of a lesson.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of a `<skill>` element.

```xml
<skill>recall that gravity acts between all objects that have mass</skill>
```



<br /><br />

## The &lt;item&gt; element

An `<item>` element defines a skill, topic, concept, or case that is either a prerequisite of the lesson or is excluded from it.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of an `<item>` element.

```xml
<item>centripetal force</item>
```

