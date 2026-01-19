import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Requires: pip install pillow
import pandas as pd
import joblib

# --- THEME & COLORS ---
COLORS = {
    "bg_dark": "#0f172a",  # Deep Navy (Background)
    "bg_panel": "#1e293b",  # Slate Grey (Panels)
    "text_light": "#f8fafc",  # Off-white
    "text_dim": "#94a3b8",  # Muted Grey
    "accent": "#3b82f6",  # Royal Blue
    "danger": "#ef4444",  # Red
    "success": "#22c55e",  # Green
}

# Increased font sizes for "Bigger" feel
FONT_HEADER = ("Helvetica", 24, "bold")
FONT_BODY = ("Helvetica", 12)  # Slightly larger for inputs
FONT_RESULT = ("Helvetica", 16, "bold")  # NEW: Very bold for the %


class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 1. SETUP WINDOW
        self.title("Dino Bank System")
        self.configure(bg=COLORS["bg_dark"])
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.exit_app)

        # 2. STYLE CONFIGURATION (Make Dropdowns Bigger)
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' allows more custom coloring than default

        # Configure the Dropdown (Combobox) to be tall and dark
        self.style.configure("TCombobox",
                             fieldbackground=COLORS["bg_panel"],
                             background=COLORS["accent"],
                             foreground="black",
                             arrowsize=20,  # Bigger arrow
                             padding=10)  # Taller box (Internal padding)

        # 3. LOAD AI BRAIN
        self.model = None
        self.scaler = None
        try:
            self.model = joblib.load('loan_model.pkl')
            self.scaler = joblib.load('scaler.pkl')
        except:
            pass

            # 4. START AT LOGIN PAGE
        self.show_login_screen()

    def load_image(self, path, size):
        """Helper to safely load images"""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            return None

    # ==========================================
    # 🔒 SCREEN 1: LOGIN PAGE
    # ==========================================
    def show_login_screen(self):
        self.login_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        self.login_frame.pack(fill="both", expand=True)

        # -- Left Side: Branding Panel --
        banner_frame = tk.Frame(self.login_frame, bg=COLORS["bg_dark"], width=500)
        banner_frame.pack(side="left", fill="both", expand=True)

        left_content = tk.Frame(banner_frame, bg=COLORS["bg_dark"])
        left_content.place(relx=0.5, rely=0.5, anchor="center")

        # REBRANDING HERE
        tk.Label(left_content, text="DINO", font=("Helvetica", 50, "bold"), bg=COLORS["bg_dark"],
                 fg=COLORS["text_light"]).pack()
        tk.Label(left_content, text="FINANCIAL SYSTEMS", font=("Helvetica", 18, "bold"), bg=COLORS["bg_dark"],
                 fg=COLORS["accent"]).pack(pady=10)
        tk.Label(left_content, text="AI-Powered Risk Assessment", font=("Helvetica", 14), bg=COLORS["bg_dark"],
                 fg=COLORS["text_dim"]).pack(pady=5)

        # -- Right Side: Login Form --
        form_area = tk.Frame(self.login_frame, bg=COLORS["bg_panel"], width=600)
        form_area.pack(side="right", fill="both", expand=True)

        center_box = tk.Frame(form_area, bg=COLORS["bg_panel"])
        center_box.place(relx=0.5, rely=0.5, anchor="center")

        img_logo = self.load_image("banking.png", (100, 100))  # Slightly bigger logo
        if img_logo:
            lbl_logo = tk.Label(center_box, image=img_logo, bg=COLORS["bg_panel"])
            lbl_logo.image = img_logo
            lbl_logo.pack(pady=20)

        tk.Label(center_box, text="SECURE LOGIN", font=("Helvetica", 20, "bold"), bg=COLORS["bg_panel"],
                 fg=COLORS["text_light"]).pack(pady=10)

        # User Field
        frm_user = tk.Frame(center_box, bg=COLORS["bg_panel"])
        frm_user.pack(pady=10)
        img_user = self.load_image("person.png", (30, 30))
        if img_user:
            lbl_u = tk.Label(frm_user, image=img_user, bg=COLORS["bg_panel"])
            lbl_u.image = img_user
            lbl_u.pack(side="left", padx=10)
        self.entry_user = tk.Entry(frm_user, font=FONT_BODY, width=25, bg="white", fg="black", relief="flat", bd=5)
        self.entry_user.pack(side="left", pady=5, ipady=3)  # ipady makes input taller
        self.entry_user.insert(0, "admin")

        # Pass Field
        frm_pass = tk.Frame(center_box, bg=COLORS["bg_panel"])
        frm_pass.pack(pady=10)
        img_lock = self.load_image("padlock.png", (25, 30))
        if img_lock:
            lbl_p = tk.Label(frm_pass, image=img_lock, bg=COLORS["bg_panel"])
            lbl_p.image = img_lock
            lbl_p.pack(side="left", padx=12)
        self.entry_pass = tk.Entry(frm_pass, font=FONT_BODY, width=25, show="*", bg="white", fg="black", relief="flat",
                                   bd=5)
        self.entry_pass.pack(side="left", pady=5, ipady=3)
        self.entry_pass.insert(0, "admin123")

        tk.Button(center_box, text="AUTHENTICATE", command=self.validate_login, bg=COLORS["accent"], fg="white",
                  font=("Helvetica", 12, "bold"), width=20, cursor="hand2", pady=5).pack(pady=30)

    def validate_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        if user == "admin" and pwd == "admin123":
            self.login_frame.destroy()
            self.show_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Credentials")

    # ==========================================
    # 🏦 SCREEN 2: MAIN DASHBOARD
    # ==========================================
    def show_dashboard(self):
        self.main_container = tk.Frame(self, bg=COLORS["bg_dark"])
        self.main_container.pack(fill="both", expand=True, padx=40, pady=40)

        self.entries = {}

        # --- HEADER ---
        header = tk.Frame(self.main_container, bg=COLORS["bg_dark"])
        header.pack(fill="x", pady=(0, 20))

        img_logo = self.load_image("banking.png", (50, 50))
        if img_logo:
            lbl = tk.Label(header, image=img_logo, bg=COLORS["bg_dark"])
            lbl.image = img_logo
            lbl.pack(side="left", padx=10)

        # REBRANDING HERE
        tk.Label(header, text="DINO BANK AI TERMINAL", font=FONT_HEADER, bg=COLORS["bg_dark"],
                 fg=COLORS["text_light"]).pack(side="left")

        tk.Button(header, text="LOGOUT X", command=self.exit_app, bg=COLORS["danger"], fg="white",
                  font=("Helvetica", 10, "bold"), bd=0, padx=20, pady=8, cursor="hand2").pack(side="right")

        # --- CONTENT SPLIT ---
        content = tk.Frame(self.main_container, bg=COLORS["bg_dark"])
        content.pack(fill="both", expand=True)

        # LEFT: FORM
        form_frame = tk.Frame(content, bg=COLORS["bg_panel"], padx=25, pady=25)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 25))

        self.input_grid = tk.Frame(form_frame, bg=COLORS["bg_panel"])
        self.input_grid.pack(fill="x")

        # Add all inputs
        self.add_row(0, "Gender", ["Male", "Female"], "Married", ["No", "Yes"])
        self.add_row(1, "Dependents", ["0", "1", "2", "3+"], "Education", ["Graduate", "Not Graduate"])
        self.add_row(2, "Self Employed", ["No", "Yes"], "Credit History", ["1.0 (Good)", "0.0 (Bad)"])
        self.add_row(3, "Applicant Income", None, "Co-Applicant Income", None)
        self.add_row(4, "Loan Amount", None, "Loan Term (Months)", None)
        self.add_row(5, "Property Area", ["Semiurban", "Urban", "Rural"], None, None)

        # Defaults
        self.entries["Applicant Income"].insert(0, "5000")
        self.entries["Co-Applicant Income"].insert(0, "0")
        self.entries["Loan Amount"].insert(0, "120")
        self.entries["Loan Term (Months)"].insert(0, "360")

        tk.Button(form_frame, text="RUN ANALYSIS", command=self.run_logic, bg=COLORS["accent"], fg="white",
                  font=("Helvetica", 16, "bold"), pady=12, cursor="hand2").pack(fill="x", pady=25)

        # RIGHT: STATUS
        self.status_frame = tk.Frame(content, bg=COLORS["bg_panel"], width=350)
        self.status_frame.pack(side="right", fill="y")
        self.status_frame.pack_propagate(False)

        tk.Label(self.status_frame, text="DECISION STATUS", font=("Helvetica", 14, "bold"), bg=COLORS["bg_panel"],
                 fg=COLORS["text_dim"]).pack(pady=(30, 10))

        self.lbl_status = tk.Label(self.status_frame, text="WAITING", font=("Helvetica", 30, "bold"),
                                   bg=COLORS["bg_dark"], fg=COLORS["text_dim"], width=12, pady=15)
        self.lbl_status.pack(pady=20)

        # This label will hold the Bold Percentage
        self.lbl_reason = tk.Label(self.status_frame, text="Ready for data...", font=FONT_BODY, bg=COLORS["bg_panel"],
                                   fg=COLORS["text_light"], wraplength=280)
        self.lbl_reason.pack(pady=10)

    # --- HELPERS ---
    def add_row(self, row, l1, opt1, l2, opt2):
        # Increased pady for spacing
        tk.Label(self.input_grid, text=l1, bg=COLORS["bg_panel"], fg=COLORS["text_dim"],
                 font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="w", pady=12)

        if opt1:
            # Using the big style we created
            e1 = ttk.Combobox(self.input_grid, values=opt1, state="readonly", font=FONT_BODY, style="TCombobox")
            e1.current(0)
        else:
            e1 = tk.Entry(self.input_grid, font=FONT_BODY, relief="flat", bd=5)

        e1.grid(row=row, column=1, padx=15, sticky="ew", ipady=4)  # ipady makes it taller
        self.entries[l1] = e1

        if l2:
            tk.Label(self.input_grid, text=l2, bg=COLORS["bg_panel"], fg=COLORS["text_dim"],
                     font=("Helvetica", 10, "bold")).grid(row=row, column=2, sticky="w", pady=12)
            if opt2:
                e2 = ttk.Combobox(self.input_grid, values=opt2, state="readonly", font=FONT_BODY, style="TCombobox")
                e2.current(0)
            else:
                e2 = tk.Entry(self.input_grid, font=FONT_BODY, relief="flat", bd=5)

            e2.grid(row=row, column=3, padx=15, sticky="ew", ipady=4)
            self.entries[l2] = e2

        self.input_grid.columnconfigure(1, weight=1)
        self.input_grid.columnconfigure(3, weight=1)

    # --- LOGIC ---
    def run_logic(self):
        try:
            # 1. HARD RULES
            income = float(self.entries["Applicant Income"].get())
            coincome = float(self.entries["Co-Applicant Income"].get())
            total = income + coincome

            if total < 4000:
                self.lbl_status.config(text="REJECTED", fg=COLORS["danger"])
                self.lbl_reason.config(text="REASON: Total income is below bank policy threshold ($4,000).",
                                       font=FONT_BODY)
                return

            # 2. AI PREDICTION
            if not self.model:
                messagebox.showerror("Error", "Model not loaded.")
                return

            # Prepare Data
            val_gender = 1 if self.entries["Gender"].get() == "Male" else 0
            val_married = 1 if self.entries["Married"].get() == "Yes" else 0
            dep = self.entries["Dependents"].get()
            val_dep = 3 if dep == "3+" else int(dep)
            val_edu = 1 if self.entries["Education"].get() == "Graduate" else 0
            val_self = 1 if self.entries["Self Employed"].get() == "Yes" else 0
            val_credit = 1.0 if "1.0" in self.entries["Credit History"].get() else 0.0
            val_loan = float(self.entries["Loan Amount"].get())
            val_term = float(self.entries["Loan Term (Months)"].get())
            area = self.entries["Property Area"].get()
            val_r = 1 if area == "Rural" else 0
            val_s = 1 if area == "Semiurban" else 0
            val_u = 1 if area == "Urban" else 0

            df = pd.DataFrame(
                [[val_gender, val_married, val_dep, val_edu, val_self, income, coincome, val_loan, val_term, val_credit,
                  val_r, val_s, val_u]],
                columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome',
                         'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area_Rural',
                         'Property_Area_Semiurban', 'Property_Area_Urban'])

            # Predict
            scaled = self.scaler.transform(df)
            pred = self.model.predict(scaled)
            prob = self.model.predict_proba(scaled)[0][1]

            if pred[0] == 1:
                self.lbl_status.config(text="APPROVED", fg=COLORS["success"])
                # BOLD RESULT HERE
                self.lbl_reason.config(text=f"Confidence:\n{prob * 100:.1f}%", font=FONT_RESULT)
            else:
                self.lbl_status.config(text="REJECTED", fg=COLORS["danger"])
                # BOLD RESULT HERE
                self.lbl_reason.config(text=f"Confidence:\n{(1 - prob) * 100:.1f}%", font=FONT_RESULT)

        except ValueError:
            messagebox.showerror("Error", "Check your number inputs.")

    def exit_app(self, e=None):
        self.destroy()


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()