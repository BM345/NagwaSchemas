from histories import * 
from datetime import datetime 

history1 = History("explainer", "000000000001")
user1 = "example.user.1@nagwa.com"

history1.addAction(CreateEntityAction(datetime.now(), user1))
history1.addAction(CreateNewVersionAction(datetime.now(), user1, "1", "000000000001.1.xml"))
history1.addAction(ChangeWorkflowAction(datetime.now(), user1, "new_explainer_workflow"))
history1.addAction(ChangeWorkflowStatusAction(datetime.now(), user1, "", "drafting"))
history1.addAction(ChangeAssigneeAction(datetime.now(), user1, user1))
history1.addAction(ChangePriorityAction(datetime.now(), user1, "high"))

history1.save("../examples/000000000001.history.xml")