# 🌸 FocusFlow - Task Management System

![CI](https://github.com/Vinola-Lorencia/TodoApp/actions/workflows/ci.yml/badge.svg)
![coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)

FocusFlow adalah aplikasi desktop berbasis Python menggunakan PyQt5 yang dirancang untuk membantu pengguna dalam mengelola tugas harian secara lebih produktif. Aplikasi ini mendukung fitur manajemen task, prioritas, deadline, Pomodoro timer, serta sistem statistik progres.

Project ini dibuat sebagai bagian dari tugas mata kuliah **Software Testing**, dengan implementasi automated testing dan CI/CD menggunakan GitHub Actions.

--- Update for triggering GitHub Actionsjjjj

## 🚀 Features

- ➕ Add, edit, delete, and complete tasks  
- 🎯 Priority system (Low, Medium, High)  
- 📅 Deadline tracking dengan validasi dan overdue detection  
- 🍅 Pomodoro timer (25 menit fokus session)  
- 🔍 Search task berdasarkan keyword  
- 📊 Progress tracking (persentase task selesai)  
- 📈 Statistik task (total, completed, overdue, pomodoro sessions)  

---

## 🛠️ Tech Stack

- Python 3.11  
- PyQt5 (GUI Desktop Application)  
- Pytest (Unit & Integration Testing)  
- Pytest-Cov (Code Coverage)  
- GitHub Actions (CI/CD Pipeline)  

---

## 🛠️ Cara Menjalankan Aplikasi
1. Clone repository ini.
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
3. Jalankan aplikasi:cc
   ```bash
   python -m App.ui


## 📁 Project Structure

```txt
App/
 ├── ui.py              # GUI Layer (PyQt5)
 ├── task_service.py    # Business Logic
 ├── storage.py         # Data Persistence Layer
 └── Assets/            # UI Assets (images)

Tests/
 ├── test_task_service.py
 ├── test_storage.py
 └── test_integration.py

.github/
 └── workflows/
     └── ci.yml