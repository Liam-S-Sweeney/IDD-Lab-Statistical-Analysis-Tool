import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from descriptive_csv_generator import master_descriptive_csv_generator, all_single_var_descriptive_csv_generator
from multivariate_exploration import explore_multi_variables, multivariate_visualizations, correlational_analysis

# Dataframe Selection
file_path = r'data_files\VT Teen Study Waves 1,2,3,4 merged all youth variables.csv'
raw_df = pd.read_csv(file_path) 
numeric_df = raw_df.apply(pd.to_numeric, errors='coerce').replace(-99, np.nan).replace(-999, np.nan)

# All variable options
var_options = [var for var in numeric_df.columns]

# Create window
root = tk.Tk()
root.title("IDD Lab Data Analysis Tool")
root.geometry('500x500')

# Root layout
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

top_frame = ttk.Frame(root)
top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)

dropdown_frame = ttk.Frame(root)
dropdown_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
dropdown_frame.columnconfigure(0, weight=1)

bottom_frame = ttk.Frame(root)
bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)

# Create variable combobox class
class SearchableDropdown:
    def __init__(self, parent, options, row):
        self.str_var = tk.StringVar()
        self.options = options
        self.dropdown = ttk.Combobox(parent, values=options, textvariable=self.str_var)
        self.dropdown.grid(row=row, column=0, pady=4, sticky="ew")
        self.str_var.trace_add("write", self.check_input)

    def check_input(self, *args):
        typed = self.str_var.get()

        if typed == "":
            self.dropdown['values'] = self.options
        else:
            filtered = [item for item in self.options if item.lower().startswith(typed.lower())]
            self.dropdown['values'] = filtered

    def get_value(self):
        return self.str_var.get().strip()

# Determine how many variables are wanted with spinbox
dropdown_widgets = []

def update_dropdowns(*args):
    global dropdown_widgets

    desired = int(vc_str_var.get())
    current = len(dropdown_widgets)

    if desired > current:
        for _ in range(desired-current):
            dropdown_widgets.append(
                SearchableDropdown(parent=dropdown_frame, 
                                   options=var_options,
                                   row=len(dropdown_widgets)
                                   )
            )

    elif desired < current:
        for _ in range(current - desired):
            w = dropdown_widgets.pop()
            w.dropdown.destroy()

def get_selected_values():
    selected_values = [w.get_value() for w in dropdown_widgets if w.get_value()]
    selected_values = list(dict.fromkeys(selected_values))  
    return selected_values

def run_explore_multivariate():
    selected = [w.get_value() for w in dropdown_widgets if w.get_value()]
    selected = list(dict.fromkeys(selected))  

    if not selected:
        messagebox.showwarning("No variables selected", 
                               "Select at least 1 variable.")
        return

    explore_multi_variables(*selected)

def run_multivariate_vis():
    selected = [w.get_value() for w in dropdown_widgets if w.get_value()]
    selected = list(dict.fromkeys(selected)) 

    if len(selected) < 2:
        messagebox.showwarning(
            "Not enough variables",
            "Please select at least two variables."
        )
        return

    multivariate_visualizations(*selected)

def run_multivariate_corr():
    selected = [w.get_value() for w in dropdown_widgets if w.get_value()]
    selected = list(dict.fromkeys(selected)) 

    if len(selected) < 2:
        messagebox.showwarning(
            "Not enough variables",
            "Please select at least two variables."
        )
        return

    correlational_analysis(*selected)

vc_str_var = tk.StringVar(value='1')

var_count_selection = tk.Spinbox(top_frame, from_=1, to=10, width=5, 
                                 textvariable=vc_str_var, 
                                 command=update_dropdowns
                                 )
var_count_selection.grid(row=2, column=0, columnspan=3, pady=(10, 0))

vc_label = ttk.Label(top_frame, text='Number of Variables?')
vc_label.grid(row=1,column=0, columnspan=3, pady=(10, 0))

vc_str_var.trace_add('write', update_dropdowns)

# Number of variable dropdowns present initially
update_dropdowns()

# Confirm button click


# Multivariate Buttons
btn_explore_multi_var = tk.Button(top_frame, 
                                  text='Multivariate Exploration',
                            command=run_explore_multivariate)
btn_explore_multi_var.grid(row=0, column=0, padx=5, sticky="ew")

btn_multi_vis = tk.Button(top_frame, text='Multivariate Visualization',
                           command=run_multivariate_vis)
btn_multi_vis.grid(row=0, column=1, padx=5, sticky="ew")

btn_multi_corr = tk.Button(top_frame, text='Multivariate Visualization',
                           command=run_multivariate_corr)
btn_multi_corr.grid(row=0, column=2, padx=5, sticky="ew")

# Full-Data Buttons
btn_master_desc = tk.Button(bottom_frame, 
                            text='Master Descriptive CSV Generator',
                            command=master_descriptive_csv_generator)
btn_master_desc.grid(row=0, column=0, padx=5, sticky="ew")

btn_all_single = tk.Button(bottom_frame, 
                           text='All Single Var Descriptive CSV Generator',
                           command=all_single_var_descriptive_csv_generator)
btn_all_single.grid(row=0, column=1, padx=5, sticky="ew")

# Start GUI loop
root.mainloop()