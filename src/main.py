"""!
Script Name: main.py
Description: This script implements a closed-loop motor control system using an encoder for
feedback and USB communication for setting control parameters. It continuously reads control
parameters from a connected GUI via USB and adjusts the motor's behavior accordingly. 

Author: Conor Schott, Fermin Moreno, Berent Baysal
Date: 2/22/24

Dependencies:
- utime: MicroPython time module providing functions for time-related tasks.
- pyb: MicroPython module for accessing board-specific functions and hardware peripherals.
- encoder_reader: Custom module for interfacing with an encoder to read position feedback.
- motor_control: Custom module for controlling a motor using PWM signals.
- closed_loop: Custom module implementing a closed-loop control algorithm for motor position control.

Description:
1. Initialize the encoder and motor objects to interface with the hardware.
2. Establish communication with a graphical user interface (GUI) via USB to receive control parameters.
3. Continuously read control parameters from the GUI, including proportional gain (Kp) and setpoint.
4. Initialize a closed-loop controller with the received control parameters.
5. Enter a control loop where the motor's position is continuously monitored using the encoder feedback.
6. Based on the closed-loop control algorithm, calculate the appropriate control output to drive the motor.
7. Adjust the motor's behavior by setting the duty cycle according to the calculated control output.
8. Repeat the control loop for a predefined number of iterations to observe the motor's response to control inputs.
9. Print performance metrics of the closed-loop control system after the step response is completed.
10. Stop the motor and reset the encoder position for the next iteration.

""" 


# Import necessary modules
import utime
import pyb
import encoder_reader
import motor_control
import closed_loop

# Initialize encoder and motor objects
enc = encoder_reader.Encoder(8, pyb.Pin.board.PC6, pyb.Pin.board.PC7)
moe = motor_control.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)

# Initialize USB communication
gui_comm = pyb.USB_VCP()

while True:
    try:
        # Zero the encoder
        enc.zero()
        
        # Read proportional gain (Kp) from GUI
        while not gui_comm.any():
            pass
        kp_string = gui_comm.read(10).decode('utf-8')  # Read up to 10 bytes
        Kp = float(kp_string.strip())  # Convert string to float
        
        # Read setpoint from GUI
        while not gui_comm.any():
            pass
        setpoint_string = gui_comm.read(10).decode('utf-8')  # Read up to 10 bytes
        setpoint = float(setpoint_string.strip())  # Convert string to float
        
        # Initialize closed-loop controller
        close = closed_loop.ClosedLoopController(Kp, setpoint)

        # Main control loop
        iterations = 0
        while iterations <= 25:
            current_position = enc.read()
            output = close.run(current_position)
            moe.set_duty_cycle(output)
            iterations += 1
            utime.sleep_ms(10)

        # Printing results after step response completed
        close.print_results()
        moe.set_duty_cycle(0)
        enc.zero()
        
    except ValueError as e:
        print('ValueError:', e)
        enc.zero()
    except Exception as e:
        print('Exception:', e)
        # Additional exception handling or logging can be added here
        enc.zero()
