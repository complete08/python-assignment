
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "contact_book_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def save_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    # email is optional (schema allows NULL); name and phone are required
    if not name or not phone:
        messagebox.showwarning("Missing Fields", "Name and Phone are required.")
        return

    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)",
            (name, phone, email or None),
        )
        conn.commit()
        messagebox.showinfo("Success", f"'{name}' was saved successfully.")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        view_contacts()
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to save contact:\n{e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def view_contacts():
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone, email FROM contacts ORDER BY id")
        rows = cursor.fetchall()

        contacts_text.delete("1.0", tk.END)
        header = f"{'ID':<5}{'Name':<20}{'Phone':<15}{'Email':<25}\n"
        contacts_text.insert(tk.END, header)
        contacts_text.insert(tk.END, "-" * 65 + "\n")

        if not rows:
            contacts_text.insert(tk.END, "No contacts saved yet.\n")
        else:
            for cid, name, phone, email in rows:
                contacts_text.insert(tk.END, f"{cid:<5}{name:<20}{phone:<15}{(email or ''):<25}\n")
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch contacts:\n{e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ================= UI Setup =================
root = tk.Tk()
root.title("Contact Book")
root.geometry("560x480")
root.minsize(520, 440)
root.configure(bg="#f4f6f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f4f6f8")
style.configure("TLabel", background="#f4f6f8", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), background="#f4f6f8")

ttk.Label(root, text="Contact Book", style="Header.TLabel").pack(pady=(16, 10))

form_frame = ttk.Frame(root)
form_frame.pack(pady=5, padx=20, fill="x")

ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=4)
name_entry = ttk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, pady=4, padx=10, sticky="w")

ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky="w", pady=4)
phone_entry = ttk.Entry(form_frame, width=30)
phone_entry.grid(row=1, column=1, pady=4, padx=10, sticky="w")

ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=4)
email_entry = ttk.Entry(form_frame, width=30)
email_entry.grid(row=2, column=1, pady=4, padx=10, sticky="w")

button_frame = ttk.Frame(root)
button_frame.pack(pady=14)

ttk.Button(button_frame, text="Save Contact", command=save_contact).grid(row=0, column=0, padx=6)
ttk.Button(button_frame, text="View All Contacts", command=view_contacts).grid(row=0, column=1, padx=6)

records_frame = ttk.Frame(root)
records_frame.pack(pady=10, padx=20, fill="both", expand=True)

scrollbar = ttk.Scrollbar(records_frame)
scrollbar.pack(side="right", fill="y")

contacts_text = tk.Text(
    records_frame,
    height=12,
    font=("Consolas", 10),
    yscrollcommand=scrollbar.set,
    wrap="none",
    bg="white",
    relief="solid",
    borderwidth=1,
)
contacts_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=contacts_text.yview)

view_contacts()

if __name__ == "__main__":
    root.mainloop()