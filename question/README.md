# Question XML

Below are listed links to examples of the new question XML format that are based on existing questions.

| Current XML | New XML | Key Features |
|---|---|---|
| [578143060713](examples/578143060713_current.question.xml) | [578143060713](examples/578143060713_new.question.xml) | Multi-part question with MCQs; single instance |
| [409158921650](examples/409158921650_current.question.xml) | [409158921650](examples/409158921650_new.question.xml) | Single-part; multiple instances; different solution text required for different instances |
| [676140256919](examples/676140256919_current.question.xml) | [676140256919](examples/676140256919_new.question.xml) | Figures; different answer formats |
| [505183812139](examples/505183812139_current.question.xml) | [505183812139](examples/505183812139_new.question.xml) | New FITBQ type |
| [682162714504](examples/682162714504_current.question.xml) | [682162714504](examples/682162714504_new.question.xml) | FRQ |
| [818183672624](examples/818183672624_current.question.xml) | [818183672624](examples/818183672624_new.question.xml) | With tables |
| [625137396409](examples/625137396409_current.question.xml) | [625137396409](examples/625137396409_new.question.xml) | MRQ becoming MCQ |

## Important Changes

Many different changes to the structure of question XML documents have been made. Below are described some of the key design decisions.

### &lt;unit&gt; tags can now exist on there own

Previously, `<unit>` tags could only exist within `<quantity>` tags. However, there are many occasions where we want to express a unit only, and not a quantity (such as in expressions like 'Give your answer in days to 2 significant figures.'). `<unit>` tags can now exist on there own, and the `type` attribute on the `&lt;quantity&gt;` tag has been replaced by the `form` attribute on the `&lt;unit&gt;` tag.

### &lt;solution&gt; tags added to every question part

Now that we have started writing explainers, and we have some solution text for many questions, we will need to store this somewhere. It makes sense to store the solution text for a question in the question XML document. Each part now has at least one `&lt;solution&gt;` element to contain this text.

### FITBQs become their own question type

So far, FITBQs (fill-in-the-blanks questions) have been made using the MCQ format. This is very non-ideal. Since we will probably want students to be able to drag and drop terms into the blanks of an FITBQ question (it will require a new XML structure to describe how to do this for a given question), and since there are quite a few FITBQs in the content, it makes sense to make these a new question type.

### MRQs are now just a type of MCQ

MRQs (multiple-response questions) and MCQs (multiple-choice questions) become one and the same - both known as MCQs. This is because the only difference between them is that MCQs have one correct answer choice, and MRQs have more than one. MCQs are just the special case of an MRQ where n, the number of correct answer choices, equals 1.

MRQs can still be identified, because the number of `&lt;choice&gt;` elements with `is_correct_answer="true"` is greater than 1.