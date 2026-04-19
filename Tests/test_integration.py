import pytest
from App.task_service import TaskService


# ========================
# INTEGRATION TEST
# ========================

def test_full_task_flow():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study Integration", "High")

    service.complete_task(task["id"])
    service.increment_pomodoro(task["id"])

    stats = service.get_statistics()

    assert stats["total"] == 1
    assert stats["completed"] == 1
    assert stats["pomodoro"] == 1


def test_add_and_delete_flow():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Task Delete")

    service.delete_task(task["id"])

    assert len(service.get_tasks()) == 0


def test_search_after_add():
    service = TaskService()
    service.tasks = []

    service.add_task("Belajar Python")
    service.add_task("Makan siang")

    result = service.search_task("python")

    assert len(result) == 1


def test_progress_after_multiple_actions():
    service = TaskService()
    service.tasks = []

    t1 = service.add_task("Task 1")
    t2 = service.add_task("Task 2")

    service.complete_task(t1["id"])

    progress = service.calculate_progress()

    assert progress == 50


def test_overdue_integration():
    service = TaskService()
    service.tasks = []

    # inject manual overdue task
    service.tasks.append({
        "id": 1,
        "title": "Old Task",
        "completed": False,
        "priority": "Medium",
        "deadline": "2000-01-01",
        "pomodoro_sessions": 0
    })

    stats = service.get_statistics()

    assert stats["overdue"] == 1