# Question XML

This document gives the specification for the new question XML format (version 2.0), and describes the important changes that have been made from the previous question XML format.

## Table of Contents

+ [Question Part Types](#question-part-types)
+ [Examples of the New Format](#examples-of-the-new-format)
+ [Overview of Important Changes](#overview-of-important-changes)

## Question Part Types

The table below briefly describes the different question part types - including new question part types - that can exist in Nagwa content. New question part types are indicated by an asterisk (*).

| Abbreviation | Name | Description |
|---|---|---|
| MCQ | Multiple-Choice Question | A question where the student is given a set of answer options to choose from, one or more of which is correct. MCQs can also double-up as numerical-response or text-response questions, where the student types in a number or short piece of text as their answer, which is then compared to the correct answer. |
| FRQ | Free-Response Question | A question where the student may enter a long text answer that they have written. |
| CTSQ* | Complete-The-Sentence Question | A question where the student is given an incomplete sentence or sentences, and must find words or phrases that correctly complete them. Also known as Fill-In-The-Blanks Questions. |
| CTTQ* | Complete-The-Table Question | A question where the student is given an incomplete table, and must find the words, phrases, or numbers that correctly complete it. |
| CTEQ* | Complete-The-Equation Question | A question where the student is given an incomplete equation, and must find the numbers or terms that correctly complete it. |
| SQ* | Select Question | A question where the student is given a sentence or sentences, and must select certain words or phrases from them. |
| OQ* | Ordering Question | A question where the student is given a list of items, and must put them in the correct order. |
| MQ* | Matching Question | A question where the student is given two or more lists, and must match the items in the different lists. |
| DLQ* | Diagram-Labelling Question | A question where the student is presented with a diagram, and must label different parts of it, either being given the labels to use, and having to drag and drop them into place, or having to type out the correct labels. |
| CQ* | Classifying Question | A question where the student must place given items into different category boxes. |
| TFQ* | True-False Question | A question where the answer is either true or false. (No other answer options are permitted. If an option such as 'It is not possible to determine.' is desired, the question must be an MCQ instead.) |
| YNQ* | Yes-No Question | A question where the answer is either yes or no. (No other answer options are permitted. If an option such as 'It is not possible to determine.' is desired, the question must be an MCQ instead.) |

## Examples of the New Format

Below are listed links to examples of the new question XML format that are based on existing questions.

| Previous XML | New XML | Key Features |
|---|---|---|
| [578143060713](examples/578143060713_current.question.xml) | [578143060713](examples/578143060713_new.question.xml) | Multi-part; MCQs; single instance |
| [409158921650](examples/409158921650_current.question.xml) | [409158921650](examples/409158921650_new.question.xml) | Single-part; MCQ; multiple instances; different solution text required for different instances |
| [676140256919](examples/676140256919_current.question.xml) | [676140256919](examples/676140256919_new.question.xml) | Figures; different answer formats |
| [505183812139](examples/505183812139_current.question.xml) | [505183812139](examples/505183812139_new.question.xml) | New CTSQ type |
| [682162714504](examples/682162714504_current.question.xml) | [682162714504](examples/682162714504_new.question.xml) | FRQ |
| [818183672624](examples/818183672624_current.question.xml) | [818183672624](examples/818183672624_new.question.xml) | With tables |
| [625137396409](examples/625137396409_current.question.xml) | [625137396409](examples/625137396409_new.question.xml) | MRQ becoming MCQ | 

Below are listed links to examples of new question XML documents for new question part types.

| New XML | Key Features |
|---|---|
| [sq1](examples/sq1.question.xml) | SQ | 
| [oq1](examples/oq1.question.xml) | OQ | 
| [mq1](examples/mq1.question.xml) | MQ | 
| [tfq1](examples/tfq1.question.xml) | TFQ | 
| [ynq1](examples/ynq1.question.xml) | YNQ | 

## Overview of Important Changes

This section describes some of the bigger changes to the design of the question XML format, and, in some cases, the reasons for the change. Not all changes are described in this section - only the more significant ones.

### Question parts are moved into the &lt;parts&gt; tag

Previously, the different question parts in a question existed as `<mcq>`, `<mrq>`, `<frq>`, and `<statement>` elements which were direct subelements of the root `<question>` element.

In the new format, question parts are denoted by the new `<part>` tag, which has an attribute `type` for specifying the part type. The `<part>` elements in a question are grouped together under the new `<parts>` element, which is itself a direct subelement of the `<question>` root element.

This change improves the readability of the XML, and it may also make querying the XML easier (as a multi-part question is now just one where `//question/parts/part` > 1).

### &lt;developers&gt; and &lt;developer&gt; tags allow for a more comprehensive description of who has interacted with a question

Previously, the `<developer_name>` and `<developer_email>` tags were the only ones that denoted who had worked on a file, and they always denoted who had created the question.

In the new format, this has been made more general and extensible. There is now a `<developers>` element, which is a direct subelement of the root element, and which can contain any number of `<developer>` elements. Each `<developer>` element can have a `role` attribute, denoting how to developer has interacted with the question. The developer's name and email address are contained within `<name>` and `<email_address>` subelements.

This allows for any number of developers to be listed, if necessary. It also improves the readability of the XML.

### More date information can be stored

The new format introduces the `<upload_date>` tag and the `<last_modification_date>` tag. This makes it easier to track the progress of a question while it is being developed.

### Solutions can now be stored in the question XML

Now that we have started writing explainers, we have the written solutions for many questions. Since these are intrinsically linked to the questions, the best place to store them is in the question XML.

Each question part now has a `<solutions>` subelement. This can have any number of `<solution>` subelements, which contain the solution text for different instances of the question. (While most of the time the solution text will be the same for the different instances of the question, there are some cases where the exact wording needs to be slightly different. Hence, multiple `<solution>` elements can exist for each question part.)

### Introduction of &lt;s&gt; tags

The new format introduces `<s>` tags, which are used to identify sentences. This allows for determining more things about the question programmatically (for example, a question with more sentences in it might be considered a harder question - this can now be determined easily programmatically), and it improves the readability of the XML.

### &lt;m&gt; tags replace &lt;latex&gt; tags and dollar signs

In the question XML at the moment, sections of mathematical notation are indicated by both `<latex>` tags and dollar signs - for example, `<latex>$y = mx + c$</latex>`. It shouldn't be necessary to have both `<latex>` tags _and_ dollar signs, and considering that a lot of our questions contain several sections of mathematical notation, it's also excessive.

The new format simplifies this by introducing the `<m>` 'mathematical notation' tag. This makes the XML easier to read. A section of mathematical notation would be marked-up as something like `<m>y = mx + c</m>`.

### &lt;unit&gt; tags can now exist on their own

Previously, `<unit>` tags could only exist within `<quantity>` tags. However, there are many occasions where we want to express a unit only - not a quantity (such as in expressions like 'Give your answer in kilometres.').

In the new format, `<unit>` tags can exist on their own, as well as within `<quantity>` tags. The `type` attribute on the `<quantity>` tag has been replaced by the `form` attribute on the `<unit>` tag.

This simplifies the XML - removing unnecessary elements - and improves readability.



### FITBQs become their own question type

So far, FITBQs (fill-in-the-blanks questions) have been made using the MCQ format. This is very non-ideal. Since we will probably want students to be able to drag and drop terms into the blanks of an FITBQ question (it will require a new XML structure to describe how to do this for a given question), and since there are quite a few FITBQs in the content, it makes sense to make these a new question type.

### MRQs are now just a type of MCQ

MRQs (multiple-response questions) and MCQs (multiple-choice questions) become one and the same - both known as MCQs. This is because the only difference between them is that MCQs have one correct answer choice, and MRQs have more than one. MCQs are just the special case of an MRQ where n, the number of correct answer choices, equals 1.

MRQs can still be identified, because the number of `<choice>` elements with `is_correct_answer="true"` is greater than 1.