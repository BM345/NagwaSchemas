# Semantic Tags Specification

This document gives the specification for Semantic Tags.

## Table of Contents

- [The &lt;binomen&gt; element](#the-binomen-element)
- [The &lt;generic_name&gt; element](#the-generic-name-element)
- [The &lt;specific_name&gt; element](#the-specific-name-element)
- [The &lt;book_title&gt; element](#the-book-title-element)
- [The &lt;journal_name&gt; element](#the-journal-name-element)
- [The &lt;newspaper_name&gt; element](#the-newspaper-name-element)
- [The &lt;magazine_name&gt; element](#the-magazine-name-element)
- [The &lt;movie_title&gt; element](#the-movie-title-element)


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

## The &lt;book_title&gt; element

The book title element is used to identify titles of books - for example: J. R. R. Tolkien's *The Lord of the Rings* or George R. R. Martin's *A Game of Thrones*.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<book_title>` element.

```xml
<book_title>
</book_title>
```



<br /><br />

## The &lt;journal_name&gt; element

The journal name element is used to identify names of academic journals - for example: *Physical Review* or *Applied Physics Letters*.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<journal_name>` element.

```xml
<journal_name>
</journal_name>
```



<br /><br />

## The &lt;newspaper_name&gt; element

The newspaper name element is used to identify names of newspapers - for example: *The Guardian* or *The Independent*.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<newspaper_name>` element.

```xml
<newspaper_name>
</newspaper_name>
```



<br /><br />

## The &lt;magazine_name&gt; element

The magazine name element is used to identify names of magazines - for example: *Time* or *Vanity Fair*.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<magazine_name>` element.

```xml
<magazine_name>
</magazine_name>
```



<br /><br />

## The &lt;movie_title&gt; element

The movie title element is used to identify titles of movies - for example: *Green Lantern* or *Airplane!*.

### Attributes

None

### Possible Subelements

None

### Examples

Below is shown an example of the `<movie_title>` element.

```xml
<movie_title>
</movie_title>
```

