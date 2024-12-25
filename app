import tkinter as tk
from tkinter import messagebox

# Example: User input parameters (expand this based on your full code)

class ConcreteMixDesignApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Concrete Mix Design Calculator")
        self.master.geometry("400x600")
        
        # Grade of Concrete
        self.grade_label = tk.Label(master, text="Grade of Concrete:")
        self.grade_label.grid(row=0, column=0, padx=10, pady=5)
        self.grade = tk.Entry(master)
        self.grade.grid(row=0, column=1, padx=10, pady=5)
        
        # Exposure Condition
        self.exposure_label = tk.Label(master, text="Exposure Condition:")
        self.exposure_label.grid(row=1, column=0, padx=10, pady=5)
        self.exposure = tk.Entry(master)
        self.exposure.grid(row=1, column=1, padx=10, pady=5)
        
        # Slump
        self.slump_label = tk.Label(master, text="Slump (mm):")
        self.slump_label.grid(row=2, column=0, padx=10, pady=5)
        self.slump = tk.Entry(master)
        self.slump.grid(row=2, column=1, padx=10, pady=5)
        
        # Size of Aggregate
        self.size_label = tk.Label(master, text="Size of Aggregate (mm):")
        self.size_label.grid(row=3, column=0, padx=10, pady=5)
        self.size = tk.Entry(master)
        self.size.grid(row=3, column=1, padx=10, pady=5)
        
        # Type of Aggregate
        self.type_label = tk.Label(master, text="Type of Aggregate:")
        self.type_label.grid(row=4, column=0, padx=10, pady=5)
        self.type = tk.Entry(master)
        self.type.grid(row=4, column=1, padx=10, pady=5)
        
        # Standard selection (ACI or IS)
        self.standard_label = tk.Label(master, text="Select Standard:")
        self.standard_label.grid(row=5, column=0, padx=10, pady=5)
        
        self.standard_var = tk.StringVar()
        self.standard_var.set("IS")  # default to IS
        self.standard_aci = tk.Radiobutton(master, text="ACI", variable=self.standard_var, value="ACI")
        self.standard_aci.grid(row=5, column=1, padx=10, pady=5)
        self.standard_is = tk.Radiobutton(master, text="IS", variable=self.standard_var, value="IS")
        self.standard_is.grid(row=5, column=2, padx=10, pady=5)
        
        # Button to calculate mix
        self.calculate_button = tk.Button(master, text="Calculate Mix Design", command=self.calculate_mix)
        self.calculate_button.grid(row=6, columnspan=3, pady=20)
    
    def calculate_mix(self):
        try:
            # Retrieve user input values
            grade = self.grade.get()
            exposure = self.exposure.get()
            slump = self.slump.get()
            size_of_aggregate = self.size.get()
            aggregate_type = self.type.get()
            standard = self.standard_var.get()
            
            # Call calculation functions based on selected standard (ACI or IS)
            if standard == "ACI":
                # Call ACI mix design functions (you need to implement those)
                pass
            else:
                # Call IS mix design functions
                pass
            
            # Display Result
            result_message = f"Concrete Mix Design:\n\nCement: {cement_content:.2f} kg\nWater: {water_content:.2f} kg\nCoarse Aggregate: {mass_CA:.2f} kg\nFine Aggregate: {mass_FA:.2f} kg\nChemical Admixture: {mass_chem_ad:.2f} kg"
            messagebox.showinfo("Mix Design Results", result_message)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

# Main App Window
root = tk.Tk()
app = ConcreteMixDesignApp(root)
root.mainloop()
