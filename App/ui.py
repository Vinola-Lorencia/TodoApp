import sys
import os
from App.task_service import TaskService

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QLabel,
    QProgressBar, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer


class TodoApp(QWidget):

    def __init__(self):
        super().__init__()
        self.task_service = TaskService()

        self.setWindowTitle("🌸 MINITEEN FocusFlow")
        self.setGeometry(300, 100, 550, 750)

        # ===== TIMER =====
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 25 * 60
        self.current_task_index = None

        self.init_ui()

    # ========================
    # INIT UI
    # ========================
    def init_ui(self):

        main_layout = QVBoxLayout()

        # ===== IMAGE =====
        image_label = QLabel()
        base_dir = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.join(base_dir, "Assets", "miniteen.png")

        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(250, 180, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)

        image_label.setAlignment(Qt.AlignCenter)

        # ===== HEADER =====
        header = QLabel("MINITEEN FOCUSFLOW")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 18, QFont.Bold))

        # ===== TIMER =====
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 20, QFont.Bold))

        # ===== STATISTICS =====
        self.stats_label = QLabel("")
        self.stats_label.setAlignment(Qt.AlignCenter)

        # ===== ADD BUTTON =====
        self.show_form_btn = QPushButton("➕ Add Task")
        self.show_form_btn.clicked.connect(self.toggle_form)

        # ===== FORM =====
        self.form_widget = QWidget()
        form_layout = QVBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Task title")

        self.priority = QComboBox()
        self.priority.addItems(["Low", "Medium", "High"])

        self.deadline = QLineEdit()
        self.deadline.setPlaceholderText("Deadline (YYYY-MM-DD)")

        self.add_button = QPushButton("Save Task")
        self.add_button.clicked.connect(self.add_task)

        form_layout.addWidget(self.task_input)
        form_layout.addWidget(self.priority)
        form_layout.addWidget(self.deadline)
        form_layout.addWidget(self.add_button)

        self.form_widget.setLayout(form_layout)
        self.form_widget.setVisible(False)

        # ===== SEARCH =====
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search task...")

        self.search_button = QPushButton("🔍")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # ===== TASK LIST =====
        self.task_list = QListWidget()

        # ===== BUTTONS =====
        btn_layout = QHBoxLayout()

        self.complete_btn = QPushButton("✔ Complete")
        self.delete_btn = QPushButton("🗑 Delete")
        self.pomodoro_btn = QPushButton("🍅 Start")

        btn_layout.addWidget(self.complete_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.pomodoro_btn)

        # ===== PROGRESS =====
        self.progress_label = QLabel("Progress: 0%")
        self.progress_label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # ===== LAYOUT =====
        main_layout.addWidget(image_label)
        main_layout.addWidget(header)
        main_layout.addWidget(self.timer_label)
        main_layout.addWidget(self.stats_label)
        main_layout.addWidget(self.show_form_btn)
        main_layout.addWidget(self.form_widget)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.task_list)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.progress_label)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)

        self.apply_styles()
        self.connect_events()
        self.load_tasks()

    # ========================
    # EVENTS
    # ========================
    def connect_events(self):
        self.complete_btn.clicked.connect(self.complete_task)
        self.delete_btn.clicked.connect(self.delete_task)
        self.pomodoro_btn.clicked.connect(self.start_pomodoro)

        self.search_button.clicked.connect(self.search_task)
        self.search_input.returnPressed.connect(self.search_task)

    # ========================
    # TOGGLE FORM
    # ========================
    def toggle_form(self):
        self.form_widget.setVisible(not self.form_widget.isVisible())

    # ========================
    # LOAD TASKS
    # ========================
    def load_tasks(self):
        self.task_list.clear()

        tasks = self.task_service.get_tasks()

        for task in tasks:
            text = self.format_task(task)
            self.task_list.addItem(text)

        self.update_progress()
        self.update_stats()

    # ========================
    # FORMAT TASK
    # ========================
    def format_task(self, task):
        text = f"{task['title']} | {task['priority']} | 🍅 {task['pomodoro_sessions']}"

        if task["deadline"]:
            text += f" | 📅 {task['deadline']}"
            try:
                if self.task_service.is_overdue(task["id"]):
                    text += " ❗OVERDUE"
            except:
                pass

        if task["completed"]:
            text += " ✅"

        return text

    # ========================
    # SEARCH
    # ========================
    def search_task(self):
        keyword = self.search_input.text().strip()

        if keyword == "":
            self.load_tasks()
            return

        results = self.task_service.search_task(keyword)

        self.task_list.clear()

        for task in results:
            self.task_list.addItem(self.format_task(task))

    # ========================
    # ADD TASK
    # ========================
    def add_task(self):
        title = self.task_input.text().strip()
        priority = self.priority.currentText()
        deadline = self.deadline.text() or None

        try:
            self.task_service.add_task(title, priority, deadline)

            self.task_input.clear()
            self.deadline.clear()
            self.form_widget.setVisible(False)

            self.load_tasks()

        except Exception as e:
            QMessageBox.warning(self, "Input Error", str(e))

    # ========================
    # COMPLETE
    # ========================
    def complete_task(self):
        index = self.task_list.currentRow()
        if index < 0:
            return

        task = self.task_service.get_tasks()[index]
        self.task_service.complete_task(task["id"])
        self.load_tasks()

    # ========================
    # DELETE
    # ========================
    def delete_task(self):
        index = self.task_list.currentRow()
        if index < 0:
            return

        task = self.task_service.get_tasks()[index]
        self.task_service.delete_task(task["id"])
        self.load_tasks()

    # ========================
    # POMODORO
    # ========================
    def start_pomodoro(self):

        if self.timer.isActive():
            self.timer.stop()
            self.timer_label.setText("25:00")
            self.pomodoro_btn.setText("🍅 Start")
            return

        index = self.task_list.currentRow()
        if index < 0:
            return

        self.current_task_index = index
        self.time_left = 25 * 60

        self.timer.start(1000)
        self.pomodoro_btn.setText("⏹ Stop")

    # ========================
    # TIMER
    # ========================
    def update_timer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60

        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

        if self.time_left == 0:
            self.timer.stop()

            task = self.task_service.get_tasks()[self.current_task_index]
            self.task_service.increment_pomodoro(task["id"])

            self.load_tasks()

            self.timer_label.setText("25:00")
            self.pomodoro_btn.setText("🍅 Start")
            return

        self.time_left -= 1

    # ========================
    # PROGRESS
    # ========================
    def update_progress(self):
        percent = self.task_service.calculate_progress()
        self.progress_bar.setValue(percent)
        self.progress_label.setText(f"Progress: {percent}%")

    # ========================
    # STATISTICS
    # ========================
    def update_stats(self):
        stats = self.task_service.get_statistics()

        text = (
            f"📊 Total: {stats['total']} | "
            f"✅ Done: {stats['completed']} | "
            f"🍅 Pomodoro: {stats['pomodoro']} | "
            f"❗ Overdue: {stats['overdue']}"
        )

        self.stats_label.setText(text)

    # ========================
    # STYLE
    # ========================
    def apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #FFEAF4;
        }

        QLabel {
            color: #444;
        }

        QLineEdit, QComboBox {
            padding: 8px;
            border-radius: 10px;
            border: 1px solid #FFB6D9;
            background-color: white;
        }

        QPushButton {
            background-color: #FFB6D9;
            border-radius: 10px;
            font-weight: bold;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #FFA4CF;
        }

        QListWidget {
            background-color: white;
            border-radius: 10px;
            padding: 5px;
        }

        QProgressBar {
            border-radius: 8px;
            text-align: center;
        }

        QProgressBar::chunk {
            background-color: #FF8CC8;
            border-radius: 8px;
        }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())