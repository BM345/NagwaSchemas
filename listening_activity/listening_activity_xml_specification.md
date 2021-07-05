# Listening Activity XML Specification

This document gives the specification for Listening Activity XML.

## Table of Contents

- [The &lt;listening_activity&gt; element](#the-listening-activity-element)
- [The &lt;title&gt; element](#the-title-element)
- [The &lt;seo_description&gt; element](#the-seo-description-element)
- [The &lt;subject&gt; element](#the-subject-element)
- [The &lt;g_value&gt; element](#the-g-value-element)
- [The &lt;listening_material&gt; element](#the-listening-material-element)
- [The &lt;sections&gt; element](#the-sections-element)
- [The &lt;section&gt; element](#the-section-element)
- [The &lt;questions&gt; element](#the-questions-element)
- [The &lt;question&gt; element](#the-question-element)


<br /><br />

## The &lt;listening_activity&gt; element

The &lt;listening_activity&gt; element is the root element of a Listening Activity XML file.

### Attributes

| Name | Required | Allowed Values | Description |
|---|---|---|---|
| `id` | Required | a 12-digit entity id | The id of this listening activity. |
| `version` | Required | an integer | The version number of this content entity. |

### Possible Subelements

- &lt;title&gt;
- &lt;seo_description&gt;
- &lt;subject&gt;
- &lt;g_value&gt;
- &lt;listening_material&gt;
- &lt;sections&gt;

### Examples

Below is shown an example of the `<listening_activity>` element.

```xml
<listening_activity id="000000000000" version="1">
    <title></title>
    <seo_description></seo_description>
    <subject></subject>
    <g_value></g_value>
    <listening_material></listening_material>
    <sections></sections>
</listening_activity>
```



<br /><br />

## The &lt;title&gt; element

The &lt;title&gt; element contains the title of this listening activity.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<title>` element.

```xml
<title>Ecotourism in the Seychelles</title>
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
<seo_description>practise listening for gist, detail and specific information in the context of ecotourism.</seo_description>
```



<br /><br />

## The &lt;subject&gt; element

The &lt;subject&gt; element gives the subject of this listening activity.

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

The &lt;g_value&gt; element gives the g-value of this listening activity.

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

## The &lt;listening_material&gt; element

The &lt;listening_material&gt; element contains the audio that the student must listen to for this activity.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<listening_material>` element.

```xml
<listening_material>
    ...
</listening_material>
```



<br /><br />

## The &lt;sections&gt; element

The &lt;sections&gt; element contains the list of sections in this listening activity.

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

The &lt;section&gt; element describes a section of this listening activity. There are three types of section: listening for gist, listening for detail, and listening for specific information.

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

The &lt;questions&gt; element contains the list of questions in this section of the listening activity.

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

