

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ================= Database Configuration =================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "company_db",
}


def get_connection():
    """Open and return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


# ================= Validation Helpers =================
def validate_form(name, department, salary):
    if not name or not department or not salary:
        messagebox.showwarning("Missing Fields", "Name, Department, and Salary are all required.")
        return False
    try:
        float(salary)
    except ValueError:
        messagebox.showwarning("Invalid Salary", "Salary must be a valid number.")
        return False
    return True


def validate_id(emp_id):
    if not emp_id.isdigit():
        messagebox.showwarning("Invalid ID", "ID must be a positive whole number.")
        return False
    return True


def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)


def render_rows(rows, empty_message="No records found."):
    records_text.delete("1.0", tk.END)
    header = f"{'ID':<6}{'Name':<22}{'Department':<20}{'Salary':>12}\n"
    records_text.insert(tk.END, header)
    records_text.insert(tk.END, "-" * 60 + "\n")
    if not rows:
        records_text.insert(tk.END, empty_message + "\n")
        return
    for emp_id, name, department, salary in rows:
        records_text.insert(tk.END, f"{emp_id:<6}{name:<22}{department:<20}{salary:>12.2f}\n")


# ================= Core CRUD Functions =================
def add_employee():
    name = name_entry.get().strip()
    department = department_entry.get().strip()
    salary = salary_entry.get().strip()

    if not validate_form(name, department, salary):
        return

    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)",
            (name, department, float(salary)),
        )
        conn.commit()
        messagebox.showinfo("Success", f"'{name}' was added successfully.")
        clear_fields()
        view_employees()
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to add employee:\n{e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_employee():
    emp_id = id_entry.get().strip()
    name = name_entry.get().strip()
    department = department_entry.get().strip()
    salary = salary_entry.get().strip()

    if not emp_id:
        messagebox.showwarning("Missing ID", "Enter the ID of the employee you want to update.")
        return
    if not validate_id(emp_id):
        return
    if not validate_form(name, department, salary):
        return

    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employees SET name=%s, department=%s, salary=%s WHERE id=%s",
            (name, department, float(salary), emp_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Not Found", f"No employee exists with ID {emp_id}.")
        else:
            messagebox.showinfo("Success", f"Employee {emp_id} updated successfully.")
            clear_fields()
            view_employees()
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to update employee:\n{e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_employee():
    emp_id = id_entry.get().strip()

    if not emp_id:
        messagebox.showwarning("Missing ID", "Enter the ID of the employee you want to delete.")
        return
    if not validate_id(emp_id):
        return

    if not messagebox.askyesno("Confirm Delete", f"Delete employee with ID {emp_id}? This cannot be undone."):
        return

    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Not Found", f"No employee exists with ID {emp_id}.")
        else:
            messagebox.showinfo("Success", f"Employee {emp_id} deleted successfully.")
            clear_fields()
            view_employees()
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to delete employee:\n{e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def view_employees():
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, department, salary FROM employees ORDER BY id")
        rows = cursor.fetchall()
        render_rows(rows, empty_message="No employees in the database yet.")
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch employees:\n{e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def search_employee():
    """Bonus: search employees by (partial, case-insensitive) name."""
    term = search_entry.get().strip()
    if not term:
        messagebox.showwarning("Missing Search Term", "Enter a name to search for.")
        return

    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, department, salary FROM employees WHERE name LIKE %s ORDER BY id",
            (f"%{term}%",),
        )
        rows = cursor.fetchall()
        render_rows(rows, empty_message=f"No employees found matching '{term}'.")
    except Error as e:
        messagebox.showerror("Database Error", f"Search failed:\n{e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ================= UI Setup =================
root = tk.Tk()
root.title("Employee Management System")
root.geometry("720x640")
root.minsize(680, 560)
root.configure(bg="#f4f6f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f4f6f8")
style.configure("TLabel", background="#f4f6f8", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#f4f6f8")

ttk.Label(root, text="Employee Management System", style="Header.TLabel").pack(pady=(18, 12))

# --- Form ---
form_frame = ttk.Frame(root)
form_frame.pack(pady=5, padx=20, fill="x")

ttk.Label(form_frame, text="ID (Update / Delete):").grid(row=0, column=0, sticky="w", pady=4)
id_entry = ttk.Entry(form_frame, width=32)
id_entry.grid(row=0, column=1, pady=4, padx=10, sticky="w")

ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky="w", pady=4)
name_entry = ttk.Entry(form_frame, width=32)
name_entry.grid(row=1, column=1, pady=4, padx=10, sticky="w")

ttk.Label(form_frame, text="Department:").grid(row=2, column=0, sticky="w", pady=4)
department_entry = ttk.Entry(form_frame, width=32)
department_entry.grid(row=2, column=1, pady=4, padx=10, sticky="w")

ttk.Label(form_frame, text="Salary:").grid(row=3, column=0, sticky="w", pady=4)
salary_entry = ttk.Entry(form_frame, width=32)
salary_entry.grid(row=3, column=1, pady=4, padx=10, sticky="w")

# --- Action Buttons ---
button_frame = ttk.Frame(root)
button_frame.pack(pady=15)

ttk.Button(button_frame, text="Add Employee", command=add_employee).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Update Employee", command=update_employee).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Delete Employee", command=delete_employee).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="View All", command=view_employees).grid(row=0, column=3, padx=5)
ttk.Button(button_frame, text="Clear Form", command=clear_fields).grid(row=0, column=4, padx=5)

# --- Bonus: Search by Name ---
search_frame = ttk.Frame(root)
search_frame.pack(pady=(0, 12))

ttk.Label(search_frame, text="Search by Name:").grid(row=0, column=0, padx=(0, 8))
search_entry = ttk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=(0, 8))
ttk.Button(search_frame, text="Search", command=search_employee).grid(row=0, column=2)

# --- Records Display ---
records_frame = ttk.Frame(root)
records_frame.pack(pady=10, padx=20, fill="both", expand=True)

scrollbar = ttk.Scrollbar(records_frame)
scrollbar.pack(side="right", fill="y")

records_text = tk.Text(
    records_frame,
    height=15,
    font=("Consolas", 10),
    yscrollcommand=scrollbar.set,
    wrap="none",
    bg="white",
    relief="solid",
    borderwidth=1,
)
records_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=records_text.yview)

# Load existing records on startup
view_employees()

if __name__ == "__main__":
    root.mainloop()