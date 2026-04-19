import pytest
from App.task_service import TaskService


# ========================
# BASIC TEST
# ========================

def test_add_task():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study Testing", "High")

    assert task["title"] == "Study Testing"
    assert task["completed"] is False
    assert task["priority"] == "High"
    assert task["pomodoro_sessions"] == 0


def test_complete_task():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study Testing")

    completed_task = service.complete_task(task["id"])

    assert completed_task["completed"] is True


def test_delete_task():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study Testing")

    service.delete_task(task["id"])

    assert len(service.tasks) == 0


# ========================
# PROGRESS TEST
# ========================

def test_progress_empty():
    service = TaskService()
    service.tasks = []

    assert service.calculate_progress() == 0


def test_progress_no_completed():
    service = TaskService()
    service.tasks = []

    service.add_task("Study Testing")

    assert service.calculate_progress() == 0


def test_progress_completed():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study Testing")
    service.complete_task(task["id"])

    assert service.calculate_progress() == 100


def test_progress_partial():
    service = TaskService()
    service.tasks = []

    t1 = service.add_task("Task 1")
    t2 = service.add_task("Task 2")

    service.complete_task(t1["id"])

    assert service.calculate_progress() == 50


# ========================
# VALIDATION TEST
# ========================

def test_add_task_empty():
    service = TaskService()
    service.tasks = []

    with pytest.raises(ValueError):
        service.add_task("")


def test_invalid_priority():
    service = TaskService()
    service.tasks = []

    with pytest.raises(ValueError):
        service.add_task("Study", "Super")


def test_invalid_deadline_format():
    service = TaskService()
    service.tasks = []

    with pytest.raises(ValueError):
        service.add_task("Study", deadline="2024/01/01")


def test_deadline_in_past():
    service = TaskService()
    service.tasks = []

    with pytest.raises(ValueError):
        service.add_task("Study", deadline="2000-01-01")


# ========================
# EDGE CASE TEST
# ========================

def test_complete_task_not_found():
    service = TaskService()
    service.tasks = []

    with pytest.raises(ValueError):
        service.complete_task(999)


def test_delete_task_not_found():
    service = TaskService()
    service.tasks = []

    with pytest.raises(ValueError):
        service.delete_task(999)


# ========================
# POMODORO TEST
# ========================

def test_increment_pomodoro():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study")

    updated = service.increment_pomodoro(task["id"])

    assert updated["pomodoro_sessions"] == 1


def test_increment_pomodoro_multiple():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study")

    service.increment_pomodoro(task["id"])
    service.increment_pomodoro(task["id"])

    assert task["pomodoro_sessions"] == 2


# ========================
# DEADLINE TEST (FIXED)
# ========================

def test_not_overdue():
    service = TaskService()
    service.tasks = []

    task = service.add_task("Study", deadline="2099-01-01")

    assert service.is_overdue(task["id"]) is False


def test_overdue():
    service = TaskService()
    service.tasks = []

    # bypass validation (inject langsung)
    task = {
        "id": 1,
        "title": "Old Task",
        "completed": False,
        "priority": "Medium",
        "deadline": "2000-01-01",
        "pomodoro_sessions": 0
    }

    service.tasks.append(task)

    assert service.is_overdue(1) is True


# ========================
# SEARCH TEST
# ========================

def test_search_task():
    service = TaskService()
    service.tasks = []

    service.add_task("Belajar Python")
    service.add_task("Makan siang")

    result = service.search_task("python")

    assert len(result) == 1
    assert result[0]["title"] == "Belajar Python"


def test_search_not_found():
    service = TaskService()
    service.tasks = []

    service.add_task("Belajar Python")

    result = service.search_task("Java")

    assert result == []


# ========================
# SORT TEST
# ========================

def test_sort_by_priority():
    service = TaskService()
    service.tasks = []

    service.add_task("Task Low", "Low")
    service.add_task("Task High", "High")
    service.add_task("Task Medium", "Medium")

    sorted_tasks = service.sort_by_priority()

    assert sorted_tasks[0]["priority"] == "High"


# ========================
# ID TEST
# ========================

def test_generate_id_unique():
    service = TaskService()
    service.tasks = []

    t1 = service.add_task("Task 1")
    t2 = service.add_task("Task 2")

    assert t1["id"] != t2["id"]


# ========================
# STATISTICS TEST
# ========================

def test_statistics_empty():
    service = TaskService()
    service.tasks = []

    stats = service.get_statistics()

    assert stats["total"] == 0
    assert stats["completed"] == 0
    assert stats["overdue"] == 0
    assert stats["pomodoro"] == 0


def test_statistics_filled():
    service = TaskService()
    service.tasks = []

    t1 = service.add_task("Task 1", deadline="2099-01-01")

    # inject overdue
    service.tasks.append({
        "id": 99,
        "title": "Old Task",
        "completed": False,
        "priority": "Medium",
        "deadline": "2000-01-01",
        "pomodoro_sessions": 0
    })

    service.complete_task(t1["id"])
    service.increment_pomodoro(t1["id"])
    service.increment_pomodoro(t1["id"])

    stats = service.get_statistics()

    assert stats["total"] == 2
    assert stats["completed"] == 1
    assert stats["pomodoro"] == 2
    assert stats["overdue"] == 1