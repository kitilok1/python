import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def setup_database():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
    ''')
    conn.commit()
    conn.close()

setup_database()

app = tk.Tk()
app.title("Список сотрудников")
app.geometry("700x500")
app.configure(bg='#3498db')

frame_inputs = tk.Frame(app, bg='#3498db')
frame_inputs.pack(pady=20)

labels = ["ФИО", "Номер телефона", "Email", "Заработная плата"]
for label in labels:
    label_widget = tk.Label(frame_inputs, text=label, bg='#3498db', fg='white')
    label_widget.pack(side=tk.LEFT, padx=10)

entries = [tk.Entry(frame_inputs, width=20) for _ in labels]
for entry in entries:
    entry.pack(side=tk.LEFT, padx=10)

def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM employees'):
        tree.insert("", tk.END, values=row)
    conn.close()

def on_add():
    values = [entry.get() for entry in entries]
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO employees (full_name, phone_number, email, salary)
    VALUES (?, ?, ?, ?)
    ''', values)
    conn.commit()
    conn.close()
    refresh_tree()

add_button = tk.Button(app, text="Добавить", bg='#2ecc71', fg='white', command=on_add)
add_button.pack(pady=10)

def on_update():
    selected_item = tree.selection()[0]
    if not selected_item:
        return
    id = tree.item(selected_item, 'values')[0]
    new_values = [entry.get() for entry in entries]
    
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE employees 
    SET full_name = ?, phone_number = ?, email = ?, salary = ? 
    WHERE id = ?
    ''', (*new_values, id))
    conn.commit()
    conn.close()
    refresh_tree()

update_button = tk.Button(app, text="Изменить", bg='#f39c12', fg='white', command=on_update)
update_button.pack(pady=10)

def on_delete():
    selected_item = tree.selection()[0]
    if not selected_item:
        return
    id = tree.item(selected_item, 'values')[0]
    
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    refresh_tree()

delete_button = tk.Button(app, text="Удалить", bg='#e74c3c', fg='white', command=on_delete)
delete_button.pack(pady=10)

def on_search():
    search_term = search_entry.get()
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', ('%' + search_term + '%',)):
        tree.insert("", tk.END, values=row)
    conn.close()

search_label = tk.Label(app, text="Поиск по ФИО:", bg='#3498db', fg='white')
search_label.pack(pady=10)

search_entry = tk.Entry(app)
search_entry.pack(pady=10)

search_button = tk.Button(app, text="Поиск", bg='#2980b9', fg='white', command=on_search)
search_button.pack(pady=10)

tree = ttk.Treeview(app, columns=(1,2,3,4,5), show="headings", height=10)
tree.pack(pady=20)

tree.heading(1, text="ID")
tree.heading(2, text="ФИО")
tree.heading(3, text="Номер телефона")
tree.heading(4, text="Email")
tree.heading(5, text="Заработная плата")

tree.column(1, width=50)
tree.column(2, width=150)
tree.column(3, width=100)
tree.column(4, width=150)
tree.column(5, width=100)

refresh_tree()
app.mainloop()
