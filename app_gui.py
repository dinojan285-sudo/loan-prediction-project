import tkinter as tk
from tkinter import messagebox
import pandas as pd
import joblib

# --- 1. Load the Model & Scaler ---
try:
    model = joblib.load('loan_model.pkl')
    scaler = joblib.load('scaler.pkl')
    print("Model and Scaler loaded successfully!")
except FileNotFoundError:
    messagebox.showerror("Error", "Model files not found! Make sure they are in the same folder.")
    exit()


# --- 2. The Prediction Logic ---
def run_prediction():
    try:
        # Get raw inputs
        raw_income = float(entry_income.get())
        raw_coincome = float(entry_coincome.get())
        raw_loanamt = float(entry_loanamt.get())
        raw_term = float(entry_term.get())

        # Translate Text to Numbers
        val_gender = 1 if var_gender.get() == "Male" else 0
        val_married = 1 if var_married.get() == "Yes" else 0
        val_education = 1 if var_education.get() == "Graduate" else 0
        val_self_emp = 1 if var_self_emp.get() == "Yes" else 0

        dep = var_dependents.get()
        val_dependents = 3 if dep == "3+" else int(dep)

        val_credit = float(var_credit.get())

        area = var_area.get()
        val_rural = 1 if area == "Rural" else 0
        val_semi = 1 if area == "Semiurban" else 0
        val_urban = 1 if area == "Urban" else 0

        # Create DataFrame
        input_data = pd.DataFrame({
            'Gender': [val_gender],
            'Married': [val_married],
            'Dependents': [val_dependents],
            'Education': [val_education],
            'Self_Employed': [val_self_emp],
            'ApplicantIncome': [raw_income],
            'CoapplicantIncome': [raw_coincome],
            'LoanAmount': [raw_loanamt],
            'Loan_Amount_Term': [raw_term],
            'Credit_History': [val_credit],
            'Property_Area_Rural': [val_rural],
            'Property_Area_Semiurban': [val_semi],
            'Property_Area_Urban': [val_urban]
        })

        # Scale and Predict
        scaled_input = scaler.transform(input_data)
        prediction = model.predict(scaled_input)

        # Show Result
        if prediction[0] == 1:
            messagebox.showinfo("Result", "✅ Loan APPROVED!")
        else:
            messagebox.showwarning("Result", "❌ Loan REJECTED.")

    except ValueError:
        messagebox.showerror("Error", "Please check that Income and Loan Amount are valid numbers.")


# --- 3. Build the GUI ---
root = tk.Tk()
root.title("Bank Loan Predictor")
root.geometry("400x750")


def add_label(text):
    tk.Label(root, text=text, font=("Arial", 10, "bold")).pack(pady=5)


add_label("Gender")
var_gender = tk.StringVar(value="Male")
tk.OptionMenu(root, var_gender, "Male", "Female").pack()

add_label("Married")
var_married = tk.StringVar(value="No")
tk.OptionMenu(root, var_married, "Yes", "No").pack()

add_label("Dependents")
var_dependents = tk.StringVar(value="0")
tk.OptionMenu(root, var_dependents, "0", "1", "2", "3+").pack()

add_label("Education")
var_education = tk.StringVar(value="Graduate")
tk.OptionMenu(root, var_education, "Graduate", "Not Graduate").pack()

add_label("Self Employed")
var_self_emp = tk.StringVar(value="No")
tk.OptionMenu(root, var_self_emp, "Yes", "No").pack()

add_label("Applicant Income")
entry_income = tk.Entry(root)
entry_income.insert(0, "5000")
entry_income.pack()

add_label("Coapplicant Income")
entry_coincome = tk.Entry(root)
entry_coincome.insert(0, "0")
entry_coincome.pack()

add_label("Loan Amount (Thousands)")
entry_loanamt = tk.Entry(root)
entry_loanamt.insert(0, "120")
entry_loanamt.pack()

add_label("Loan Term (Months)")
entry_term = tk.Entry(root)
entry_term.insert(0, "360")
entry_term.pack()

add_label("Credit History (1.0 = Good)")
var_credit = tk.StringVar(value="1.0")
tk.OptionMenu(root, var_credit, "1.0", "0.0").pack()

add_label("Property Area")
var_area = tk.StringVar(value="Semiurban")
tk.OptionMenu(root, var_area, "Urban", "Semiurban", "Rural").pack()

tk.Button(root, text="PREDICT STATUS", command=run_prediction, bg="green", fg="white", font=("Arial", 12, "bold")).pack(
    pady=20)

root.mainloop()