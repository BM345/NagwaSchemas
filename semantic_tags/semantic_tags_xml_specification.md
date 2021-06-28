# Semantic Tags Specification

This document gives the specification for Semantic Tags.

## Table of Contents

- [The &lt;binomen&gt; element](#the-binomen-element)
- [The &lt;generic_name&gt; element](#the-generic-name-element)
- [The &lt;specific_name&gt; element](#the-specific-name-element)
- [The &lt;creative_work_title&gt; element](#the-creative-work-title-element)


<br /><br />

## The &lt;binomen&gt; element

The binomen element is used to identify binomina - binominal names used in biology - such as *Homo sapiens* or *Panthera leo*. Binomina consist of two names - a generic name and a specific name - the &lt;generic_name&gt; and &lt;specific_name&gt; elements can be used to identify these.

### Attributes

None

### Possible Subelements

- &lt;generic_name&gt;
- &lt;specific_name&gt;

### Examples

Below is shown an example of the `<binomen>` element.

```xml
<binomen>
    <generic_name></generic_name>
    <specific_name></specific_name>
</binomen>
```



<br /><br />

## The &lt;generic_name&gt; element

The generic name element is used to identify the generic name - the genus - within a binomen. For example, in the binomen *Homo sapiens*, *Homo* is the generic name - humans are part of the genus *Homo*.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<generic_name>` element.

```xml
<generic_name>
</generic_name>
```



<br /><br />

## The &lt;specific_name&gt; element

The specific name element is used to identify the specific name - the species - within a binomen. For example, in the binomen *Homo sapiens*, *sapiens* is the specific name.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<specific_name>` element.

```xml
<specific_name>
</specific_name>
```



<br /><br />

## The &lt;creative_work_title&gt; element

The creative work title element is used to identify titles of creative works, such as J. R. R. Tolkien's *The Lord of the Rings*. Titles of creative works are typically rendered in italics.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<creative_work_title>` element.

```xml
<creative_work_title>
</creative_work_title>
```

