#
# File Name: Res_to_Temp.py
# By: Angel Martinez
#
# Last Modified: 03/24/23
#
# Description:
# Creates a simple UI that can convert resistance from SRS SIM921 AC Resistance Bridge to temperature of RuO
# thermocouple from Specific Heat Probe
#

import math

import tkinter as tk
import tkinter.font
from tkinter import messagebox

# Initial Resistance (Ohms)
r0 = 77350

# a coefficients
a0 = 0.27007140
a1 = 0.07323249
a2 = 1.02198090
a3 = -1.9558035
a4 = 3.48898940
a5 = -4.41759550
a6 = 3.69768560
a7 = -1.78710350
a8 = 0.38218430


# Conversion Functions
def temp_function(r):
    ans_1 = 1 / (a0 + a1 * math.pow(math.log(r / r0), .25) + a2 * math.pow(math.log(r / r0), 1)
                 + a3 * math.pow(math.log(r / r0), 2) + a4 * math.pow(math.log(r / r0), 3)
                 + a5 * math.pow(math.log(r / r0), 4) + a6 * math.pow(math.log(r / r0), 5)
                 + a7 * math.pow(math.log(r / r0), 6) + a8 * math.pow(math.log(r / r0), 7)) ** 4
    return ans_1


# Creates zero function
def zero_func(r, temp):
    return temp_function(r) - temp


# Use the bisection method to solve for x
def res_function(temp):
    # Define the initial interval
    a, b = r0, 4 * r0
    # Define the tolerance for convergence
    tol = 1e-11
    # Define the maximum number of iterations
    max_iter = 100000

    for i in range(max_iter):
        c = (a + b) / 2  # Define the midpoint of the interval
        if zero_func(c, temp) == 0 or (b - a) / 2 < tol:
            return c  # Return the solution
        elif zero_func(a, temp) * zero_func(c, temp) < 0:
            b = c
        else:
            a = c
    return None


# App Mode
class App:
    def __init__(self):
        # Create Windows
        self.window = tk.Tk()
        self.window.title("Resistance to Temperature")

        self.window.geometry("370x440")
        self.window.resizable(width=False, height=False)
        self.w_font = tkinter.font.nametofont("TkDefaultFont")
        self.w_font.config(size=13)

        # Stores a coefficients as Strings
        self.coefficients = "a0 = " + str(a0) + "\n" + \
                            "a1 = " + str(a1) + "\n" + \
                            "a2 = " + str(a2) + "\n" + \
                            "a3 = " + str(a3) + "\n" + \
                            "a4 = " + str(a4) + "\n" + \
                            "a5 = " + str(a5) + "\n" + \
                            "a6 = " + str(a6) + "\n" + \
                            "a7 = " + str(a7) + "\n" + \
                            "a8 = " + str(a8) + "\n"

        # Saves Resistance Entry Value
        res_cur = tk.DoubleVar()

        # Creates Label String Variables
        self.res_0 = str(r0) + " Ω"
        self.temp = ""
        self.temp_percent = 15 * "   " + " "
        self.res_1_val = 15 * "  " + " "

        # New strings variables given entry resistance (button function)
        def chg_temp():
            r_new = self.e1.get()
            r_new = float(r_new)
            print(r_new)

            if r_new >= 4*r0 or r_new <= r0:
                messagebox.showerror('Enter Another Value', 'Enter Value Between 77,350 and 309,400.')
                pass

            out = temp_function(r_new)
            self.temp = str(out) + " K"

            self.temp_percent = str(1.01 * out) + " K"

            out_res = res_function(1.01 * out)
            self.res_1_val = str(out_res) + " Ω"

            self.temp_label_1 = tk.Label(self.low, text=self.temp)
            self.temp_label_1.grid(row=1, column=1)

            self.temp_1_label_1 = tk.Label(self.low_low, text=self.temp_percent)
            self.temp_1_label_1.grid(row=0, column=1, pady=5)

            self.res_1_out = tk.Label(self.low_low, text=self.res_1_val)
            self.res_1_out.grid(row=1, column=1, padx=5, pady=5)

        # Create Frames
        self.top = tk.Frame(self.window, width=425, height=125)
        self.top.grid(row=0, column=0, padx=5, pady=5)

        self.mid = tk.Frame(self.window, width=425, height=200, highlightbackground="black",
                            highlightthickness=1)
        self.mid.grid(row=1, column=0, padx=5, pady=5)

        self.low = tk.Frame(self.window, width=425, height=100, highlightbackground="black",
                            highlightthickness=1)
        self.low.grid(row=2, column=0, padx=5, pady=5)

        self.low_low = tk.Frame(self.window, width=425, height=100, highlightbackground="black",
                                highlightthickness=1)
        self.low_low.grid(row=3, column=0, padx=5, pady=5)

        # Labels
        self.title = tk.Label(self.top, text="Ohms To Kelvin", font=("Ariel", 25, "bold"))
        self.title.grid(row=0, column=0)

        # Mid
        self.res_label = tk.Label(self.mid, text="Res_0 = " + self.res_0, font=("Ariel", 12, "bold"))
        self.res_label.grid(row=0, column=0)

        self.a_label = tk.Label(self.mid, text=self.coefficients, font=("Ariel", 8))
        self.a_label.grid(row=1, column=0)

        # Low
        self.res_ask = tk.Label(self.low, text="Resistance =  ")
        self.res_ask.grid(row=0, column=0, padx=5, pady=5)

        self.temp_label = tk.Label(self.low, text="Temperature = ")
        self.temp_label.grid(row=1, column=0, padx=5, pady=5)

        self.temp_label_1 = tk.Label(self.low, text=self.temp)
        self.temp_label_1.grid(row=1, column=1, pady=5)

        # Low_Low
        self.temp_1_label = tk.Label(self.low_low, text="1% Increase = ")
        self.temp_1_label.grid(row=0, column=0, pady=5)

        self.temp_1_label_1 = tk.Label(self.low_low, text=self.temp_percent)
        self.temp_1_label_1.grid(row=0, column=1, pady=5)

        self.res_1 = tk.Label(self.low_low, text="Resistance =  ")
        self.res_1.grid(row=1, column=0, padx=5, pady=5)

        self.res_1_out = tk.Label(self.low_low, text=self.res_1_val)
        self.res_1_out.grid(row=1, column=1, padx=5, pady=5)

        # Entry and Button
        self.e1 = tk.Entry(self.low, width=30, textvariable=res_cur)
        self.e1.grid(row=0, column=1)

        self.button = tk.Button(self.low, text="Go", font=("Ariel", 10), width=2, height=0, activebackground='#00ff00',
                                command=chg_temp)
        self.button.grid(row=0, column=2, padx=5, pady=5)

        # Runs Mainloop
        self.window.mainloop()


App()

# # Continuous Mode, from terminal
# while True:
#     print()
#
#     res_1 = float(input("Resistance Reading: "))
#
#     tf = temp_function(res_1)
#     print(tf)
#     rf = res_function(tf)
#     print(rf)
#
#     print()
#
#     print("1%:\n"+str(1.01*tf))
#     rf = res_function(1.01*tf)
#     print(rf)
#
