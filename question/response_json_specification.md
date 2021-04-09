# Response JSON Specification

This document gives the specification for the JSON format we use for students' responses to questions.

## Table of Contents

## Overview

Each response given by a student to a question part should be stored as a JSON object. Note that a response object corresponds to a __question part__, and not simply the entire __question__. This is because students must be able to submit responses to the different parts of a question (if there is more than one) separately. Students may also submit multiple responses to a question part that do not pass validation, thus they are required to alter and then resubmit their answer.

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
    "correct_answer": {},
    "evaluation": {}
}
```

### Evaluation Object

The evaluation object captures the evaluation of a student's answer.

Answers can be evaluated in different ways. Most of the time, answers are evaluated programmatically by comparing the student's answer to the correct answer. For multiple choice questions, this means simply comparing the list of the student's choices to the list of correct choices. Sometimes, however, the answer must be assessed by a teacher. This is the case with free response questions.

The evaluation object captures _whether_ a given response has yet been evaluated (and hence whether a teacher needs to evaluate it), and, once it has been evaluated, the evaluation method. It also captures the number of marks that a student has been given for their answer.

The table below lists the possible properties of this object.

| Property | Required | Allowed Values | Description | 
| --- | --- | --- | --- |
| `response_has_been_evaluated` | Required | boolean | denotes whether this response has yet been evaluated; for questions such as MCQs, MQs, OQs, SQs, et cetera - which can be evaluated automatically - this property will be set to `true` straight away; for questions such as FRQs - which require teacher input - this value will need to be set to `false` when the student first submits their answer, and then changed to true once the teacher has marked it |