import requests
from requests.auth import HTTPBasicAuth
import tkinter as tk


def authenticate():
    url = 'https://httpbin.org/basic-auth/shkurin/1234'
    username = username_entry.get()
    password = password_entry.get()

    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        login_window.destroy()
        show_calculator()
    else:
        auth_label.config(text="Ошибка: неверные данные", fg="red")


def show_calculator():
    def calculate(operation):
        try:
            num1 = float(entry1.get())
            num2 = float(entry2.get())

            if operation == '+':
                res = num1 + num2
            elif operation == '-':
                res = num1 - num2
            elif operation == '*':
                res = num1 * num2
            elif operation == '/':
                if num2 != 0:
                    res = num1 / num2
                else:
                    result_label.config(text="Ошибка: деление на ноль!")
                    return

            result_label.config(text=f"Результат: {res}")
        except ValueError:
            result_label.config(text="Ошибка: введите числа!")

    root = tk.Tk()
    root.title("Калькулятор")

    entry1 = tk.Entry(root, font=("Arial", 16), width=15)
    entry1.pack(pady=10)

    entry2 = tk.Entry(root, font=("Arial", 16), width=15)
    entry2.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text='+', font=("Arial", 14), command=lambda: calculate('+'))
    add_button.grid(row=0, column=0, padx=10)

    sub_button = tk.Button(button_frame, text='-', font=("Arial", 14), command=lambda: calculate('-'))
    sub_button.grid(row=0, column=1, padx=10)

    mul_button = tk.Button(button_frame, text='*', font=("Arial", 14), command=lambda: calculate('*'))
    mul_button.grid(row=0, column=2, padx=10)

    div_button = tk.Button(button_frame, text='/', font=("Arial", 14), command=lambda: calculate('/'))
    div_button.grid(row=0, column=3, padx=10)

    result_label = tk.Label(root, text="Результат:", font=("Arial", 16))
    result_label.pack(pady=10)
    root.mainloop()


login_window = tk.Tk()
login_window.title("Авторизация")

tk.Label(login_window, text="Логин:").pack(pady=5)
username_entry = tk.Entry(login_window, font=("Arial", 14))
username_entry.pack(pady=5)

tk.Label(login_window, text="Пароль:").pack(pady=5)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 14))
password_entry.pack(pady=5)

auth_button = tk.Button(login_window, text="Войти", command=authenticate)
auth_button.pack(pady=10)

auth_label = tk.Label(login_window, text="")
auth_label.pack(pady=5)

login_window.mainloop()