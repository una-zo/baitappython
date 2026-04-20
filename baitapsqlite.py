import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ================= DATABASE =================
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    major TEXT,
    gpa REAL
)
""")
conn.commit()

# ================= FUNCTIONS =================
def refresh(data=None):
    for row in tree.get_children():
        tree.delete(row)

    if data is None:
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()

    for row in data:
        tree.insert("", tk.END, values=row)


def show_all():
    refresh()


def show_high_gpa():
    cursor.execute("SELECT * FROM students WHERE gpa > 3.0")
    refresh(cursor.fetchall())


def validate_input():
    name = entry_name.get().strip()
    major = entry_major.get().strip()

    try:
        gpa = float(entry_gpa.get().strip())
    except:
        messagebox.showerror("Error", "GPA phải là số")
        return None

    if not name or not major:
        messagebox.showerror("Error", "Không được để trống Name hoặc Major")
        return None

    return name, major, gpa


def add_student():
    data = validate_input()
    if not data:
        return

    cursor.execute(
        "INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)",
        data
    )
    conn.commit()
    show_all()


def delete_low_gpa():
    cursor.execute("DELETE FROM students WHERE gpa < 2.0")
    conn.commit()
    show_all()
    messagebox.showinfo("Info", "Đã xóa sinh viên GPA < 2.0")


def get_selected_id():
    selected = tree.focus()
    if not selected:
        return None
    return tree.item(selected)["values"][0]


def update_gpa():
    sid = get_selected_id()
    if sid is None:
        messagebox.showerror("Error", "Chọn sinh viên trước")
        return

    try:
        new_gpa = float(entry_gpa.get())
    except:
        messagebox.showerror("Error", "GPA không hợp lệ")
        return

    cursor.execute("UPDATE students SET gpa=? WHERE id=?", (new_gpa, sid))
    conn.commit()
    show_all()


def on_select(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected)["values"]

    entry_name.delete(0, tk.END)
    entry_major.delete(0, tk.END)
    entry_gpa.delete(0, tk.END)

    entry_name.insert(0, values[1])
    entry_major.insert(0, values[2])
    entry_gpa.insert(0, values[3])

# ================= UI =================
root = tk.Tk()
root.title("Phan mem quan ly hoc sinh")
root.geometry("700x500")
root.config(bg="#f4f6f8")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", padding=6)
style.configure("Treeview", rowheight=25)

# ===== Input Frame =====
input_frame = tk.Frame(root, bg="#f4f6f8")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Name", bg="#f4f6f8").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(input_frame, width=25)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Major", bg="#f4f6f8").grid(row=1, column=0, padx=5, pady=5)
entry_major = tk.Entry(input_frame, width=25)
entry_major.grid(row=1, column=1, padx=5)

tk.Label(input_frame, text="GPA", bg="#f4f6f8").grid(row=2, column=0, padx=5, pady=5)
entry_gpa = tk.Entry(input_frame, width=25)
entry_gpa.grid(row=2, column=1, padx=5)

# ===== Buttons =====
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Add", command=add_student).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Show All", command=show_all).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="GPA > 3.0", command=show_high_gpa).grid(row=0, column=2, padx=5)
ttk.Button(btn_frame, text="Update GPA", command=update_gpa).grid(row=0, column=3, padx=5)
ttk.Button(btn_frame, text="Delete GPA < 2.0", command=delete_low_gpa).grid(row=0, column=4, padx=5)

# ===== Table =====
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

cols = ("ID", "Name", "Major", "GPA")

tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.pack()
tree.bind("<<TreeviewSelect>>", on_select)

show_all()

root.mainloop()
conn.close()