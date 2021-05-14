from workflows import * 

workflow1 = Workflow("New Lesson Scope Workflow", "This workflow is used for creating new lesson scopes.")

courseDesign = workflow1.addStatus("Course Design", "The lesson scope is being written according to the requirements of different courses.")
subjectReview = workflow1.addStatus("Subject Review", "The lesson scope is being checked for clarity and ambiguity.")
copyediting = workflow1.addStatus("Copyediting", "The lesson scope is being copyedited.")
markup = workflow1.addStatus("Markup", "The lesson scope is being marked-up.")
markupReview = workflow1.addStatus("Markup Review", "The markup of the lesson scope is being reviewed.")
finalReview = workflow1.addStatus("Final Review", "This is the final review before the lesson scope goes live.")
published = workflow1.addStatus("Published", "The lesson scope has been published.")

t1 = workflow1.addTransition(courseDesign, subjectReview, "Submit to Subject Review", "Submit", "", "", "submit")
t1.rules.append(RolesRule(["course_designer"]))

t2 = workflow1.addTransition(subjectReview, courseDesign, "Send back to Course Design", "Reject", "", "", "reject", True)
t2.rules.append(RolesRule(["subject_reviewer"]))

t3 = workflow1.addTransition(subjectReview, copyediting, "Send to Copyediting", "Approve", "", "", "approve")
t3.rules.append(RolesRule(["subject_reviewer"]))

t4 = workflow1.addTransition(copyediting, markup, "Send to Markup", "Send to Markup", "", "", "send")
t4.rules.append(RolesRule(["copyeditor"]))

t5 = workflow1.addTransition(markup, markupReview, "Submit to Markup Review", "Submit", "", "", "submit")
t5.rules.append(RolesRule(["markup_editor"]))

t6 = workflow1.addTransition(markupReview, markup, "Send back to Markup", "Reject", "", "", "reject", True)
t6.rules.append(RolesRule(["markup_reviewer"]))

t7 = workflow1.addTransition(markupReview, finalReview, "Send to Final Review", "Approve", "", "", "approve")
t7.rules.append(RolesRule(["markup_reviewer"]))

t8 = workflow1.addTransition(finalReview, markup, "Send back to Markup", "Send back to Markup", "", "", "reject", True)
t8.rules.append(RolesRule(["course_designer"]))

t9 = workflow1.addTransition(finalReview, courseDesign, "Send back to Course Design", "Send back to Course Design", "", "", "reject", True)
t9.rules.append(RolesRule(["course_designer"]))

t10 = workflow1.addTransition(finalReview, published, "Publish", "Approve and Publish", "", "", "approve")
t10.rules.append(RolesRule(["course_designer"]))

workflow1.save("../examples/new_lesson_scope.workflow.xml")