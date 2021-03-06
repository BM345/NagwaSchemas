# Response JSON Specification

This document gives the specification for the JSON format we use for storing students' responses to questions.

## Table of Contents

+ [Overview](#overview)
+ [Examples](#examples)
+ [Structure](#structure)
    + [Answer Objects](#answer-objects)
        + [response_format = "choices"](#response_format--choices)
        + [response_format = "input_text"](#response_format--input_text)
        + [response_format = "select_text"](#response_format--select_text)
        + [response_format = "order_items"](#response_format--order_items)
        + [response_format = "match_items"](#response_format--match_items)
        + [response_format = "free_response"](#response_format--free_response)
        + [response_format = "yes_or_no"](#response_format--yes_or_no)
        + [response_format = "true_or_false"](#response_format--true_or_false)
    + [Validation Object](#validation-object)
    + [Evaluation Object](#evaluation-object)

## Overview

Information about a student's response to a question part is stored as a JSON object. Note that each JSON object represents a student's response to a __question part__, not to an entire __question__. This is because students must be able to submit responses to the different parts of a question (if there is more than one part) separately. Students must also be able to resubmit their answer to a given question part if their answer does not pass validation - a separate response object will be required for each attempt.

## Examples

The Response JSON format should be fairly easy to understand just from looking at examples of it. The table below gives links to examples for different question part types.

| Part Type | Link |
|---|---|
| MCQ, answered as multiple-choice | [Link](examples/578143060713_part3_choices.json) |
| MCQ, answered as text-input where the answer passed validation | [Link](examples/578143060713_part3_inputtext.json) |
| MCQ, answered as text-input where the answer did not pass validation | [Link](examples/578143060713_part3_inputtext_validationfailed.json) |
| MRQ (MRQs are merged with MCQs in the new question XML specification), answered as multiple-choice | [Link](examples/625137396409_part1_choices.json) |
| SQ | [Link](examples/sq1_part1_selecttext.json) |
| OQ | [Link](examples/oq1_part1_orderitems.json) |
| MQ | [Link](examples/mq1_part1_matchitems.json) |
| FRQ, before the teacher has marked the student's answer | [Link](examples/682162714504_part1_freeresponse.json) |
| FRQ, after the teacher has marked the student's answer | [Link](examples/682162714504_part1_freeresponse_evaluated.json) |

## Structure

The top-level entity of a Response JSON file must be an object. The table below lists the possible properties of this object.

| Property | Required | Allowed Values | Description | 
| --- | --- | --- | --- |
| `question_id` | Required | string / a 12-digit entity id | the id of the question that this response has been given for |
| `question_version` | Required | string | the version of the question that this response has been given for; the version is usually an integer; stored here as a string just in case non-numeric versions are used |
| `instance` | Required | string | the reference for the instance of the question that this response has been given for |
| `part` | Required | string | the reference for the part of the question that this response has been given for |
| `submitted_at` | Required | string / timestamp | the date and time at which the response was submitted |
| `response_format` | Required | string / one of a set of values | the response format that the student gave their answer in; many of our questions can be answered in different ways - MCQs can often be answered either by a student choosing one option out of a set of options, or by typing in their answer into an answer box; the different ways that a student can answer a given question are defined in the Question XML; this property can have one of the following values: `choices`, `input_text`, `select_text`, `order_items`, `match_items`, `free_response`, `yes_or_no`, `true_or_false` |
| `student_answer` | Required | object | an object that captures the answer the student gave; [see below](#answer-objects) |
| `validation` | Required | object | an object that gives information about whether validation was applied to this response, and whether validation was passed; this includes the message that was sent to the student if the response did not pass validation, which is useful to know for identifying issues; [see below](#validation-object) |
| `normalised_student_answer` | | object | an object that gives the normalised version of the student's answer; this object only needs to be present if the student's answer was validated and it passed (in which case the validation code produces a normalised version of the student's answer); [see below](#answer-objects) |
| `correct_answer` | Required | object | an object that captures the correct answer; it's important to include this as a question may be later updated and the answer changed (perhaps because the answer was completely wrong, or because it was just slightly wrong - perhaps it was written to 3 d.p. when it should only have been to 2 d.p.); by storing the correct answer alongside the answer the student gave, it's always easy to see _why_ the student's answer would have been marked correct or incorrect; [see below](#answer-objects) |
| `evaluation` | Required | object | an object that captures the evaluation of the student's answer; [see below](#evaluation-object) |

#### Example

Below is shown an empty response object.

```json
{
    "question_id": "",
    "question_version": "",
    "instance": "",
    "part": "",
    "submitted_at": "",
    "response_format": "",
    "student_answer": {},
    "validation": {},
    "normalised_student_answer": {},
    "correct_answer": {},
    "evaluation": {}
}
```

### Answer Objects

The student answer object captures the answer that the student submitted for the question part. The normalised student answer object captures the normalised version of the answer that the student submitted. We only validate and normalise certain types of answers - answers where the student has had to type something into an answer box - so the normalised student answer object does not appear in all response objects. The correct answer object captures the correct answer to the question part.

The student answer object, the normalised student answer object, and the correct answer object always have the same structure as each other. What that structure is, however, is dependent on the value of the `response_format` property.

#### response_format = "choices"

The response format can be `choices` if the question part type is `mcq`. In this case, the answer objects have one property, `choices`, the value of which is an array of references. The references are defined in the question XML.

```json
"student_answer": {
    "choices": ["a"]
},
"correct_answer": {
    "choices": ["a"]
}
```

Below is shown an example of these objects for where the student must choose multiple options (an MRQ).

```json
"student_answer": {
    "choices": ["p", "r"]
},
"correct_answer": {
    "choices": ["p", "q"]
}
```

#### response_format = "input_text"

The response format can be `input_text` if the question part type is `mcq` (a multiple choice question), `ctsq` (a complete-the-sentence question), `cttq` (a complete-the-table question), or `cteq` (a complete-the-equation question).

```json
"student_answer": {
    "input_boxes": [
        {"reference": "k", "value": "9.22"}
    ]
},
"correct_answer": {
    "input_boxes": [
        {"reference": "k", "value": "3.45"}
    ]
}
```

#### response_format = "select_text"

The response format can be `select_text` if the question part type is `sq` (a select question). In this case, the answer objects have one property, `selections`, the value of which is an array of references.

```json
"student_answer": {
    "selections": ["a", "b", "c", "d"]
},
"correct_answer": {
    "selections": ["b", "d", "f", "g"]
}
```

#### response_format = "order_items"

The response format can be `order_items` if the question part type is `oq` (an ordering question). In this case the answer objects have one property, `items`, the value of which is an array of references. For the student answer object, this array shows the order that the student put the items in. For the correct answer object, this array shows the correct order of the items.

```json
"student_answer": {
    "items": ["a", "b", "d", "c", "e"]
},
"correct_answer": {
    "items": ["a", "b", "c", "d", "e"]
}
```

#### response_format = "match_items"

The response format can be `match_items` if the question part type is `mq` (a matching question). In this case the answer objects have one property, `matches`, the value of which is an array of match objects. Each match object has two properties: `from` and `to`, denoting a match between two list items, as defined by the question XML.

```json
"student_answer": {
    "matches": [
        {"from": "list 1, item 1", "to": "list 2, item 1"},
        {"from": "list 1, item 2", "to": "list 2, item 2"}
    ]
},
"correct_answer": {
    "matches": [
        {"from": "list 1, item 1", "to": "list 2, item 1"},
        {"from": "list 1, item 2", "to": "list 2, item 2"},
        {"from": "list 1, item 3", "to": "list 2, item 3"},
        {"from": "list 1, item 4", "to": "list 2, item 4"},
        {"from": "list 1, item 5", "to": "list 2, item 5"}
    ]
}
```

#### response_format = "free_response"

The response format can be `free_response` if the question part type is `frq` (a free response question). In this case, the answer objects have one property, `text`, the value of which is a string. 

```json
"student_answer": {
    "text": "<p>A galaxy is billions of stars and planets in a spiral in space.</p>"
},
"correct_answer": {
    "text": "<p><s>A galaxy is a collection of billions of stars.</s></p>"
},
```

Note that, because we are able to apply more semantic markup (sentence tags, quantity tags, et cetera) to the correct answer as given in the question XML, even if the wording of the student's answer is exactly the same as that in the model answer, the two strings will likely never be identical.

#### response_format = "yes_or_no"

The response format can be `yes_or_no` if the question part type is `ynq` (a yes-no question). In this case, the answer objects have one property, `value`, the value of which is either `"yes"` or `"no"`.

```json
"student_answer": {
    "value": "no"
},
"correct_answer": {
    "value": "yes"
}
```

#### response_format = "true_or_false"

The response format can be `true_or_false` if the question part type is `tfq` (a true-false question). In this case, the answer objects have one property, `value`, the value of which is either `true` or `false`.

```json
"student_answer": {
    "value": false
},
"correct_answer": {
    "value": true
}
```

### Validation Object

The validation object gives information about whether validation was applied to this response, and whether validation was passed.

For most response formats, there is no validation process. So, for most response formats, this object will simply be:

```json
"validation": {
    "applied": false
}
```

The only response format that we apply validation for is the `input_text` format.

In the case where validation is applied and the student's answer passes, this object will simply be:

```json
"validation": {
    "applied": true,
    "passed": true,
}
```

In the case where validation is applied and the student's answer doesn't pass, this object will be of the form:

```json
"validation": {
    "applied": true,
    "passed": false,
    "message_to_student": "Only use the characters 0 to 9 and the plus and minus signs in your answer. Your answer must be a single, whole number."
}
```

The message that the student is given if their answer does not pass validation should be included in the object. This is to make it easier to resolve issues with the platform. For example, perhaps a student attempts to answer a question several times, and each time they are shown a message, but that message simply doesn't make sense in the context of the question they are answering, so the message tells them to do the wrong thing. By recording the message, we can easily see what they were told to do, and what they did.

The table below defines the different properties of the validation object.

| Property | Required | Allowed Values | Description | 
| --- | --- | --- | --- |
| `applied` | Required | boolean | whether or not validation has been applied to the student's answer; this will only be `true` if `response_format` is equal to `input_text`, as this is the only response format we apply validation to; for all other response formats, this will be `false` |
| `passed` | Required only if `applied` is `true` | boolean | whether or not the student's answer passed validation |
| `message_to_student` | Required only if `applied` is `true` and `passed` is `false` | string | the message that the student received if their answer did not pass validation; this is useful for identifying issues |



### Evaluation Object

The evaluation object captures the evaluation of a student's answer.

Answers can be evaluated in different ways. Most of the time, answers are evaluated programmatically by comparing the student's answer to the correct answer. For multiple choice questions, this means simply comparing the list of the student's choices to the list of correct choices. Sometimes, however, the answer must be assessed by a teacher. This is the case with free response questions.

The evaluation object captures _whether_ a given response has yet been evaluated (and hence whether a teacher needs to evaluate it), and, once it has been evaluated, the evaluation method. It also captures the number of marks that a student has been given for their answer.

The table below lists the possible properties of this object.

| Property | Required | Allowed Values | Description | 
| --- | --- | --- | --- |
| `response_has_been_evaluated` | Required | boolean | denotes whether this response has yet been evaluated; for questions such as MCQs, SQs, OQs, MQs, et cetera - which can be evaluated automatically - this property will be set to `true` straight away; for questions such as FRQs - which require teacher input - this value will need to be set to `false` when the student first submits their answer, and then changed to `true` once the teacher has marked it |
| `evaluated_at` | Required once `response_has_been_evaluated` has been set to `true`; otherwise leave out | string / timestamp | the date and time at which the response was evaluated; if the answer was evaluated automatically, the value would be the server time when the response was received from the student; if the answer was evaluated by a teacher / user, it would be the server time when the teacher / user did so |
| `method` | Required once `response_has_been_evaluated` has been set to `true`; otherwise leave out | string / one of a set of values | denotes how this response was evaluated |
| `number_of_marks_available` | Required | integer | the maximum number of marks that can be given for this question part |
| `number_of_marks_given` | Required once `response_has_been_evaluated` has been set to `true`; otherwise leave out | integer | the number of marks that have been given to the student for their answer; equal to `number_of_marks_available` if the answer is completely correct; equal to 0 of the answer is completely incorrect; teachers may award some marks for FRQ answers that are partially correct; MQs may also allow partial marks |

The table below lists the possible values of the `method` property.

| Value | Meaning |
|---|---|
| `default` | the student's answer was evaluated automatically by direct comparison to the key; does not include if the validation code was used to parse the student's answer and provide a normalised form |
| `parser` | denotes that the student's answer was parsed using the validation code, and converted into a normalised form before being checked (or was checked for equality by the validation code itself); this will be useful in case there are issues with the parser code |
| `user` | denotes that a user had to manually check the answer and mark it; usually a teacher |

In the distant future, we may also be able to mark FRQs using neural networks. In this case, we will be able to set the `method` property to `neural_network`.

#### Example

Below is shown an example evaluation object.

```json
"evaluation": {
    "response_has_been_evaluated": true,
    "evaluated_at": "2021-03-30T10:00:03",
    "method": "default",
    "maximum_number_of_marks_available": 1,
    "number_of_marks_given": 1
}
```