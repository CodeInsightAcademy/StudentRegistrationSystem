import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='student'
)
c = conn.cursor()

# Create students table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT NOT NULL,
        gender VARCHAR(50) NOT NULL
    )
''')
conn.commit()

# Create the main application window
root = tk.Tk()
root.title("Student Registration System")

# Function to add a student to the database
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    gender = combo_gender.get()
    
    if name and age and gender:
        c.execute('INSERT INTO students (name, age, gender) VALUES (%s, %s, %s)', (name, age, gender))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
        clear_entries()
        populate_treeview()
    else:
        messagebox.showwarning("Input Error", "Please fill out all fields")

# Function to update selected student
def update_student():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item, 'values')[0]
        name = entry_name.get()
        age = entry_age.get()
        gender = combo_gender.get()

        if name and age and gender:
            c.execute('UPDATE students SET name = %s, age = %s, gender = %s WHERE id = %s', (name, age, gender, student_id))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully")
            clear_entries()
            populate_treeview()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a student to update")

# Function to delete selected student
def delete_student():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item, 'values')[0]
        c.execute('DELETE FROM students WHERE id = %s', (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully")
        clear_entries()
        populate_treeview()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a student to delete")

# Function to populate the treeview with student data
def populate_treeview():
    for row in tree.get_children():
        tree.delete(row)
    c.execute('SELECT * FROM students')
    for row in c.fetchall():
        tree.insert('', 'end', values=row)

# Function to clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    combo_gender.set('')

# Function to fill entry fields with selected student data
def on_tree_select(event):
    try:
        selected_item = tree.selection()[0]
        student_id, name, age, gender = tree.item(selected_item, 'values')
        entry_name.delete(0, tk.END)
        entry_name.insert(0, name)
        entry_age.delete(0, tk.END)
        entry_age.insert(0, age)
        combo_gender.set(gender)
    except IndexError:
        pass

# GUI layout
frame_form = ttk.Frame(root, padding="10")
frame_form.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(frame_form, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
entry_name = ttk.Entry(frame_form)
entry_name.grid(row=0, column=1, pady=2)

ttk.Label(frame_form, text="Age:").grid(row=1, column=0, sticky=tk.W, pady=2)
entry_age = ttk.Entry(frame_form)
entry_age.grid(row=1, column=1, pady=2)

ttk.Label(frame_form, text="Gender:").grid(row=2, column=0, sticky=tk.W, pady=2)
combo_gender = ttk.Combobox(frame_form, values=["Male", "Female", "Other"])
combo_gender.grid(row=2, column=1, pady=2)

frame_buttons = ttk.Frame(root, padding="10")
frame_buttons.grid(row=1, column=0, padx=10, pady=10)

button_add = ttk.Button(frame_buttons, text="Add Student", command=add_student)
button_add.grid(row=0, column=0, padx=5, pady=5)

button_update = ttk.Button(frame_buttons, text="Update Student", command=update_student)
button_update.grid(row=0, column=1, padx=5, pady=5)

button_delete = ttk.Button(frame_buttons, text="Delete Student", command=delete_student)
button_delete.grid(row=0, column=2, padx=5, pady=5)

button_clear = ttk.Button(frame_buttons, text="Clear Fields", command=clear_entries)
button_clear.grid(row=0, column=3, padx=5, pady=5)

frame_tree = ttk.Frame(root, padding="10")
frame_tree.grid(row=2, column=0, padx=10, pady=10)

tree = ttk.Treeview(frame_tree, columns=("ID", "Name", "Age", "Gender"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Gender", text="Gender")
tree.bind('<<TreeviewSelect>>', on_tree_select)
tree.grid(row=0, column=0, sticky="nsew")

populate_treeview()

root.mainloop()
