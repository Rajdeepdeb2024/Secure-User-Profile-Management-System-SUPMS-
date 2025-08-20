import tkinter as tk
from tkinter import ttk, messagebox
import re
import mysql.connector

# -------------------- DATABASE CONNECTION --------------------
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="67808033",
    database="Python_Project"
)
cur_obj = conn_obj.cursor()

# -------------------- BACKEND FUNCTIONS --------------------
def strong_password(password):
    return (
        len(password) >= 6 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[\W_]', password)
    )

def strong_userid(user_id):
    return (
        len(user_id) >= 3 and
        re.search(r'[A-Z]', user_id) and
        re.search(r'[0-9]', user_id)
    )

def data_entry_sql(full_name, address, phone_number, user_id, password):
    sql = "INSERT INTO cust_details (full_name,address,phone_number,user_id,password) VALUES (%s, %s, %s, %s, %s)"
    try:
        cur_obj.execute(sql, (full_name, address, phone_number, user_id, password))
        conn_obj.commit()
        return True
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return False

def data_retrieve(user_id):
    query = "SELECT * FROM cust_details WHERE user_id=%s"
    try:
        cur_obj.execute(query, (user_id,))
        return cur_obj.fetchone()
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return None

def data_retrieve_by_phone_and_id(phone_number, cust_id):
    query = "SELECT * FROM cust_details WHERE phone_number=%s AND cust_id=%s"
    try:
        cur_obj.execute(query, (phone_number, cust_id))
        return cur_obj.fetchone()
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return None

def update_user_details(cust_id, name, address, phone, password):
    qry = "UPDATE cust_details SET full_name=%s, address=%s, phone_number=%s, password=%s WHERE cust_id=%s"
    try:
        cur_obj.execute(qry, (name, address, phone, password, cust_id))
        conn_obj.commit()
        return True
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return False

def delete_user(user_id):
    try:
        cur_obj.execute("DELETE FROM cust_details WHERE user_id=%s", (user_id,))
        conn_obj.commit()
        return True
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return False

# -------------------- FRONTEND CLASSES --------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Customer Management System")
        self.geometry("650x450")
        self.configure(bg="#f0f4f7")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, LoginPage, RegisterPage, ProfileViewPage, UpdateProfilePage, DeleteAccountPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Customer Management System", font=("Arial", 20, "bold")).pack(pady=20)

        ttk.Button(self, text="Login", command=lambda: parent.show_frame(LoginPage)).pack(pady=5)
        ttk.Button(self, text="Register", command=lambda: parent.show_frame(RegisterPage)).pack(pady=5)
        ttk.Button(self, text="Profile View", command=lambda: parent.show_frame(ProfileViewPage)).pack(pady=5)
        ttk.Button(self, text="Update Profile", command=lambda: parent.show_frame(UpdateProfilePage)).pack(pady=5)
        ttk.Button(self, text="Delete Account", command=lambda: parent.show_frame(DeleteAccountPage)).pack(pady=5)
        ttk.Button(self, text="Exit", command=parent.destroy).pack(pady=10)

class LoginPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Login", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="User ID:").grid(row=1, column=0, sticky="e", pady=5)
        self.user_id_entry = ttk.Entry(self)
        self.user_id_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Button(self, text="Login", command=self.login_user).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: parent.show_frame(MainMenu)).grid(row=4, column=0, columnspan=2)

    def login_user(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        user_details = data_retrieve(user_id)
        if user_details and user_details[-1] == password:
            messagebox.showinfo("Success", "Login Successful!")
        else:
            messagebox.showerror("Error", "Invalid credentials!")

class RegisterPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Register", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Full Name", "Address", "Phone Number", "User ID", "Password"]
        self.entries = {}
        for idx, label in enumerate(labels, start=1):
            ttk.Label(self, text=label + ":").grid(row=idx, column=0, sticky="e", pady=5)
            entry = ttk.Entry(self, show="*" if label == "Password" else "")
            entry.grid(row=idx, column=1, pady=5)
            self.entries[label] = entry

        ttk.Button(self, text="Register", command=self.register_user).grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: parent.show_frame(MainMenu)).grid(row=len(labels)+2, column=0, columnspan=2)

    def register_user(self):
        full_name = self.entries["Full Name"].get().upper()
        address = self.entries["Address"].get()
        phone_number = self.entries["Phone Number"].get()
        user_id = self.entries["User ID"].get()
        password = self.entries["Password"].get()

        if not (phone_number.isdigit() and len(phone_number) == 10):
            messagebox.showerror("Error", "Invalid phone number!")
            return
        if not strong_userid(user_id):
            messagebox.showerror("Error", "User ID must include uppercase and digit!")
            return
        if not strong_password(password):
            messagebox.showerror("Error", "Password must include uppercase, lowercase, digit, and special character!")
            return

        if data_entry_sql(full_name, address, phone_number, user_id, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.master.show_frame(LoginPage)

class ProfileViewPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Profile View", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Phone Number:").grid(row=1, column=0, sticky="e", pady=5)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Customer ID:").grid(row=2, column=0, sticky="e", pady=5)
        self.cust_id_entry = ttk.Entry(self)
        self.cust_id_entry.grid(row=2, column=1, pady=5)

        ttk.Button(self, text="View Profile", command=self.view_profile).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: parent.show_frame(MainMenu)).grid(row=4, column=0, columnspan=2)

    def view_profile(self):
        phone = self.phone_entry.get()
        cust_id = self.cust_id_entry.get()
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "Invalid phone number!")
            return
        if not cust_id.isdigit():
            messagebox.showerror("Error", "Customer ID must be digits!")
            return
        user = data_retrieve_by_phone_and_id(phone, cust_id)
        if user:
            messagebox.showinfo("Profile", f"Name: {user[1]}\nAddress: {user[2]}\nPhone: {user[3]}\nUser ID: {user[4]}")
        else:
            messagebox.showerror("Error", "No data found!")

class UpdateProfilePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Update Profile", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        self.user_id_entry = ttk.Entry(self)
        self.pass_entry = ttk.Entry(self, show="*")
        ttk.Label(self, text="User ID:").grid(row=1, column=0, sticky="e", pady=5)
        self.user_id_entry.grid(row=1, column=1, pady=5)
        ttk.Label(self, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
        self.pass_entry.grid(row=2, column=1, pady=5)

        self.name_entry = ttk.Entry(self)
        self.addr_entry = ttk.Entry(self)
        self.phone_entry = ttk.Entry(self)
        self.newpass_entry = ttk.Entry(self, show="*")

        labels = ["New Full Name", "New Address", "New Phone", "New Password"]
        entries = [self.name_entry, self.addr_entry, self.phone_entry, self.newpass_entry]
        for idx, (lbl, ent) in enumerate(zip(labels, entries), start=3):
            ttk.Label(self, text=lbl + ":").grid(row=idx, column=0, sticky="e", pady=5)
            ent.grid(row=idx, column=1, pady=5)

        ttk.Button(self, text="Update", command=self.update_profile).grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: parent.show_frame(MainMenu)).grid(row=8, column=0, columnspan=2)

    def update_profile(self):
        user_id = self.user_id_entry.get()
        password = self.pass_entry.get()
        user_details = data_retrieve(user_id)
        if not user_details or user_details[-1] != password:
            messagebox.showerror("Error", "Invalid login!")
            return
        cust_id = user_details[0]
        new_name = self.name_entry.get().upper() or user_details[1]
        new_addr = self.addr_entry.get() or user_details[2]
        new_phone = self.phone_entry.get() or user_details[3]
        if new_phone and (not new_phone.isdigit() or len(new_phone) != 10):
            messagebox.showerror("Error", "Invalid phone number!")
            return
        new_pass = self.newpass_entry.get() or user_details[-1]
        if new_pass != user_details[-1] and not strong_password(new_pass):
            messagebox.showerror("Error", "Weak password!")
            return
        if update_user_details(cust_id, new_name, new_addr, new_phone, new_pass):
            messagebox.showinfo("Success", "Profile updated!")

class DeleteAccountPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Delete Account", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="User ID:").grid(row=1, column=0, sticky="e", pady=5)
        self.user_id_entry = ttk.Entry(self)
        self.user_id_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Button(self, text="Delete Account", command=self.delete_account).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: parent.show_frame(MainMenu)).grid(row=4, column=0, columnspan=2)

    def delete_account(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        user_details = data_retrieve(user_id)
        if not user_details or user_details[-1] != password:
            messagebox.showerror("Error", "Invalid login!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete your account?"):
            if delete_user(user_id):
                messagebox.showinfo("Deleted", "Account deleted successfully!")
                self.master.show_frame(MainMenu)

# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
    conn_obj.close()
