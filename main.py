import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()

        # Поля формы
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(root, textvariable=self.type_var,
                                     values=["Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"])
        self.type_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Date", "Type", "Duration"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type_var = tk.StringVar()
        self.filter_type_combo = ttk.Combobox(root, textvariable=self.filter_type_var,
                                           values=["Все", "Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"])
        self.filter_type_combo.set("Все")
        self.filter_type_combo.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтры", command=self.apply_filters).grid(row=7, column=0, columnspan=2, pady=10)

        self.refresh_table()

    def validate_input(self):
        """Проверка корректности ввода"""
        try:
            date = datetime.strptime(self.date_entry.get(), "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД.ММ.ГГГГ")
            return False

        try:
            duration = int(self.duration_entry.get())
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return False

        if not self.type_var.get():
            messagebox.showerror("Ошибка", "Выберите тип тренировки")
            return False

        return True

    def add_training(self):
        """Добавление тренировки"""
        if self.validate_input():
            training = {
                "date": self.date_entry.get(),
                "type": self.type_var.get(),
                "duration": int(self.duration_entry.get())
            }
            self.trainings.append(training)
            self.save_data()
            self.refresh_table()
            # Очистка полей
            self.date_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.type_combo.set("")

    def refresh_table(self, filtered_trainings=None):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        trainings_to_show = filtered_trainings if filtered_trainings else self.trainings
        for training in trainings_to_show:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

    def apply_filters(self):
        """Применение фильтров"""
        filtered = self.trainings

        # Фильтр по типу
        selected_type = self.filter_type_var.get()
        if selected_type != "Все":
            filtered = [t for t in filtered if t["type"] == selected_type]

        # Фильтр по дате
        filter_date = self.filter_date_entry.get()
        if filter_date:
            try:
                datetime.strptime(filter_date, "%d.%m.%Y")
                filtered = [t for t in filtered if t["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты фильтра")
                return

        self.refresh_table(filtered)

    def save_data(self):
        """Сохранение данных в JSON"""
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """Загрузка данных из JSON"""
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
        except FileNotFoundError:
            self.trainings = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
