import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import joblib
import datetime

# --- THEME CONFIGURATION ---
COLORS = {
    "bg_dark": "#0f172a",  # Deep Navy (Main BG)
    "bg_panel": "#1e293b",  # Lighter Slate (Panels)
    "bg_input": "#334155",  # Input field background
    "text_light": "#f8fafc",  # White text
    "text_dim": "#94a3b8",  # Grey text
    "accent": "#6366f1",  # Indigo (Sophisticated Blue/Purple)
    "accent_hover": "#4f46e5",  # Darker Indigo
    "danger": "#ef4444",  # Red
    "success": "#10b981",  # Emerald Green
    "log_bg": "#000000",  # Black for terminal
    "log_text": "#00ff00"  # Hacker Green
}

FONTS = {
    "header": ("Segoe UI", 26, "bold"),
    "sub": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 11),
    "result": ("Segoe UI", 18, "bold")
}


class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 1. WINDOW SETUP
        self.title("Dino Bank - AI Admin Terminal")
        self.configure(bg=COLORS["bg_dark"])
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.exit_app)

        # 2. STYLING
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure("TCombobox",
                             fieldbackground=COLORS["bg_input"],
                             background=COLORS["accent"],
                             foreground="white",
                             arrowsize=20)
        self.style.map('TCombobox', fieldbackground=[('readonly', COLORS["bg_input"])],
                       selectbackground=[('readonly', COLORS["bg_input"])], selectforeground=[('readonly', 'white')])

        # 3. LOAD ML ARTEFACTS
        self.model = None
        self.scaler = None
        try:
            self.model = joblib.load('loan_model.pkl')
            self.scaler = joblib.load('scaler.pkl')
        except Exception as e:
            print(f"[SYSTEM] Warning: ML files missing. {e}")

        # 4. START
        self.show_login_screen()

    def load_image(self, path, size):
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            return None

    # --- CENTRALISED AUDIT LOGGING SYSTEM ---
    def log(self, message):
        """Writes a timestamped message to the on-screen terminal and stdout."""
        if hasattr(self, 'terminal'):
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.terminal.configure(state='normal')
            self.terminal.insert(tk.END, f"[{timestamp}] {message}\n")
            self.terminal.see(tk.END)
            self.terminal.configure(state='disabled')
        print(message)

    # ==========================================
    # SCREEN 1: LOGIN
    # ==========================================
    def show_login_screen(self):
        self.login_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        self.login_frame.pack(fill="both", expand=True)

        left = tk.Frame(self.login_frame, bg=COLORS["bg_dark"], width=600)
        left.pack(side="left", fill="both", expand=True)
        content = tk.Frame(left, bg=COLORS["bg_dark"])
        content.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(content, text="DINO", font=("Segoe UI", 60, "bold"), bg=COLORS["bg_dark"], fg="white").pack()
        tk.Label(content, text="FINANCIAL INTELLIGENCE", font=("Segoe UI", 20), bg=COLORS["bg_dark"],
                 fg=COLORS["accent"]).pack(pady=10)

        right = tk.Frame(self.login_frame, bg=COLORS["bg_panel"], width=500)
        right.pack(side="right", fill="both", expand=True)
        box = tk.Frame(right, bg=COLORS["bg_panel"])
        box.place(relx=0.5, rely=0.5, anchor="center")

        img_logo = self.load_image("banking.png", (80, 80))
        if img_logo:
            lbl = tk.Label(box, image=img_logo, bg=COLORS["bg_panel"])
            lbl.image = img_logo
            lbl.pack(pady=20)

        tk.Label(box, text="ADMIN LOGIN", font=FONTS["header"], bg=COLORS["bg_panel"], fg="white").pack(pady=20)

        self.entry_user = self.create_login_entry(box, "person.png", "")
        self.entry_pass = self.create_login_entry(box, "padlock.png", "", is_pass=True)

        btn = tk.Button(box, text="ACCESS TERMINAL", command=self.validate_login,
                        bg=COLORS["accent"], fg="white", font=FONTS["sub"],
                        relief="flat", padx=40, pady=10, cursor="hand2")
        btn.pack(pady=30)

        tk.Label(box, text="(Hint: admin / admin123)", bg=COLORS["bg_panel"], fg="#444").pack()

    def create_login_entry(self, parent, icon_file, default_text, is_pass=False):
        frame = tk.Frame(parent, bg=COLORS["bg_panel"])
        frame.pack(pady=10)
        img = self.load_image(icon_file, (24, 24))
        if img:
            lbl = tk.Label(frame, image=img, bg=COLORS["bg_panel"])
            lbl.image = img
            lbl.pack(side="left", padx=10)

        entry = tk.Entry(frame, font=FONTS["body"], width=25, bg="white", relief="flat", show="*" if is_pass else "")
        entry.pack(side="left", ipady=5)
        return entry

    def validate_login(self):
        if self.entry_user.get() == "admin" and self.entry_pass.get() == "admin123":
            self.login_frame.destroy()
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    # ==========================================
    # SCREEN 2: DASHBOARD
    # ==========================================
    def show_dashboard(self):
        self.main_container = tk.Frame(self, bg=COLORS["bg_dark"])
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)
        self.entries = {}

        # --- HEADER ---
        header = tk.Frame(self.main_container, bg=COLORS["bg_dark"])
        header.pack(fill="x", pady=(0, 20))

        img = self.load_image("banking.png", (40, 40))
        if img:
            lbl = tk.Label(header, image=img, bg=COLORS["bg_dark"])
            lbl.image = img
            lbl.pack(side="left", padx=10)

        tk.Label(header, text="DINO BANK // ADMIN DASHBOARD", font=FONTS["header"], bg=COLORS["bg_dark"],
                 fg="white").pack(side="left")
        tk.Button(header, text="LOGOUT", command=self.exit_app, bg=COLORS["danger"], fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=20).pack(side="right")

        # --- CONTENT AREA ---
        content = tk.Frame(self.main_container, bg=COLORS["bg_dark"])
        content.pack(fill="both", expand=True)

        # LEFT COLUMN: INPUTS
        left_col = tk.Frame(content, bg=COLORS["bg_panel"], padx=20, pady=20)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))

        self.create_group_label(left_col, "PERSONAL DETAILS")
        grid_personal = tk.Frame(left_col, bg=COLORS["bg_panel"])
        grid_personal.pack(fill="x", pady=(0, 20))
        self.add_input(grid_personal, 0, "Gender", ["Male", "Female"], "Married", ["No", "Yes"])
        self.add_input(grid_personal, 1, "Dependents", ["0", "1", "2", "3+"], "Education",
                       ["Graduate", "Not Graduate"])
        self.add_input(grid_personal, 2, "Self Employed", ["No", "Yes"], "Property Area",
                       ["Semiurban", "Urban", "Rural"])

        self.create_group_label(left_col, "FINANCIAL DATA")
        grid_finance = tk.Frame(left_col, bg=COLORS["bg_panel"])
        grid_finance.pack(fill="x")
        self.add_input(grid_finance, 0, "Applicant Income", None, "Co-Applicant Income", None)
        self.add_input(grid_finance, 1, "Loan Amount", None, "Loan Term (Months)", None)
        self.add_input(grid_finance, 2, "Credit History", ["Good (All Debts Paid)", "Bad (Unpaid Debts)"], None, None)

        tk.Button(left_col, text="RUN RISK ANALYSIS", command=self.run_logic,
                  bg=COLORS["accent"], fg="white", font=("Segoe UI", 14, "bold"),
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=20, side="bottom")

        # RIGHT COLUMN: STATUS + LOGS
        right_col = tk.Frame(content, bg=COLORS["bg_dark"], width=400)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)

        status_box = tk.Frame(right_col, bg=COLORS["bg_panel"], padx=20, pady=20)
        status_box.pack(fill="x", pady=(0, 20))
        tk.Label(status_box, text="DECISION ENGINE", font=FONTS["sub"], bg=COLORS["bg_panel"],
                 fg=COLORS["text_dim"]).pack(anchor="w")
        self.lbl_status = tk.Label(status_box, text="READY", font=("Segoe UI", 32, "bold"), bg=COLORS["bg_panel"],
                                   fg=COLORS["text_dim"])
        self.lbl_status.pack(pady=10)
        self.lbl_prob = tk.Label(status_box, text="Waiting for input...", font=FONTS["body"], bg=COLORS["bg_panel"],
                                 fg="white")
        self.lbl_prob.pack()

        log_frame = tk.Frame(right_col, bg="black", bd=2, relief="sunken")
        log_frame.pack(fill="both", expand=True)
        tk.Label(log_frame, text="> SYSTEM_LOGS", bg="black", fg="#00ff00", font=("Consolas", 10)).pack(anchor="w",
                                                                                                        padx=5)

        self.terminal = scrolledtext.ScrolledText(log_frame, bg="black", fg=COLORS["log_text"], font=("Consolas", 9),
                                                  state='disabled')
        self.terminal.pack(fill="both", expand=True)
        self.log("System initialized.")
        self.log("ML artefacts loaded: loan_model.pkl, scaler.pkl")
        self.log("Hybrid Decision Engine ready.")
        self.log("Waiting for user inputs...")

    # --- HELPERS ---
    def create_group_label(self, parent, text):
        tk.Label(parent, text=text, font=FONTS["sub"], bg=COLORS["bg_panel"], fg=COLORS["accent"]).pack(anchor="w",
                                                                                                        pady=(5, 10))

    def add_input(self, parent, row, l1, opt1, l2, opt2):
        tk.Label(parent, text=l1, bg=COLORS["bg_panel"], fg="white", font=("Segoe UI", 10, "bold")).grid(row=row,
                                                                                                         column=0,
                                                                                                         sticky="w",
                                                                                                         pady=5)
        if opt1:
            e1 = ttk.Combobox(parent, values=opt1, state="readonly", font=FONTS["body"], style="TCombobox")
        else:
            e1 = tk.Entry(parent, font=FONTS["body"], bg=COLORS["bg_input"], fg="white", insertbackground="white",
                          relief="flat")
        e1.grid(row=row, column=1, padx=10, sticky="ew", ipady=4)
        self.entries[l1] = e1

        if l2:
            tk.Label(parent, text=l2, bg=COLORS["bg_panel"], fg="white", font=("Segoe UI", 10, "bold")).grid(row=row,
                                                                                                             column=2,
                                                                                                             sticky="w",
                                                                                                             pady=5)
            if opt2:
                e2 = ttk.Combobox(parent, values=opt2, state="readonly", font=FONTS["body"], style="TCombobox")
            else:
                e2 = tk.Entry(parent, font=FONTS["body"], bg=COLORS["bg_input"], fg="white", insertbackground="white",
                              relief="flat")
            e2.grid(row=row, column=3, padx=10, sticky="ew", ipady=4)
            self.entries[l2] = e2

        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=1)

    # ==========================================
    # HYBRID DECISION ENGINE: run_logic()
    # ==========================================
    def run_logic(self):
        self.log("-" * 30)
        self.log("[PROCESS] Initiating analysis...")

        try:
            # ============================================
            # GATE 1: INPUT VALIDATION (try-except guard)
            # ============================================
            try:
                inc_text = self.entries["Applicant Income"].get()
                coinc_text = self.entries["Co-Applicant Income"].get()

                if not inc_text or not coinc_text:
                    raise ValueError("Empty Fields")

                inc = float(inc_text)
                coinc = float(coinc_text)
            except ValueError:
                self.log("[ERROR] Missing or invalid financial data.")
                messagebox.showwarning("Incomplete Data", "Please fill in all numerical financial fields.")
                return

            total = inc + coinc
            self.log(f"[DATA] Applicant Income: ${inc:,.0f} | Co-Applicant: ${coinc:,.0f} | Total: ${total:,.0f}")

            # ============================================
            # GATE 2: DETERMINISTIC POLICY ENFORCEMENT
            # ============================================

            # 2a. Income Floor Policy (HARD_REJECT)
            if total < 2500:
                self.log("[POLICY] HARD_REJECT: Combined income below $2,500 statutory minimum.")
                self.update_status("REJECTED", COLORS["danger"], "Reason: Income below policy threshold")
                return

            if not self.model:
                self.log("[ERROR] AI Model not loaded. Cannot proceed.")
                return

            # 2b. Safety Clamp for Out-of-Distribution Protection
            clamped_inc = min(inc, 15000)
            clamped_coinc = min(coinc, 8000)

            if inc > 15000 or coinc > 8000:
                self.log(f"[CLAMP] Outlier detected. Original: ${inc:,.0f} / ${coinc:,.0f}")
                self.log(f"[CLAMP] Clamped to: ${clamped_inc:,.0f} / ${clamped_coinc:,.0f} for Z-score stability.")

            # ============================================
            # GATE 3: AI INFERENCE (predict_proba)
            # ============================================

            # 3a. Validate and encode dropdown selections
            try:
                gender = 1 if self.entries["Gender"].get() == "Male" else 0
                married = 1 if self.entries["Married"].get() == "Yes" else 0

                dep_raw = self.entries["Dependents"].get()
                if not dep_raw: raise ValueError("Dropdown Empty")
                dep = 3 if dep_raw == "3+" else int(dep_raw)

                edu = 1 if self.entries["Education"].get() == "Graduate" else 0
                self_emp = 1 if self.entries["Self Employed"].get() == "Yes" else 0

                credit_txt = self.entries["Credit History"].get()
                if not credit_txt: raise ValueError("Dropdown Empty")
                credit = 1.0 if "Good" in credit_txt else 0.0

                area_txt = self.entries["Property Area"].get()
                if not area_txt: raise ValueError("Dropdown Empty")
                area_r = 1 if area_txt == "Rural" else 0
                area_s = 1 if area_txt == "Semiurban" else 0
                area_u = 1 if area_txt == "Urban" else 0

                loan = float(self.entries["Loan Amount"].get())
                term = float(self.entries["Loan Term (Months)"].get())

            except ValueError:
                self.log("[ERROR] Missing dropdown selections or invalid loan data.")
                messagebox.showwarning("Incomplete Data", "Please select options for all dropdowns.")
                return

            # 3b. Build DataFrame with CLAMPED income values
            df = pd.DataFrame(
                [[gender, married, dep, edu, self_emp, clamped_inc, clamped_coinc, loan, term, credit, area_r, area_s, area_u]],
                columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome',
                         'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History',
                         'Property_Area_Rural', 'Property_Area_Semiurban', 'Property_Area_Urban'])

            self.log("[GATE 3] Scaling features via StandardScaler...")
            scaled = self.scaler.transform(df)

            # 3c. Compute raw log-odds (linear output before sigmoid)
            log_odds = np.dot(scaled, self.model.coef_[0]) + self.model.intercept_[0]
            self.log(f"[ML] Raw log-odds (z): {log_odds[0]:.4f}")

            # 3d. Extract probability via predict_proba
            pred = self.model.predict(scaled)[0]
            prob = self.model.predict_proba(scaled)[0][1]

            self.log(f"[ML] Sigmoid probability: {prob:.4f}")
            self.log(f"[ML] Confidence: {prob * 100:.1f}%")

            # 3e. Display top contributing features for audit trail
            feature_names = df.columns.tolist()
            coefs = self.model.coef_[0]
            contributions = scaled[0] * coefs
            top_indices = np.argsort(np.abs(contributions))[::-1][:3]
            self.log("[ML] Top feature contributions:")
            for idx in top_indices:
                self.log(f"      {feature_names[idx]}: {contributions[idx]:+.4f}")

            # 3f. Final decision
            if pred == 1:
                self.log("[RESULT] APPROVED")
                self.update_status("APPROVED", COLORS["success"], f"Confidence: {prob * 100:.1f}%")
            else:
                self.log("[RESULT] REJECTED")
                self.update_status("REJECTED", COLORS["danger"], f"Risk Level: {(1 - prob) * 100:.1f}%")

        except Exception as e:
            self.log(f"[ERROR] {str(e)}")
            messagebox.showerror("System Error", str(e))

    def update_status(self, text, color, subtext):
        self.lbl_status.config(text=text, fg=color)
        self.lbl_prob.config(text=subtext)

    def exit_app(self, e=None):
        self.destroy()


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()