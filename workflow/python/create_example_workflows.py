from workflows import * 

workflow1 = Workflow("New Lesson Scope Workflow")

courseDesign = workflow1.addStatus("Course Design")
subjectReview = workflow1.addStatus("Subject Review")

workflow1.addTransition(courseDesign, subjectReview, "Submit to Subject Review", "Submit", "", "", "submit")

workflow1.save("../examples/new_lesson_scope.workflow.xml")