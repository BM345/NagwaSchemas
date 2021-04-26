# Describing Workflows

This document describes how the workflows that we use in the development of Nagwa content can be generically described using a simple XML structure.

## Principles of Design

The diagram below shows a workflow that we might use for developing an explainer.

![](diagram_1.png)

The coloured boxes are **statuses**. When a content entity has a particular status, it usually means that someone in a particular team must take a particular action with the content entity. For example, if the status is 'Copyediting', then someone from the copyediting team must copyedit the content entity, or if the status is 'Final Review', then someone from the relevant subject team must review the content entity.

The black arrows are **transitions**. The transitions denote what the status of a given content entity may be updated to when it is at a given point in the workflow. Transitions can have **rules**. For example, in the diagram above, each of the two transitions away from the 'Drafting' status have rules to them - the transition to 'Course Review' is only permitted if the content entity *hasn't* been at 'Course Review' before, and the transition directly to 'Subject Review' (skipping 'Course Review') is only permitted if the content entity *has* been at 'Course Review' once before already.

Using these three concepts - statuses, transitions, and rules - we can easily describe a workflow with a simple XML structure. Below is shown this structure without any data in it.

```xml
<workflow>
    <name></name>
    <description></description>
    <statuses>
        <status reference="...">
            <name></name>
            <description></description>
        </status>
        <status reference="...">
            <name></name>
            <description></description>
        </status>
        <status reference="...">
            <name></name>
            <description></description>
        </status>
    </statuses>
    <transitions>
        <transition from="..." to="...">
            <name></name>
            <button_text></button_text>
            <description></description>
            <rules>
                <rule />
                <rule />
            </rules>
        </transition>
        <transition from="..." to="...">
            <name></name>
            <button_text></button_text>
            <description></description>
            <rules>
                <rule />
                <rule />
            </rules>
        </transition>
    </transitions>
</workflow>
```

The root element of the workflow XML is a `<workflow>` element. The `<statuses>` subelement contains the set of statuses for the workflow, and the `<transitions>` subelement contains the set of transitions. Each `<status>` element has a `reference` attribute, and these references are used in the `from` and `to` attributes on each `<transition>` element to denote which statuses the transition links. Each `<transition>` element contains a `<rules>` subelement, which contains the set of rules that apply to this transition.

Below is shown part of the workflow XML for the workflow shown in the diagram above. (The full XML for the above workflow can be viewed [here](workflows/examples/new_explainer.workflow.xml).)

```xml
<?xml version="1.0" encoding="utf-8" ?>
<workflow reference="new_explainer">
    <name>New Explainer Workflow</name>
    <description>This workflow is used for creating new explainers.</description>
    <statuses>
        <status reference="drafting" category="writing">
            <name>Drafting</name>
            <description>The explainer is being drafted.</description>
        </status>
        <status reference="course_review" category="writing">
            <name>Course Review</name>
            <description>The explainer is being reviewed for course suitability.</description>
        </status>
        <status reference="subject_review" category="writing">
            <name>Subject Review</name>
            <description>The explainer is being reviewed for its subject-specific content.</description>
        </status>
    </statuses>
    <transitions>
        <transition reference="submit_to_course_review" from="drafting" to="course_review" type="submit">
            <name>Submit to Course Review</name>
            <button_text>Submit</button_text>
            <description></description>
            <rules>
                <rule allow_if="role in ['content_writer']" />
                <rule allow_if="'submit_to_course_review' not in pastTransitions" />
            </rules>
        </transition>
        <transition reference="submit_to_subject_review_1" from="drafting" to="subject_review" type="submit">
            <name>Submit to Subject Review</name>
            <button_text>Submit</button_text>
            <description></description>
            <rules>
                <rule allow_if="role in ['content_writer']" />
                <rule allow_if="'submit_to_course_review' in pastTransitions" />
            </rules>
        </transition>
        <transition reference="submit_to_subject_review_2" from="course_review" to="subject_review" type="approve">
            <name>Submit to Subject Review</name>
            <button_text>Approve</button_text>
            <description></description>
            <rules>
                <rule allow_if="role in ['course_designer']" />
            </rules>
        </transition>
        <transition reference="send_back_to_drafting_1" from="course_review" to="drafting" type="reject">
            <name>Send back to Drafting</name>
            <button_text>Reject</button_text>
            <description></description>
            <rules>
                <rule allow_if="role in ['course_designer']" />
            </rules>
        </transition>
        <transition reference="send_to_copyediting" from="subject_review" to="copyediting" type="approve">
            <name>Send to Copyediting</name>
            <button_text>Approve</button_text>
            <description></description>
            <rules>
                <rule allow_if="role in ['subject_reviewer']" />
            </rules>
        </transition>
        <transition reference="send_back_to_drafting_2" from="subject_review" to="drafting" type="reject">
            <name>Send back to Drafting</name>
            <button_text>Reject</button_text>
            <description></description>
            <rules>
                <rule allow_if="role in ['subject_reviewer']" />
            </rules>
        </transition>
    </transitions>
</workflow>
```

