# Describing Workflows

This document describes how the workflows that we use in the development of Nagwa content can be generically described using a simple XML structure.

## Principles of Design

The diagram below shows a workflow that we might use for developing an explainer.

![](diagram_1.png)

The coloured boxes are **statuses**. When a content entity has a particular status, it usually means that someone in a particular team must take a particular action with the content entity. For example, if the status is 'Copyediting', then someone from the copyediting team must copyedit the content entity, or if the status is 'Final Review', then someone from the relevant subject team must review the content entity.

The black arrows are **transitions**. The transitions denote what the status of a given content entity may be updated to when it is at a given point in the workflow. Transitions can have **rules**. For example, in the diagram above, each of the two transitions away from the 'Drafting' status have rules to them - the transition to 'Course Review' is only permitted if that transition hasn't been made before, and the transition directly to 'Subject Review' (skipping 'Course Review') is only permitted if the content entity has been at 'Course Review' once before already.

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

