from App.storage import Storage
from datetime import datetime


class TaskService:
    def __init__(self):
        self.storage = Storage()
        self.tasks = self.storage.load_tasks()

    # ========================
    # CREATE TASK
    # ========================
    def add_task(self, title, priority="Medium", deadline=None):
        # 🔥 VALIDASI TITLE
        if title.strip() == "":
            raise ValueError("Task title cannot be empty.")

        # 🔥 VALIDASI PRIORITY
        if priority not in ["Low", "Medium", "High"]:
            raise ValueError("Invalid priority.")

        # 🔥 VALIDASI DEADLINE (FORMAT + LOGIC)
        if deadline:
            try:
                date_obj = datetime.strptime(deadline, "%Y-%m-%d")
            except:
                raise ValueError("Deadline must be in format YYYY-MM-DD")

            # ❗ opsional tapi bagus
            if date_obj.date() < datetime.today().date():
                raise ValueError("Deadline cannot be in the past")

        task = {
            "id": self._generate_id(),
            "title": title,
            "completed": False,
            "priority": priority,
            "deadline": deadline,
            "pomodoro_sessions": 0
        }

        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        return task

    # ========================
    # GENERATE ID (ANTI DUPLIKAT)
    # ========================
    def _generate_id(self):
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1

    # ========================
    # GET TASKS
    # ========================
    def get_tasks(self):
        return self.tasks

    # ========================
    # COMPLETE TASK
    # ========================
    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.storage.save_tasks(self.tasks)
                return task
        raise ValueError("Task not found.")

    # ========================
    # DELETE TASK
    # ========================
    def delete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.storage.save_tasks(self.tasks)
                return task
        raise ValueError("Task not found.")

    # ========================
    # POMODORO FEATURE
    # ========================
    def increment_pomodoro(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["pomodoro_sessions"] += 1
                self.storage.save_tasks(self.tasks)
                return task
        raise ValueError("Task not found.")

    # ========================
    # DEADLINE CHECK
    # ========================
    def is_overdue(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                if task["deadline"] is None:
                    return False

                deadline_date = datetime.strptime(task["deadline"], "%Y-%m-%d")
                return datetime.now() > deadline_date

        raise ValueError("Task not found.")

    # ========================
    # SEARCH TASK
    # ========================
    def search_task(self, keyword):
        return [
            task for task in self.tasks
            if keyword.lower() in task["title"].lower()
        ]

    # ========================
    # PRODUCTIVITY
    # ========================
    def calculate_progress(self):
        if len(self.tasks) == 0:
            return 0

        completed = sum(1 for t in self.tasks if t["completed"])
        return int((completed / len(self.tasks)) * 100)

    # ========================
    # SORT BY PRIORITY
    # ========================
    def sort_by_priority(self):
        priority_order = {"High": 3, "Medium": 2, "Low": 1}

        return sorted(
            self.tasks,
            key=lambda t: priority_order.get(t["priority"], 0),
            reverse=True
        )

    # ========================
    # 🔥 STATISTICS (BONUS NILAI)
    # ========================
    def get_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        overdue = sum(
            1 for t in self.tasks
            if t["deadline"] and self.is_overdue(t["id"])
        )
        pomodoro = sum(t["pomodoro_sessions"] for t in self.tasks)

        return {
            "total": total,
            "completed": completed,
            "overdue": overdue,
            "pomodoro": pomodoro
        }