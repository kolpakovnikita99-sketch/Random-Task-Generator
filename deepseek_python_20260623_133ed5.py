"""
Random Task Generator
GUI-приложение для генерации случайных задач с сохранением истории и фильтрацией.
Использует Tkinter, random, JSON.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import os
from datetime import datetime

# Имя файла для хранения данных
DATA_FILE = "tasks_history.json"

# Предопределённый список задач (категория, описание)
DEFAULT_TASKS = [
    {"category": "учеба", "task": "Прочитать статью по Python"},
    {"category": "спорт", "task": "Сделать зарядку"},
    {"category": "работа", "task": "Написать отчёт"},
    {"category": "учеба", "task": "Решить задачи по математике"},
    {"category": "спорт", "task": "Пробежка 5 км"},
    {"category": "работа", "task": "Провести совещание"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Загрузка данных
        self.tasks = []          # список всех задач (словари с ключами category, task)
        self.history = []        # список сгенерированных задач (словари с датой и задачей)
        self.current_task = None

        self.load_data()

        # Переменные для UI
        self.category_filter = tk.StringVar(value="все")
        self.new_task_text = tk.StringVar()
        self.new_category = tk.StringVar(value="учеба")

        # Построение интерфейса
        self.create_widgets()
        self.update_history_display()

    # ---------- Работа с данными ----------
    def load_data(self):
        """Загружает задачи и историю из JSON, если файл существует."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", DEFAULT_TASKS.copy())
                    self.history = data.get("history", [])
                    return
            except (json.JSONDecodeError, IOError):
                pass
        # Если файла нет или ошибка — используем задачи по умолчанию
        self.tasks = DEFAULT_TASKS.copy()
        self.history = []

    def save_data(self):
        """Сохраняет текущие задачи и историю в JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump({"tasks": self.tasks, "history": self.history}, f, ensure_ascii=False, indent=2)
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные.")

    # ---------- Основная логика ----------
    def generate_task(self):
        """Выбирает случайную задачу из списка, добавляет в историю и отображает."""
        if not self.tasks:
            messagebox.showwarning("Нет задач", "Список задач пуст. Добавьте новые задачи.")
            return
        # Фильтр по категории (если не "все")
        filter_cat = self.category_filter.get()
        if filter_cat == "все":
            available = self.tasks
        else:
            available = [t for t in self.tasks if t["category"] == filter_cat]
        if not available:
            messagebox.showinfo("Нет задач", f"Нет задач в категории '{filter_cat}'. Добавьте новые.")
            return

        chosen = random.choice(available)
        self.current_task = chosen
        # Добавляем в историю с временем
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": chosen["category"],
            "task": chosen["task"]
        }
        self.history.append(entry)
        self.save_data()
        self.update_display()
        self.update_history_display()

    def add_task(self):
        """Добавляет новую задачу в список."""
        task_text = self.new_task_text.get().strip()
        category = self.new_category.get()
        if not task_text:
            messagebox.showwarning("Ошибка", "Введите описание задачи.")
            return
        # Проверка на дубликат (не обязательно)
        self.tasks.append({"category": category, "task": task_text})
        self.save_data()
        self.new_task_text.set("")
        messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена в категорию '{category}'.")
        # Обновляем интерфейс при необходимости

    # ---------- Интерфейс ----------
    def create_widgets(self):
        """Создаёт все элементы управления."""
        # Верхняя панель: фильтр и текущая задача
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(top_frame, text="Фильтр по категории:").pack(side=tk.LEFT, padx=5)
        filter_combo = ttk.Combobox(top_frame, textvariable=self.category_filter,
                                    values=["все", "учеба", "спорт", "работа"], state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())

        btn_generate = tk.Button(top_frame, text="🎲 Сгенерировать задачу", command=self.generate_task,
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_generate.pack(side=tk.RIGHT, padx=5)

        # Отображение текущей сгенерированной задачи
        self.current_label = tk.Label(self.root, text="Нажмите «Сгенерировать»", font=("Arial", 14, "bold"),
                                      fg="#333", wraplength=600)
        self.current_label.pack(pady=10)

        # Панель добавления новой задачи
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу", font=("Arial", 10, "bold"))
        add_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(add_frame, text="Задача:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(add_frame, textvariable=self.new_task_text, width=40).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Категория:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        cat_combo = ttk.Combobox(add_frame, textvariable=self.new_category,
                                 values=["учеба", "спорт", "работа"], state="readonly")
        cat_combo.grid(row=0, column=3, padx=5, pady=5)

        btn_add = tk.Button(add_frame, text="➕ Добавить", command=self.add_task, bg="#2196F3", fg="white")
        btn_add.grid(row=0, column=4, padx=10, pady=5)

        # История
        history_frame = tk.LabelFrame(self.root, text="История задач", font=("Arial", 10, "bold"))
        history_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Создаём Listbox с прокруткой
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set,
                                          font=("Courier", 9), height=12)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

    def update_display(self):
        """Обновляет отображение текущей задачи."""
        if self.current_task:
            self.current_label.config(text=f"{self.current_task['category'].capitalize()}: {self.current_task['task']}")
        else:
            self.current_label.config(text="Нажмите «Сгенерировать»")

    def update_history_display(self):
        """Обновляет список истории с учётом фильтра."""
        self.history_listbox.delete(0, tk.END)
        filter_cat = self.category_filter.get()
        for entry in reversed(self.history):  # от новых к старым
            if filter_cat == "все" or entry["category"] == filter_cat:
                display = f"{entry['timestamp']} | {entry['category'].capitalize()}: {entry['task']}"
                self.history_listbox.insert(tk.END, display)

    # ---------- Завершение ----------
    def on_close(self):
        """Сохраняет данные перед закрытием."""
        self.save_data()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()