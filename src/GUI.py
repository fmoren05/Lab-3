"""
Script Name: GUI.py
Description: This script creates a Tkinter GUI for plotting data received from a serial device and interacting with the plot.
Author: Conor Schott, Fermin Moreno, Berent Baysal
Date: 2/22/24

Dependencies:
- tkinter
- matplotlib
- serial
- time
"""

import tkinter
from tkinter.simpledialog import askfloat
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import serial
import time

def get_user_input():
    """!
    Prompt the user to enter KP and Setpoint values.

    Returns:
        kp (float): The KP value entered by the user.
        setpoint (float): The Setpoint value entered by the user.
    """
    kp = askfloat("Input", "Enter KP:")
    if kp is not None:
        setpoint = askfloat("Input", "Enter Setpoint:")
        if setpoint is not None:
            return kp, setpoint
    return None, None

def plot_example(plot_axes, plot_canvas, xlabel, ylabel, kp, setpoint):
    """!
    Plot example data received from a serial device.

    Args:
        plot_axes (matplotlib.axes.Axes): The axes to plot the data on.
        plot_canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): The canvas to draw the plot on.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        kp (float): The KP value for the plot.
        setpoint (float): The Setpoint value for the plot.
    """
    serial_port = 'COM9'
    baud_rate = 115200
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    
    # Send KP and Setpoint values to the serial device
    ser.write(b'\x04')
    while not ser.inWaiting():
        pass
    time.sleep(0.1)
    temp = str(kp).encode('utf-8')
    ser.write(temp)
    time.sleep(0.1)
    temps = str(setpoint).encode('utf-8')
    ser.write(temps)
    
    # Read data from the serial device
    time_data = []
    position_data = []
    while not ser.inWaiting():
        pass
    line = ser.readline().rstrip().decode('utf-8')  # Read a line of text
    stop_condition = 0
    while stop_condition <= 54:
        try:
            print(line)
            if "," in line:  # Check if the line contains a comma
                time_data_str, position_data_str = line.split(",") # Split the line into parts
                times_data_flt = float(time_data_str)
                position_data_flt = float(position_data_str)
            
                time_data.append(times_data_flt)
                position_data.append(position_data_flt)
        except ValueError as e:
            print("ValueError:", e)
        except Exception as e:
            print("Exception:", e)
        finally:
            line = ser.readline().rstrip().decode('utf-8')
            stop_condition += 1

    plot_axes.plot(time_data, position_data)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()
    ser.close()

def tk_matplot(plot_function, input_fun, xlabel, ylabel, title):
    """!
    Create a Tkinter GUI with a plot and buttons for interacting with the plot.

    Args:
        plot_function (function): The function to call when plotting data.
        input_fun (function): The function to call when getting user input.
        xlabel (str): The label for the x-axis of the plot.
        ylabel (str): The label for the y-axis of the plot.
        title (str): The title of the Tkinter window.
    """
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    fig = Figure()
    axes = fig.add_subplot()

    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel,
                                                              *input_fun()))


    canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)
    toolbar.grid(row=1, column=0, columnspan=4)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=3)

    tkinter.mainloop()

if __name__ == "__main__":
    tk_matplot(plot_example, get_user_input, 
               xlabel="Time (ms)",
               ylabel="Position",
               title="Step Response")
