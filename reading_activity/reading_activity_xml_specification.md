# Reading Activity XML Specification

This document gives the specification for Reading Activity XML.

## Table of Contents

- [The &lt;reading_activity&gt; element](#the-reading-activity-element)
- [The &lt;title&gt; element](#the-title-element)
- [The &lt;seo_description&gt; element](#the-seo-description-element)
- [The &lt;subject&gt; element](#the-subject-element)
- [The &lt;g_value&gt; element](#the-g-value-element)
- [The &lt;reading_material&gt; element](#the-reading-material-element)
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
| `id` | Required | a 12-digit entity id | The id of this reading activity. |
| `version` | Required | an integer | The version number of this entity. |

### Possible Subelements

- &lt;title&gt;
- &lt;seo_description&gt;
- &lt;subject&gt;
- &lt;g_value&gt;
- &lt;reading_material&gt;
- &lt;sections&gt;

### Examples

Below is shown an example of the `<reading_activity>` element.

```xml
<reading_activity id="..." version="...">
    <title></title>
    <seo_description></seo_description>
    <subject></subject>
    <g_value></g_value>
    <reading_material></reading_material>
    <sections></sections>
</reading_activity>
```



<br /><br />

## The &lt;title&gt; element

The &lt;title&gt; element contains the title of this reading activity.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<title>` element.

```xml
<title>My Holiday in Rome &amp; My Time in Manaus, Brazil</title>
```



<br /><br />

## The &lt;seo_description&gt; element

The &lt;seo_description&gt; element contains the SEO description of this reading activity.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<seo_description>` element.

```xml
<seo_description>practise reading for gist, detail and specific information in the context of going on holiday.</seo_description>
```



<br /><br />

## The &lt;subject&gt; element

The &lt;subject&gt; element gives the subject of this reading activity.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<subject>` element.

```xml
<subject>english</subject>
```



<br /><br />

## The &lt;g_value&gt; element

The &lt;g_value&gt; element gives the g-value of this reading activity.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<g_value>` element.

```xml
<g_value>9</g_value>
```



<br /><br />

## The &lt;reading_material&gt; element

The &lt;reading_material&gt; element contains the text that the student must read for this activity.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<reading_material>` element.

```xml
<reading_material>
    ...
</reading_material>
```



<br /><br />

## The &lt;sections&gt; element

The &lt;sections&gt; element contains the list of sections in this reading activity.

### Attributes

None

### Possible Subelements

- &lt;section&gt;

### Examples

Below is shown an example of the `<sections>` element.

```xml
<sections>
    <section></section>
    <section></section>
    <section></section>
</sections>
```



<br /><br />

## The &lt;section&gt; element

The &lt;section&gt; element describes a section of this reading activity. There are three types of section: reading for gist, reading for detail, and reading for specific information.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `type` | Required | one of: `gist`, `detail`, `specific_information` | The type of this section. |

### Possible Subelements

- &lt;questions&gt;

### Examples

Below is shown an example of the `<section>` element.

```xml
<section type="...">
    <questions></questions>
</section>
```



<br /><br />

## The &lt;questions&gt; element

The &lt;questions&gt; element contains the list of questions in this section of the reading activity.

### Attributes

None

### Possible Subelements

- &lt;question&gt;

### Examples

Below is shown an example of the `<questions>` element.

```xml
<questions>
    <question id="000000000000" />
    <question id="000000000000" />
    <question id="000000000000" />
</questions>
```



<br /><br />

## The &lt;question&gt; element

The &lt;question&gt; element gives a reference to a question that is part of this section.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `id` | Required | a 12-digit entity id | The id of the question to include. |

### Possible Subelements

None

### Examples

Below is shown an example of the `<question>` element.

```xml
<question id="000000000000" />
```

