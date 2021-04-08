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