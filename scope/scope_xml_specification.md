# Scope XML Specification

This document gives the specification for Scope XML.

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

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `id` | Required |  |  |
| `derivative_of` | Optional |  |  |
| `derivative_type` | Optional |  |  |
| `version` | Required |  |  |

### Possible Subelements

- &lt;language&gt;
- &lt;dialects&gt;
- &lt;objectives&gt;
- &lt;prerequisites&gt;
- &lt;exclusions&gt;

### Examples

Below is shown an example of the `<scope>` element.

```xml
<scope id="..." derivative_of="..." derivative_type="..." version="...">
    <language></language>
    <dialects></dialects>
    <objectives></objectives>
    <prerequisites></prerequisites>
    <exclusions></exclusions>
</scope>
```



<br /><br />

## The &lt;language&gt; element

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `code` | Required |  |  |
| `name` | Optional |  |  |
| `name_in_english` | Optional |  |  |

### Possible Subelements

None

### Examples

Below is shown an example of the `<language>` element.

```xml
<language code="..." name="..." name_in_english="...">
</language>
```



<br /><br />

## The &lt;dialects&gt; element

### Attributes

None

### Possible Subelements

- &lt;dialect&gt;

### Examples

Below is shown an example of the `<dialects>` element.

```xml
<dialects>
    <dialect></dialect>
</dialects>
```



<br /><br />

## The &lt;dialect&gt; element

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `code` | Required |  |  |
| `name` | Optional |  |  |
| `name_in_english` | Optional |  |  |

### Possible Subelements

None

### Examples

Below is shown an example of the `<dialect>` element.

```xml
<dialect code="..." name="..." name_in_english="...">
</dialect>
```



<br /><br />

## The &lt;objectives&gt; element

### Attributes

None

### Possible Subelements

- &lt;skill&gt;

### Examples

Below is shown an example of the `<objectives>` element.

```xml
<objectives>
    <skill></skill>
</objectives>
```



<br /><br />

## The &lt;prerequisites&gt; element

### Attributes

None

### Possible Subelements

- &lt;item&gt;

### Examples

Below is shown an example of the `<prerequisites>` element.

```xml
<prerequisites>
    <item></item>
</prerequisites>
```



<br /><br />

## The &lt;exclusions&gt; element

### Attributes

None

### Possible Subelements

- &lt;item&gt;

### Examples

Below is shown an example of the `<exclusions>` element.

```xml
<exclusions>
    <item></item>
</exclusions>
```



<br /><br />

## The &lt;skill&gt; element

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<skill>` element.

```xml
<skill>
</skill>
```



<br /><br />

## The &lt;item&gt; element

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<item>` element.

```xml
<item>
</item>
```

