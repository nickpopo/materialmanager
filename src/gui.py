import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from src.database import create_connection, create_tables
from src.report import export_to_excel
from sqlite3 import Error

class MaterialManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Material Manager")

        self.conn = create_connection()
        create_tables(self.conn)

        self.current_user = None

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.create_login_interface()

    def create_login_interface(self):
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

    def create_main_interface(self):
        self.login_frame.pack_forget()

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.create_material_interface()
        self.create_report_interface()

    def create_material_interface(self):
        self.material_frame = tk.LabelFrame(self.main_frame, text="Materials")
        self.material_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self.material_frame, text="Add Material", command=self.add_material).pack(side="left", padx=5, pady=5)
        tk.Button(self.material_frame, text="Update Material", command=self.update_material).pack(side="left", padx=5, pady=5)
        tk.Button(self.material_frame, text="Delete Material", command=self.delete_material).pack(side="left", padx=5, pady=5)

        self.material_tree = ttk.Treeview(self.material_frame, columns=("name", "barcode", "quantity", "unit"), show='headings')
        self.material_tree.heading("name", text="Name")
        self.material_tree.heading("barcode", text="Barcode")
        self.material_tree.heading("quantity", text="Quantity")
        self.material_tree.heading("unit", text="Unit")

        self.material_tree.pack(fill="both", expand=True)
        self.load_materials()

    def create_report_interface(self):
        self.report_frame = tk.LabelFrame(self.main_frame, text="Reports")
        self.report_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self.report_frame, text="View Inventory Report", command=self.view_inventory_report).pack(padx=5, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()

        if user:
            self.current_user = user
            self.create_main_interface()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
        except Error as e:
            messagebox.showerror("Error", "Username already exists")

    def add_material(self):
        name = simpledialog.askstring("Input", "Material name:")
        barcode = simpledialog.askstring("Input", "Barcode:")
        quantity = simpledialog.askinteger("Input", "Quantity:")
        unit = simpledialog.askstring("Input", "Unit:")

        if name and barcode and quantity is not None and unit:
            cur = self.conn.cursor()
            try:
                cur.execute("INSERT INTO materials (name, barcode, quantity, unit) VALUES (?, ?, ?, ?)", (name, barcode, quantity, unit))
                self.conn.commit()
                self.load_materials()
            except Error as e:
                messagebox.showerror("Error", "Material already exists")

    def update_material(self):
        selected_item = self.material_tree.selection()
        if selected_item:
            material_id = self.material_tree.item(selected_item)['text']
            name = simpledialog.askstring("Input", "New material name:")
            barcode = simpledialog.askstring("Input", "New Barcode:")
            quantity = simpledialog.askinteger("Input", "New Quantity:")
            unit = simpledialog.askstring("Input", "New Unit:")

            if name and barcode and quantity is not None and unit:
                cur = self.conn.cursor()
                cur.execute("UPDATE materials SET name=?, barcode=?, quantity=?, unit=? WHERE id=?", (name, barcode, quantity, unit, material_id))
                self.conn.commit()
                self.load_materials()
        else:
            messagebox.showwarning("Warning", "Select a material to update")

    def delete_material(self):
        selected_item = self.material_tree.selection()
        if selected_item:
            material_id = self.material_tree.item(selected_item)['text']
            cur = self.conn.cursor()
            cur.execute("DELETE FROM materials WHERE id=?", (material_id,))
            self.conn.commit()
            self.load_materials()
        else:
            messagebox.showwarning("Warning", "Select a material to delete")

    def load_materials(self):
        for item in self.material_tree.get_children():
            self.material_tree.delete(item)
        
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM materials")
        rows = cur.fetchall()

        for row in rows:
            self.material_tree.insert("", "end", text=row[0], values=row[1:])

    def view_inventory_report(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM materials")
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("Inventory Report", "No materials found.")
            return

        report_window = tk.Toplevel(self.root)
        report_window.title("Inventory Report")

        text = tk.Text(report_window, wrap='word', height=15, width=50)
        text.pack(padx=10, pady=10)

        text.insert('1.0', "ID\tName\tBarcode\tQuantity\tUnit\n")
        text.insert('end', "-"*60 + "\n")

        for row in rows:
            text.insert('end', f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n")

        text.config(state='disabled')

        tk.Button(report_window, text="Export to Excel", command=lambda: export_to_excel(self.conn)).pack(padx=5, pady=5)

    