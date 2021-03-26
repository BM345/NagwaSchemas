# Question XML

This document gives the specification for the new question XML format (version 2.0), and describes the important changes that have been made from the previous question XML format.

## Table of Contents

+ [Question Part Types](#question-part-types)
+ [Examples of the New Format](#examples-of-the-new-format)

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

Changes are still being made to the format - use these links just to get a sense of what the new format will be like.

| Current XML | New XML | Key Features |
|---|---|---|
| [578143060713](examples/578143060713_current.question.xml) | [578143060713](examples/578143060713_new.question.xml) | Multi-part question with MCQs; single instance |
| [409158921650](examples/409158921650_current.question.xml) | [409158921650](examples/409158921650_new.question.xml) | Single-part; multiple instances; different solution text required for different instances |
| [676140256919](examples/676140256919_current.question.xml) | [676140256919](examples/676140256919_new.question.xml) | Figures; different answer formats |
| [505183812139](examples/505183812139_current.question.xml) | [505183812139](examples/505183812139_new.question.xml) | New FITBQ type |
| [682162714504](examples/682162714504_current.question.xml) | [682162714504](examples/682162714504_new.question.xml) | FRQ |
| [818183672624](examples/818183672624_current.question.xml) | [818183672624](examples/818183672624_new.question.xml) | With tables |
| [625137396409](examples/625137396409_current.question.xml) | [625137396409](examples/625137396409_new.question.xml) | MRQ becoming MCQ | 

Below are listed links to examples of new question XML documents for new question types.

| New XML | Key Features |
|---|---|
| [ynq1](examples/ynq1.question.xml) | YNQ (yes-no question) | 
| [tfq1](examples/tfq1.question.xml) | TFQ (true-false question) | 
| [sq1](examples/sq1.question.xml) | SQ (select question) | 
| [mq1](examples/mq1.question.xml) | MQ (matching question) | 
| [oq1](examples/oq1.question.xml) | OQ (ordering question) | 

## Important Changes

Many different changes to the structure of question XML documents have been made. Below are described some of the key design decisions.

### Introduction of &lt;s&gt; tags

`<s>` tags are now used to identify sentences in text. This improves readability and allows for more automated analysis of questions.

### &lt;m&gt; tags replace &lt;latex&gt; tags and dollar signs

In the content currently, sections of mathematical notation are indicated by both `<latex>` tags and dollar signs - normally something like `<latex>$y = mx + c$<latex>`. This makes the XML harder to read and is excessive. The new XML structure introduces `<m>` 'mathematics' tags. This makes the XML easier to read.

### &lt;unit&gt; tags can now exist on there own

Previously, `<unit>` tags could only exist within `<quantity>` tags. However, there are many occasions where we want to express a unit only, and not a quantity (such as in expressions like 'Give your answer in days to 2 significant figures.'). `<unit>` tags can now exist on there own, and the `type` attribute on the `<quantity>` tag has been replaced by the `form` attribute on the `<unit>` tag.

### &lt;solution&gt; tags added to every question part

Now that we have started writing explainers, and we have some solution text for many questions, we will need to store this somewhere. It makes sense to store the solution text for a question in the question XML document. Each part now has at least one `<solution>` element to contain this text.

### FITBQs become their own question type

So far, FITBQs (fill-in-the-blanks questions) have been made using the MCQ format. This is very non-ideal. Since we will probably want students to be able to drag and drop terms into the blanks of an FITBQ question (it will require a new XML structure to describe how to do this for a given question), and since there are quite a few FITBQs in the content, it makes sense to make these a new question type.

### MRQs are now just a type of MCQ

MRQs (multiple-response questions) and MCQs (multiple-choice questions) become one and the same - both known as MCQs. This is because the only difference between them is that MCQs have one correct answer choice, and MRQs have more than one. MCQs are just the special case of an MRQ where n, the number of correct answer choices, equals 1.

MRQs can still be identified, because the number of `<choice>` elements with `is_correct_answer="true"` is greater than 1.