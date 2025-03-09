import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import numpy_financial as npf
import csv
import os

def validate_inputs():
    try:
        investment=float(entry_investment.get())
        cash_flows=list(map(float, entry_cash_flows.get().split(',')))
        if entry_discount_rate.get():
            discount_rate=float(entry_discount_rate.get())
        else:
            discount_rate=None
        return investment, cash_flows, discount_rate
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all fields contain valid numbers.")
        return None, None, None

def calculate_payback():
    investment, cash_flows, _=validate_inputs()
    if investment is None:
        return
    
    cumulative_cash_flow=0
    payback_period=0
    for i, cash_flow in enumerate(cash_flows):
        cumulative_cash_flow+=cash_flow
        if cumulative_cash_flow>=investment:
            payback_period=i+1
            break
    else:
        payback_period="Not achieved"
    
    label_result.config(text=f"Payback Period: {payback_period} years")

def calculate_arr():
    investment, cash_flows, _=validate_inputs()
    if investment is None:
        return

    avg_profit=np.mean(cash_flows)
    arr=(avg_profit/investment)*100
    label_result.config(text=f"ARR: {arr:.2f}%")

def calculate_dcf():
    investment, cash_flows, discount_rate=validate_inputs()
    if investment is None or discount_rate is None:
        return
    
    discounted_cash_flows=[cf/(1+discount_rate/100)**(i+1) for i, cf in enumerate(cash_flows)]
    npv=-investment+sum(discounted_cash_flows)
    pi=sum(discounted_cash_flows)/investment
    irr=npf.irr([-investment]+cash_flows)*100
    
    label_result.config(text=f"NPV: {npv:.2f}, PI: {pi:.2f}, IRR: {irr:.2f}%")
    for row in treeview.get_children():
        treeview.delete(row)
    for i, dcf in enumerate(discounted_cash_flows, start=1):
        treeview.insert("", "end", values=(i, f"{dcf:.2f}"))
    export_to_csv(discounted_cash_flows)

def export_to_csv(discounted_cash_flows):
    if not discounted_cash_flows:
        messagebox.showwarning("Export Error", "No discounted cash flows available to save.")
        return
    file_path=os.path.join(os.path.expanduser("~"), "Downloads", "discounted_cash_flows.csv")

    with open(file_path, mode="w", newline="") as file:
        writer=csv.writer(file)
        writer.writerow(["Year", "Discounted Cash Flow"])
        for i, dcf in enumerate(discounted_cash_flows, start=1):
            writer.writerow([i, f"{dcf:.2f}"])
    messagebox.showinfo("Export to CSV", f"Discounted cash flows have been saved to '{file_path}'.")

root=tk.Tk()
root.title("Capital Budgeting Calculator")
root.geometry("600x600")
root.configure(bg="#e8f0f2")

title_label=tk.Label(root, text="Capital Budgeting Calculator", bg="#e8f0f2", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

input_frame=tk.Frame(root, bg="#e8f0f2")
input_frame.pack(pady=10, padx=10)

tk.Label(input_frame, text="Initial Investment:", bg="#e8f0f2", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_investment=tk.Entry(input_frame, width=20, font=("Arial", 12))
entry_investment.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Cash Flows (comma-separated):", bg="#e8f0f2", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_cash_flows=tk.Entry(input_frame, width=20, font=("Arial", 12))
entry_cash_flows.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Discount Rate (%):", bg="#e8f0f2", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_discount_rate=tk.Entry(input_frame, width=20, font=("Arial", 12))
entry_discount_rate.grid(row=2, column=1, padx=5, pady=5)

button_frame=tk.Frame(root, bg="#e8f0f2")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Calculate Payback", command=calculate_payback, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=10)
tk.Button(button_frame, text="Calculate ARR", command=calculate_arr, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=5, pady=10)
tk.Button(button_frame, text="Calculate NPV, PI, IRR", command=calculate_dcf, bg="#FF5722", fg="white", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, padx=5, pady=10)

result_frame=tk.Frame(root, bg="#e8f0f2")
result_frame.pack(pady=10)

label_result=tk.Label(result_frame, text="Result will be displayed here", bg="#e8f0f2", font=("Arial", 14))
label_result.pack()

treeview_frame=tk.Frame(root, bg="#e8f0f2")
treeview_frame.pack(pady=10, padx=10)

columns=("Year", "Discounted Cash Flow")
treeview=ttk.Treeview(treeview_frame, columns=columns, show='headings', height=5)
treeview.heading("Year", text="Year")
treeview.heading("Discounted Cash Flow", text="Discounted Cash Flow")
treeview.column("Year", width=100)
treeview.column("Discounted Cash Flow", width=150)

treeview.pack()

root.mainloop()

