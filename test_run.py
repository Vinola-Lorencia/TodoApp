from App.task_service import TaskService

service = TaskService()

task = service.add_task("Test Task")

print(task)
print(service.tasks)