# Flashcard Set XML Specification

This document gives the specification for Flashcard Set XML.

## Table of Contents

- [The &lt;flashcard_set&gt; element](#the-flashcard-set-element)
- [The &lt;subject&gt; element](#the-subject-element)
- [The &lt;g_value&gt; element](#the-g-value-element)
- [The &lt;cards&gt; element](#the-cards-element)
- [The &lt;card&gt; element](#the-card-element)
- [The &lt;side&gt; element](#the-side-element)


<br /><br />

## The &lt;flashcard_set&gt; element

The &lt;flashcard_set&gt; element is the root element of a Flashcard Set XML file.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `id` | Required | a 12-digit entity id |  |
| `version` | Required | an integer |  |

### Possible Subelements

- &lt;subject&gt;
- &lt;g_value&gt;
- &lt;cards&gt;

### Examples

Below is shown an example of the `<flashcard_set>` element.

```xml
<flashcard_set id="..." version="...">
    <subject></subject>
    <g_value></g_value>
    <cards></cards>
</flashcard_set>
```



<br /><br />

## The &lt;subject&gt; element

The &lt;subject&gt; element gives the subject of this flashcard set.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<subject>` element.

```xml
<subject>
</subject>
```



<br /><br />

## The &lt;g_value&gt; element

The &lt;g_value&gt; element gives the g-value of this flashcard set.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<g_value>` element.

```xml
<g_value>
</g_value>
```



<br /><br />

## The &lt;cards&gt; element



### Attributes

None

### Possible Subelements

- &lt;card&gt;

### Examples

Below is shown an example of the `<cards>` element.

```xml
<cards>
    <card></card>
</cards>
```



<br /><br />

## The &lt;card&gt; element



### Attributes

None

### Possible Subelements

- &lt;side&gt;

### Examples

Below is shown an example of the `<card>` element.

```xml
<card>
    <side></side>
</card>
```



<br /><br />

## The &lt;side&gt; element



### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<side>` element.

```xml
<side>
</side>
```

