# Reading Activity XML Specification

This document gives the specification for Reading Activity XML.

## Table of Contents

- [The &lt;reading_activity&gt; element](#the-reading-activity-element)
- [The &lt;title&gt; element](#the-title-element)
- [The &lt;seo_description&gt; element](#the-seo-description-element)
- [The &lt;subject&gt; element](#the-subject-element)
- [The &lt;g_value&gt; element](#the-g-value-element)
- [The &lt;sections&gt; element](#the-sections-element)
- [The &lt;section&gt; element](#the-section-element)
- [The &lt;questions&gt; element](#the-questions-element)
- [The &lt;question&gt; element](#the-question-element)


<br /><br />

## The &lt;reading_activity&gt; element

The &lt;reading_activity&gt; element is the root element of a Reading Activity XML file.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `id` | Required | a 12-digit entity id |  |
| `version` | Required | an integer |  |

### Possible Subelements

- &lt;title&gt;
- &lt;seo_description&gt;
- &lt;subject&gt;
- &lt;g_value&gt;
- &lt;sections&gt;

### Examples

Below is shown an example of the `<reading_activity>` element.

```xml
<reading_activity id="..." version="...">
    <title></title>
    <seo_description></seo_description>
    <subject></subject>
    <g_value></g_value>
    <sections></sections>
</reading_activity>
```



<br /><br />

## The &lt;title&gt; element



### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<title>` element.

```xml
<title>
</title>
```



<br /><br />

## The &lt;seo_description&gt; element



### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<seo_description>` element.

```xml
<seo_description>
</seo_description>
```



<br /><br />

## The &lt;subject&gt; element



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

## The &lt;sections&gt; element



### Attributes

None

### Possible Subelements

- &lt;section&gt;

### Examples

Below is shown an example of the `<sections>` element.

```xml
<sections>
    <section></section>
</sections>
```



<br /><br />

## The &lt;section&gt; element



### Attributes

None

### Possible Subelements

- &lt;questions&gt;

### Examples

Below is shown an example of the `<section>` element.

```xml
<section>
    <questions></questions>
</section>
```



<br /><br />

## The &lt;questions&gt; element



### Attributes

None

### Possible Subelements

- &lt;question&gt;

### Examples

Below is shown an example of the `<questions>` element.

```xml
<questions>
    <question></question>
</questions>
```



<br /><br />

## The &lt;question&gt; element



### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `id` | Required | a 12-digit entity id |  |

### Possible Subelements

None

### Examples

Below is shown an example of the `<question>` element.

```xml
<question id="...">
</question>
```

