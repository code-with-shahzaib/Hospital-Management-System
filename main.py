import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, time, timedelta
from database import *
from welcome_screen import *
import os
from tkinter import simpledialog

class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1100x750")
        self.root.config(bg="#f4f4f9")
        
        # Color scheme
        self.colors = {
            "primary": "#4CAF50",
            "secondary": "#2196F3",
            "accent": "#FFC107",
            "dark": "#333333",
            "light": "#f4f4f9",
            "danger": "#F44336",
            "purple": "#9C27B0"
        }
        
        # Fonts
        self.font_large = ("Helvetica", 18)
        self.font_medium = ("Helvetica", 14)
        self.font_small = ("Helvetica", 12)
        
        self.current_frame = None
        self.show_home_page()

    def clear_frame(self):
        """Clear the current frame"""
        if self.current_frame:
            self.current_frame.destroy()

    def create_nav_button(self, frame):
        """Create a back to home button"""
        btn_home = tk.Button(
            frame,
            text="← Home",
            command=self.show_home_page,
            font=self.font_small,
            bg=self.colors["secondary"],
            fg="white",
            relief="flat",
            padx=10,
            pady=5
        )
        btn_home.pack(anchor="nw", padx=10, pady=10)

    def show_home_page(self):
        """Show the main home page"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=self.colors["light"])
        self.current_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        header_frame.pack(pady=50)
        
        tk.Label(
            header_frame,
            text="Hospital Management System",
            font=("Helvetica", 28, "bold"),
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack()
        
        tk.Label(
            header_frame,
            text="Main Menu",
            font=self.font_medium,
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack(pady=10)
        
        # Button Grid
        button_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        button_frame.pack(pady=20)
        
        buttons = [
            ("Patient Management", self.show_patient_management, self.colors["primary"]),
            ("Doctor Management", self.show_doctor_management, self.colors["secondary"]),
            ("Appointment Scheduling", self.show_appointment_scheduling, self.colors["accent"]),
            ("View All Records", self.show_all_records, self.colors["purple"]),
            ("Exit System", self.root.quit, self.colors["danger"])
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=self.font_medium,
                bg=color,
                fg="white",
                width=25,
                height=2,
                relief="flat"
            )
            btn.grid(row=i//2, column=i%2, padx=15, pady=15)
        
        # Recent Activity Section
        activity_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        activity_frame.pack(fill="x", padx=50, pady=20)
        
        tk.Label(
            activity_frame,
            text="Recent Activity",
            font=self.font_medium,
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack(anchor="w")
        
        activity_tree = ttk.Treeview(
            activity_frame,
            columns=("Type", "Description", "Time"),
            show="headings",
            height=5
        )
        activity_tree.heading("Type", text="Type")
        activity_tree.heading("Description", text="Description")
        activity_tree.heading("Time", text="Time")
        
        activity_tree.column("Type", width=100)
        activity_tree.column("Description", width=300)
        activity_tree.column("Time", width=150)
        
        for activity in get_recent_activity():
            activity_tree.insert("", "end", values=(
                activity['type'],
                activity.get('name', activity.get('description', '')),
                activity['created_at']
            ))
        
        activity_tree.pack(fill="x")
        
        # Footer
        footer_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        footer_frame.pack(side="bottom", fill="x", pady=20)
        
        tk.Label(
            footer_frame,
            text=f"Logged in as: Operator | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            font=self.font_small,
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack()

    def show_patient_management(self):
        """Show patient management page"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=self.colors["light"])
        self.current_frame.pack(fill="both", expand=True)
        
        # Navigation
        self.create_nav_button(self.current_frame)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(
            header_frame,
            text="Patient Management",
            font=self.font_large,
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack(side="left", padx=20)
        
        # Action buttons
        action_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        action_frame.pack(fill="x", pady=10)
        
        btn_add = tk.Button(
            action_frame,
            text="Add New Patient",
            command=self.open_patient_form,
            font=self.font_small,
            bg=self.colors["primary"],
            fg="white",
            relief="flat"
        )
        btn_add.pack(side="left", padx=10)
        
        btn_refresh = tk.Button(
            action_frame,
            text="Refresh List",
            command=lambda: self.show_patient_list(patient_tree),
            font=self.font_small,
            bg=self.colors["secondary"],
            fg="white",
            relief="flat"
        )
        btn_refresh.pack(side="left", padx=10)
        
        # Search frame
        search_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        search_frame.pack(fill="x", pady=10)
        
        self.patient_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.patient_search_var,
            font=self.font_small,
            width=40
        )
        search_entry.pack(side="left", padx=10)
        
        btn_search = tk.Button(
            search_frame,
            text="Search",
            command=lambda: self.show_patient_list(patient_tree, self.patient_search_var.get()),
            font=self.font_small,
            bg=self.colors["accent"],
            fg="white",
            relief="flat"
        )
        btn_search.pack(side="left", padx=5)
        
        btn_search_id = tk.Button(
            search_frame,
            text="Search by ID",
            command=lambda: self.show_patient_list(patient_tree, self.patient_search_var.get(), True),
            font=self.font_small,
            bg=self.colors["purple"],
            fg="white",
            relief="flat"
        )
        btn_search_id.pack(side="left", padx=5)
        
        # Patient list
        list_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        patient_tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Name", "Age", "Gender", "Diagnosis", "Admission Date", "Created At"),
            show="headings"
        )
        
        # Configure columns
        patient_tree.heading("ID", text="ID")
        patient_tree.heading("Name", text="Name")
        patient_tree.heading("Age", text="Age")
        patient_tree.heading("Gender", text="Gender")
        patient_tree.heading("Diagnosis", text="Diagnosis")
        patient_tree.heading("Admission Date", text="Admission Date")
        patient_tree.heading("Created At", text="Created At")
        
        patient_tree.column("ID", width=50, anchor="center")
        patient_tree.column("Name", width=150)
        patient_tree.column("Age", width=50, anchor="center")
        patient_tree.column("Gender", width=80, anchor="center")
        patient_tree.column("Diagnosis", width=200)
        patient_tree.column("Admission Date", width=100, anchor="center")
        patient_tree.column("Created At", width=150, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=patient_tree.yview)
        patient_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        patient_tree.pack(side="left", fill="both", expand=True)
        
        # Show initial patient list
        self.show_patient_list(patient_tree)
        
        # Action buttons for selected patient
        action_btn_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        action_btn_frame.pack(fill="x", pady=10)
        
        btn_edit = tk.Button(
            action_btn_frame,
            text="Edit Selected",
            command=lambda: self.edit_patient(patient_tree),
            font=self.font_small,
            bg=self.colors["accent"],
            fg="white",
            relief="flat"
        )
        btn_edit.pack(side="left", padx=10)
        
        btn_delete = tk.Button(
            action_btn_frame,
            text="Delete Selected",
            command=lambda: self.delete_patient(patient_tree),
            font=self.font_small,
            bg=self.colors["danger"],
            fg="white",
            relief="flat"
        )
        btn_delete.pack(side="left", padx=10)
        
        btn_print = tk.Button(
            action_btn_frame,
            text="Print Receipt",
            command=lambda: self.print_patient_receipt(patient_tree),
            font=self.font_small,
            bg=self.colors["purple"],
            fg="white",
            relief="flat"
        )
        btn_print.pack(side="left", padx=10)

    def show_patient_list(self, tree, search_term=None, search_by_id=False):
        """Populate patient treeview"""
        for item in tree.get_children():
            tree.delete(item)
            
        patients = get_patients(search_term, search_by_id)
        for patient in patients:
            tree.insert("", "end", values=(
                patient['id'],
                patient['name'],
                patient['age'],
                patient['gender'],
                patient['diagnosis'],
                patient['admission_date'],
                patient['created_at']
            ))

    def open_patient_form(self, patient_id=None):
        """Open patient form for adding/editing"""
        form = tk.Toplevel(self.root)
        form.title("Add Patient" if not patient_id else "Edit Patient")
        form.geometry("400x400")
        form.config(bg=self.colors["light"])
        
        # Form fields
        fields = [
            ("Name:", "name", tk.Entry(form, font=self.font_small)),
            ("Age:", "age", tk.Entry(form, font=self.font_small)),
            ("Gender:", "gender", ttk.Combobox(form, values=["Male", "Female", "Other"], state="readonly", font=self.font_small)),
            ("Diagnosis:", "diagnosis", tk.Entry(form, font=self.font_small))
        ]
        
        for i, (label, _, widget) in enumerate(fields):
            tk.Label(
                form,
                text=label,
                bg=self.colors["light"],
                fg=self.colors["dark"],
                font=self.font_small
            ).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        
        # Pre-fill for edit
        if patient_id:
            patient = next(p for p in get_patients() if p['id'] == patient_id)
            fields[0][2].insert(0, patient['name'])
            fields[1][2].insert(0, patient['age'])
            fields[2][2].set(patient['gender'])
            fields[3][2].insert(0, patient['diagnosis'])
        
        # Submit button
        def submit():
            try:
                data = {
                    'name': fields[0][2].get().strip(),
                    'age': int(fields[1][2].get()),
                    'gender': fields[2][2].get(),
                    'diagnosis': fields[3][2].get().strip()
                }
                
                if not data['name']:
                    raise ValueError("Name is required")
                if data['age'] <= 0:
                    raise ValueError("Age must be positive")
                
                if patient_id:
                    update_patient(patient_id, **data)
                    messagebox.showinfo("Success", "Patient updated successfully!")
                else:
                    insert_patient(**data)
                    messagebox.showinfo("Success", "Patient added successfully!")
                
                form.destroy()
                self.show_patient_management()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(
            form,
            text="Submit",
            command=submit,
            font=self.font_small,
            bg=self.colors["primary"],
            fg="white",
            relief="flat"
        ).grid(row=len(fields), column=1, pady=10, sticky="e")

    def edit_patient(self, tree):
        """Edit selected patient"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to edit")
            return
        
        patient_id = tree.item(selected[0])['values'][0]
        self.open_patient_form(patient_id)

    def delete_patient(self, tree):
        """Delete selected patient"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        
        patient_id = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
            if delete_patient(patient_id):
                messagebox.showinfo("Success", "Patient deleted successfully")
                self.show_patient_management()
            else:
                messagebox.showerror("Error", "Failed to delete patient")

    def print_patient_receipt(self, tree):
        """Print receipt for selected patient"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to print receipt")
            return
        
        patient_id = tree.item(selected[0])['values'][0]
        patient = get_patient_by_id(patient_id)
        appointments = get_patient_appointments(patient_id)
        
        # Create receipt content
        receipt = f"""
        HOSPITAL MANAGEMENT SYSTEM
        --------------------------
        PATIENT RECEIPT
        --------------------------
        Patient ID: {patient['id']}
        Name: {patient['name']}
        Age: {patient['age']}
        Gender: {patient['gender']}
        Admission Date: {patient['admission_date']}
        Diagnosis: {patient['diagnosis']}
        
        APPOINTMENTS:
        """
        
        for appt in appointments:
            receipt += f"""
            - Appointment with Dr. {appt['doctor_name']} ({appt['specialization']})
              Date: {appt['appointment_date']}
              Time: {appt['start_time']} - {appt['end_time']}
              Notes: {appt['notes']}
            """
        
        receipt += """
        --------------------------
        Thank you for choosing our hospital!
        """
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=f"patient_{patient_id}_receipt.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(receipt)
                messagebox.showinfo("Success", f"Receipt saved successfully at:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save receipt:\n{str(e)}")

    def show_doctor_management(self):
        """Show doctor management page"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=self.colors["light"])
        self.current_frame.pack(fill="both", expand=True)
        
        # Navigation
        self.create_nav_button(self.current_frame)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(
            header_frame,
            text="Doctor Management",
            font=self.font_large,
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack(side="left", padx=20)
        
        # Action buttons
        action_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        action_frame.pack(fill="x", pady=10)
        
        btn_add = tk.Button(
            action_frame,
            text="Add New Doctor",
            command=self.open_doctor_form,
            font=self.font_small,
            bg=self.colors["primary"],
            fg="white",
            relief="flat"
        )
        btn_add.pack(side="left", padx=10)
        
        btn_refresh = tk.Button(
            action_frame,
            text="Refresh List",
            command=lambda: self.show_doctor_list(doctor_tree),
            font=self.font_small,
            bg=self.colors["secondary"],
            fg="white",
            relief="flat"
        )
        btn_refresh.pack(side="left", padx=10)
        
        # Search frame
        search_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        search_frame.pack(fill="x", pady=10)
        
        self.doctor_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.doctor_search_var,
            font=self.font_small,
            width=40
        )
        search_entry.pack(side="left", padx=10)
        
        btn_search = tk.Button(
            search_frame,
            text="Search",
            command=lambda: self.show_doctor_list(doctor_tree, self.doctor_search_var.get()),
            font=self.font_small,
            bg=self.colors["accent"],
            fg="white",
            relief="flat"
        )
        btn_search.pack(side="left", padx=5)
        
        btn_search_id = tk.Button(
            search_frame,
            text="Search by ID",
            command=lambda: self.show_doctor_list(doctor_tree, self.doctor_search_var.get(), True),
            font=self.font_small,
            bg=self.colors["purple"],
            fg="white",
            relief="flat"
        )
        btn_search_id.pack(side="left", padx=5)
        
        # Doctor list
        list_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        doctor_tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Name", "Specialization", "Experience", "Gender"),
            show="headings"
        )
        
        # Configure columns
        doctor_tree.heading("ID", text="ID")
        doctor_tree.heading("Name", text="Name")
        doctor_tree.heading("Specialization", text="Specialization")
        doctor_tree.heading("Experience", text="Experience (years)")
        doctor_tree.heading("Gender", text="Gender")
        
        doctor_tree.column("ID", width=50, anchor="center")
        doctor_tree.column("Name", width=150)
        doctor_tree.column("Specialization", width=150)
        doctor_tree.column("Experience", width=100, anchor="center")
        doctor_tree.column("Gender", width=80, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=doctor_tree.yview)
        doctor_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        doctor_tree.pack(side="left", fill="both", expand=True)
        
        # Show initial doctor list
        self.show_doctor_list(doctor_tree)
        
        # Action buttons for selected doctor
        action_btn_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        action_btn_frame.pack(fill="x", pady=10)
        
        btn_edit = tk.Button(
            action_btn_frame,
            text="Edit Selected",
            command=lambda: self.edit_doctor(doctor_tree),
            font=self.font_small,
            bg=self.colors["accent"],
            fg="white",
            relief="flat"
        )
        btn_edit.pack(side="left", padx=10)
        
        btn_delete = tk.Button(
            action_btn_frame,
            text="Delete Selected",
            command=lambda: self.delete_doctor(doctor_tree),
            font=self.font_small,
            bg=self.colors["danger"],
            fg="white",
            relief="flat"
        )
        btn_delete.pack(side="left", padx=10)

    def show_doctor_list(self, tree, search_term=None, search_by_id=False):
        """Populate doctor treeview"""
        for item in tree.get_children():
            tree.delete(item)
            
        doctors = get_doctors(search_term, search_by_id)
        for doctor in doctors:
            tree.insert("", "end", values=(
                doctor['id'],
                doctor['name'],
                doctor['specialization'],
                doctor['experience'],
                doctor['gender']
            ))

    def open_doctor_form(self, doctor_id=None):
        """Open doctor form for adding/editing"""
        form = tk.Toplevel(self.root)
        form.title("Add Doctor" if not doctor_id else "Edit Doctor")
        form.geometry("400x400")
        form.config(bg=self.colors["light"])
        
        # Form fields
        fields = [
            ("Name:", "name", tk.Entry(form, font=self.font_small)),
            ("Specialization:", "specialization", tk.Entry(form, font=self.font_small)),
            ("Experience (years):", "experience", tk.Entry(form, font=self.font_small)),
            ("Gender:", "gender", ttk.Combobox(form, values=["Male", "Female", "Other"], state="readonly", font=self.font_small))
        ]
        
        for i, (label, _, widget) in enumerate(fields):
            tk.Label(
                form,
                text=label,
                bg=self.colors["light"],
                fg=self.colors["dark"],
                font=self.font_small
            ).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        
        # Pre-fill for edit
        if doctor_id:
            doctor = next(d for d in get_doctors() if d['id'] == doctor_id)
            fields[0][2].insert(0, doctor['name'])
            fields[1][2].insert(0, doctor['specialization'])
            fields[2][2].insert(0, doctor['experience'])
            fields[3][2].set(doctor['gender'])
        
        # Submit button
        def submit():
            try:
                data = {
                    'name': fields[0][2].get().strip(),
                    'specialization': fields[1][2].get().strip(),
                    'experience': int(fields[2][2].get()),
                    'gender': fields[3][2].get()
                }
                
                if not data['name'] or not data['specialization']:
                    raise ValueError("Name and specialization are required")
                if data['experience'] < 0:
                    raise ValueError("Experience cannot be negative")
                
                if doctor_id:
                    update_doctor(doctor_id, **data)
                    messagebox.showinfo("Success", "Doctor updated successfully!")
                else:
                    insert_doctor(**data)
                    messagebox.showinfo("Success", "Doctor added successfully!")
                
                form.destroy()
                self.show_doctor_management()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(
            form,
            text="Submit",
            command=submit,
            font=self.font_small,
            bg=self.colors["primary"],
            fg="white",
            relief="flat"
        ).grid(row=len(fields), column=1, pady=10, sticky="e")

    def edit_doctor(self, tree):
        """Edit selected doctor"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a doctor to edit")
            return
        
        doctor_id = tree.item(selected[0])['values'][0]
        self.open_doctor_form(doctor_id)

    def delete_doctor(self, tree):
        """Delete selected doctor"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        
        doctor_id = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor?"):
            if delete_doctor(doctor_id):
                messagebox.showinfo("Success", "Doctor deleted successfully")
                self.show_doctor_management()
            else:
                messagebox.showerror("Error", "Failed to delete doctor")

    def show_appointment_scheduling(self):
        """Show appointment scheduling page"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=self.colors["light"])
        self.current_frame.pack(fill="both", expand=True)
        
        # Navigation
        self.create_nav_button(self.current_frame)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(
            header_frame,
            text="Appointment Scheduling",
            font=self.font_large,
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack(side="left", padx=20)
        
        # Action buttons
        action_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        action_frame.pack(fill="x", pady=10)
        
        btn_new = tk.Button(
            action_frame,
            text="Schedule New Appointment",
            command=self.open_appointment_form,
            font=self.font_small,
            bg=self.colors["primary"],
            fg="white",
            relief="flat"
        )
        btn_new.pack(side="left", padx=10)
        
        btn_refresh = tk.Button(
            action_frame,
            text="Refresh List",
            command=lambda: self.show_appointment_list(appointment_tree),
            font=self.font_small,
            bg=self.colors["secondary"],
            fg="white",
            relief="flat"
        )
        btn_refresh.pack(side="left", padx=10)
        
        # Filter frame
        filter_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        filter_frame.pack(fill="x", pady=10)
        
        tk.Label(
            filter_frame,
            text="Filter by Date:",
            bg=self.colors["light"],
            fg=self.colors["dark"],
            font=self.font_small
        ).pack(side="left", padx=10)
        
        self.appointment_date_var = tk.StringVar()
        self.appointment_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        date_entry = tk.Entry(
            filter_frame,
            textvariable=self.appointment_date_var,
            font=self.font_small,
            width=12
        )
        date_entry.pack(side="left", padx=5)
        
        btn_filter = tk.Button(
            filter_frame,
            text="Apply Filter",
            command=lambda: self.show_appointment_list(appointment_tree, self.appointment_date_var.get()),
            font=self.font_small,
            bg=self.colors["accent"],
            fg="white",
            relief="flat"
        )
        btn_filter.pack(side="left", padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        search_frame.pack(fill="x", pady=10)
        
        self.appointment_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.appointment_search_var,
            font=self.font_small,
            width=40
        )
        search_entry.pack(side="left", padx=10)
        
        btn_search = tk.Button(
            search_frame,
            text="Search",
            command=lambda: self.show_appointment_list(appointment_tree, search_term=self.appointment_search_var.get()),
            font=self.font_small,
            bg=self.colors["accent"],
            fg="white",
            relief="flat"
        )
        btn_search.pack(side="left", padx=5)
        
        btn_search_id = tk.Button(
            search_frame,
            text="Search by ID",
            command=lambda: self.show_appointment_list(appointment_tree, search_term=self.appointment_search_var.get(), search_by_id=True),
            font=self.font_small,
            bg=self.colors["purple"],
            fg="white",
            relief="flat"
        )
        btn_search_id.pack(side="left", padx=5)
        
        # Appointment list
        list_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        appointment_tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Patient", "Doctor", "Date", "Time", "Notes"),
            show="headings"
        )
        
        # Configure columns
        appointment_tree.heading("ID", text="ID")
        appointment_tree.heading("Patient", text="Patient")
        appointment_tree.heading("Doctor", text="Doctor")
        appointment_tree.heading("Date", text="Date")
        appointment_tree.heading("Time", text="Time")
        appointment_tree.heading("Notes", text="Notes")
        
        appointment_tree.column("ID", width=50, anchor="center")
        appointment_tree.column("Patient", width=150)
        appointment_tree.column("Doctor", width=150)
        appointment_tree.column("Date", width=100, anchor="center")
        appointment_tree.column("Time", width=100, anchor="center")
        appointment_tree.column("Notes", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=appointment_tree.yview)
        appointment_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        appointment_tree.pack(side="left", fill="both", expand=True)
        
        # Show initial appointment list
        self.show_appointment_list(appointment_tree)
        
        # Action buttons for selected appointment
        action_btn_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        action_btn_frame.pack(fill="x", pady=10)
        
        btn_delete = tk.Button(
            action_btn_frame,
            text="Delete Selected",
            command=lambda: self.delete_appointment(appointment_tree),
            font=self.font_small,
            bg=self.colors["danger"],
            fg="white",
            relief="flat"
        )
        btn_delete.pack(side="left", padx=10)

    def show_appointment_list(self, tree, date=None, search_term=None, search_by_id=False):
        """Populate appointment treeview"""
        for item in tree.get_children():
            tree.delete(item)
            
        appointments = get_appointments(date=date, search_term=search_term, search_by_id=search_by_id)
        for appt in appointments:
            tree.insert("", "end", values=(
                appt['id'],
                appt['patient_name'],
                appt['doctor_name'],
                appt['appointment_date'],
                f"{appt['start_time']} - {appt['end_time']}",
                appt['notes']
            ))

    def open_appointment_form(self):
        """Open appointment scheduling form"""
        form = tk.Toplevel(self.root)
        form.title("Schedule New Appointment")
        form.geometry("500x500")
        form.config(bg=self.colors["light"])
        
        # Get patients and doctors
        patients = get_patients()
        doctors = get_doctors()
        
        if not patients or not doctors:
            messagebox.showwarning("Warning", "No patients or doctors available")
            form.destroy()
            return
        
        # Form fields
        fields = [
            ("Patient:", "patient", ttk.Combobox(form, values=[f"{p['id']} - {p['name']}" for p in patients], state="readonly", font=self.font_small)),
            ("Doctor:", "doctor", ttk.Combobox(form, values=[f"{d['id']} - {d['name']} ({d['specialization']})" for d in doctors], state="readonly", font=self.font_small)),
            ("Date:", "date", tk.Entry(form, font=self.font_small)),
            ("Time Slot:", "time_slot", ttk.Combobox(form, state="readonly", font=self.font_small)),
            ("Notes:", "notes", tk.Text(form, font=self.font_small, height=5, width=30))
        ]
        
        for i, (label, _, widget) in enumerate(fields):
            tk.Label(
                form,
                text=label,
                bg=self.colors["light"],
                fg=self.colors["dark"],
                font=self.font_small
            ).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        
        # Set default date
        fields[2][2].insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Function to update time slots when doctor or date changes
        def update_time_slots():
            try:
                doctor_id = int(fields[1][2].get().split(" - ")[0])
                date = fields[2][2].get()
                datetime.strptime(date, "%Y-%m-%d")  # Validate date
                
                time_slots = get_available_time_slots(doctor_id, date)
                fields[3][2]['values'] = [f"{slot[0]} - {slot[1]}" for slot in time_slots]
                if time_slots:
                    fields[3][2].current(0)
            except (ValueError, IndexError):
                pass
        
        fields[1][2].bind("<<ComboboxSelected>>", lambda e: update_time_slots())
        fields[2][2].bind("<FocusOut>", lambda e: update_time_slots())
        
        # Submit button
        def submit():
            try:
                patient_id = int(fields[0][2].get().split(" - ")[0])
                doctor_id = int(fields[1][2].get().split(" - ")[0])
                date = fields[2][2].get()
                time_range = fields[3][2].get()
                notes = fields[4][2].get("1.0", tk.END).strip()
                
                if not time_range:
                    raise ValueError("Please select a time slot")
                
                start_time, end_time = time_range.split(" - ")
                
                schedule_appointment(patient_id, doctor_id, date, start_time, end_time, notes)
                messagebox.showinfo("Success", "Appointment scheduled successfully!")
                form.destroy()
                self.show_appointment_scheduling()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(
            form,
            text="Schedule Appointment",
            command=submit,
            font=self.font_small,
            bg=self.colors["primary"],
            fg="white",
            relief="flat"
        ).grid(row=len(fields), column=1, pady=10, sticky="e")

    def delete_appointment(self, tree):
        """Delete selected appointment"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to delete")
            return
        
        appointment_id = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this appointment?"):
            if delete_appointment(appointment_id):
                messagebox.showinfo("Success", "Appointment deleted successfully")
                self.show_appointment_scheduling()
            else:
                messagebox.showerror("Error", "Failed to delete appointment")

    def show_all_records(self):
        """Show dashboard with all records"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=self.colors["light"])
        self.current_frame.pack(fill="both", expand=True)
        
        # Navigation
        self.create_nav_button(self.current_frame)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(
            header_frame,
            text="All Records Dashboard",
            font=self.font_large,
            bg=self.colors["light"],
            fg=self.colors["dark"]
        ).pack(side="left", padx=20)
        
        # Statistics frame
        stats_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        stats_frame.pack(fill="x", pady=20, padx=20)
        
        # Get counts
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients")
            patient_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM doctors")
            doctor_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM appointments")
            appointment_count = cursor.fetchone()[0]
        
        # Create stat cards
        stat_cards = [
            ("Patients", patient_count, self.colors["primary"]),
            ("Doctors", doctor_count, self.colors["secondary"]),
            ("Appointments", appointment_count, self.colors["accent"])
        ]
        
        for i, (title, count, color) in enumerate(stat_cards):
            card = tk.Frame(stats_frame, bg=color, bd=2, relief="groove")
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            
            tk.Label(
                card,
                text=title,
                font=self.font_medium,
                bg=color,
                fg="white"
            ).pack(pady=(10, 0), padx=20)
            
            tk.Label(
                card,
                text=str(count),
                font=("Helvetica", 24, "bold"),
                bg=color,
                fg="white"
            ).pack(pady=(0, 10))
        
        # Recent activity
        activity_frame = tk.Frame(self.current_frame, bg=self.colors["light"])
        activity_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create notebook for different views
        notebook = ttk.Notebook(activity_frame)
        notebook.pack(fill="both", expand=True)
        
        # Patients tab
        patient_tab = ttk.Frame(notebook)
        notebook.add(patient_tab, text="Patients")
        
        patient_tree = ttk.Treeview(
            patient_tab,
            columns=("ID", "Name", "Age", "Gender", "Diagnosis", "Admission Date"),
            show="headings"
        )
        
        patient_tree.heading("ID", text="ID")
        patient_tree.heading("Name", text="Name")
        patient_tree.heading("Age", text="Age")
        patient_tree.heading("Gender", text="Gender")
        patient_tree.heading("Diagnosis", text="Diagnosis")
        patient_tree.heading("Admission Date", text="Admission Date")
        
        for patient in get_patients():
            patient_tree.insert("", "end", values=(
                patient['id'],
                patient['name'],
                patient['age'],
                patient['gender'],
                patient['diagnosis'],
                patient['admission_date']
            ))
        
        patient_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Doctors tab
        doctor_tab = ttk.Frame(notebook)
        notebook.add(doctor_tab, text="Doctors")
        
        doctor_tree = ttk.Treeview(
            doctor_tab,
            columns=("ID", "Name", "Specialization", "Experience", "Gender"),
            show="headings"
        )
        
        doctor_tree.heading("ID", text="ID")
        doctor_tree.heading("Name", text="Name")
        doctor_tree.heading("Specialization", text="Specialization")
        doctor_tree.heading("Experience", text="Experience")
        doctor_tree.heading("Gender", text="Gender")
        
        for doctor in get_doctors():
            doctor_tree.insert("", "end", values=(
                doctor['id'],
                doctor['name'],
                doctor['specialization'],
                doctor['experience'],
                doctor['gender']
            ))
        
        doctor_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Appointments tab
        appt_tab = ttk.Frame(notebook)
        notebook.add(appt_tab, text="Appointments")
        
        appt_tree = ttk.Treeview(
            appt_tab,
            columns=("ID", "Patient", "Doctor", "Date", "Time", "Notes"),
            show="headings"
        )
        
        appt_tree.heading("ID", text="ID")
        appt_tree.heading("Patient", text="Patient")
        appt_tree.heading("Doctor", text="Doctor")
        appt_tree.heading("Date", text="Date")
        appt_tree.heading("Time", text="Time")
        appt_tree.heading("Notes", text="Notes")
        
        for appt in get_appointments():
            appt_tree.insert("", "end", values=(
                appt['id'],
                appt['patient_name'],
                appt['doctor_name'],
                appt['appointment_date'],
                f"{appt['start_time']} - {appt['end_time']}",
                appt['notes']
            ))
        
        appt_tree.pack(fill="both", expand=True, padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    
    # First show welcome screen
    def start_main_app():
        new_root = tk.Tk()
        app = HospitalApp(new_root)
        new_root.mainloop()

    
    welcome = WelcomeScreen(root, start_main_app)
    root.mainloop()