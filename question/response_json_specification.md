# Response JSON Specification

This document gives the specification for the JSON format we use for students' responses to questions.

## Table of Contents

## Overview

Each response given by a student to a question part should be stored as a JSON object. Note that a response object corresponds to a __question part__, and not simply the entire __question__. This is because students must be able to submit responses to the different parts of a question (if there is more than one) separately. Students may also submit multiple responses to a question part that do not pass validation, thus they are required to alter and then resubmit their answer.

## Examples

The response JSON format should be fairly easy to understand just from looking at examples of it. The table below gives links to examples for different question part types.

| Part Type | Link |
|---|---|
| MCQ, answered as multiple-choice | [Link](examples/578143060713_part3_choices.json) |
| MCQ, answered as text-input | [Link](examples/578143060713_part3_inputtext.json) |
| MRQ (MRQs are merged with MCQs in new question XML specification), answered as multiple-choice | [Link](examples/625137396409_part1_choices.json) |
| FRQ, before the teacher has marked the student's answer | [Link](examples/682162714504_part1_freeresponse.json) |
| FRQ, after the teacher has marked the student's answer | [Link](examples/682162714504_part1_freeresponse_evaluated.json) |
| OQ | [Link](examples/oq1_part1_orderitems.json) |
| SQ | [Link](examples/sq1_part1_selecttext.json) |
| MQ | [Link](examples/mq1_part1_matchitems.json) |

## Structure

The top-level entity of a Response JSON file must be an object. The table below lists the possible properties of this object.

| Property | Required | Allowed Values | Description | 
| --- | --- | --- | --- |
| `question_id` | Required | string / a 12-digit entity id | the id of the question that this response has been given for |
| `question_version` | Required | string | the version of the question that this response has been given for; the version is usually an integer |
| `instance` | Required | string | the reference for the instance of the question that this response has been given for |
| `part` | Required | string | the reference for the part of the question that this response has been given for |
| `submitted_at` | Required | string / timestamp | the date and time at which the response was submitted |
| `response_format` | Required | string / one of a set of values | the response format that the student gave their answer in; many of our questions can be answered in different ways - MCQs can often be answered either by a student choosing one option out of a set of options, or by typing in their answer into an answer box; the different ways that a student can answer a given question are defined in the question XML; this property can have one of the following values: `choices`, `input_text`, `match_items`, `order_items`, `select_text`, `free_response`, `yes_or_no`, `true_or_false` |
| `student_answer` | Required | object | an object that captures the answer the student gave |
| `validation` | Required | object | an object that gives information about whether validation was applied to this response, and whether validation was passed; this includes the message that was sent to the student if the response did not pass validation, which is useful to know for identifying issues |
| `normalised_student_answer` | | object | an object that gives the normalised version of the student's answer |
| `correct_answer` | Required | object | an object that captures the correct answer; it's important to include this as a question may be later updated and the answer changed (perhaps because the answer was completely wrong, or because it was just slightly wrong - perhaps it was written to 3 d.p. when it should only have been to 2 d.p.); by storing the correct answer alongside the answer the student gave, it's always easy to see _why_ the student's answer would have been marked correct or incorrect |
| `evaluation` | Required | object | an object that captures the evaluation of the student's answer |

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

The student answer object, the normalised student answer object, and the correct answer object all always have the same structure as each other. What that structure is, however, is dependent on the value of the `response_format` property.

#### response_format = "choices"

The response format can be `choices` if the question part type is `mcq`. In this case the answer objects have one property, `choices`, the value of which is an array of references. For the student answer object, these references are for the choices that the student has chosen. For the correct answer object, these references are for the correct choices. An example of these objects is shown below.

```json
"student_answer": {
    "choices": ["a"]
},
"correct_answer": {
    "choices": ["a"]
}
```

Below is shown an example of these objects for where the students must choose multiple options (an MRQ).

```json
"student_answer": {
    "choices": ["p", "r"]
},
"correct_answer": {
    "choices": ["p", "q"]
}
```

#### response_format = "input_text"

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

#### response_format = "select_text"

#### response_format = "match_items"

#### response_format = "free_response"

#### response_format = "yes_or_no"

#### response_format = "true_or_false"

### Validation Object

The validation object gives information about whether validation was applied to this response, and whether validation was passed.

For most response formats, there is no validation process. So, for most response formats, this object will simply be:

```json
"validation": {
    "applied": false
}
```

The only response format that we apply validation for is the `input_text` format.

In the case of the `input_text` format where validation is applied and the student's answer passes, this object will simply be:

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

The message that the student is given if their answer does not pass validation should be included in the object. This is to make it easier to resolve issues with the platform. For example, perhaps a student attempts to answer a question several times, each time entering an answer that should pass validation, but doesn't. By recording the message, we will be able to see where the problem lies more easily.

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
| `response_has_been_evaluated` | Required | boolean | denotes whether this response has yet been evaluated; for questions such as MCQs, MQs, OQs, SQs, et cetera - which can be evaluated automatically - this property will be set to `true` straight away; for questions such as FRQs - which require teacher input - this value will need to be set to `false` when the student first submits their answer, and then changed to true once the teacher has marked it |
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

#### Example

Below is shown an example evaluation object.

```json
{
    "response_has_been_evaluated": true,
    "evaluated_at": "2021-03-30T10:00:03",
    "method": "default",
    "maximum_number_of_marks_available": 1,
    "number_of_marks_given": 1
}
```