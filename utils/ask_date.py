from datetime import datetime
from tkinter import simpledialog, messagebox
from typing import Optional


# Функція для перевірки коректного формату дати
def ask_date(prompt: str) -> Optional[datetime]:
    while True:
        date_str = simpledialog.askstring(prompt, f"{prompt} (YYYY-MM-DD) або залиште пустим:")
        if not date_str:  # Якщо дата не введена, повертаємо None
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Помилка", "Неправильний формат дати. Використовуйте формат YYYY-MM-DD.")
