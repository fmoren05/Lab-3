"""
Script Name: closed_loop.py
Description: This script defines a ClosedLoopController class for implementing a closed-loop proportional controller for DC motors.
Author: Conor Schott, Fermin Moreno, Berent Baysal
Date: 2/22/24

Dependencies:
- utime
- pyb
- encoder_reader
- motor_control
"""

import utime
import pyb
import encoder_reader
import motor_control

class ClosedLoopController:
    """! Represents a closed-loop proportional controller for DC motors."""
    
    def __init__(self, Kp, setpoint):
        """! Initializes the ClosedLoopController object.
        
        Args:
            Kp (float): The proportional gain of the controller.
            setpoint (int): The initial setpoint for the motor position.
        """
        self.Kp = Kp
        self.setpoint = setpoint
        self.measured_output = 0
        self.time_buffer = []
        self.position_buffer = []
        self.start_time = None
        
    def run(self, measured_output):
        """! Runs the closed-loop control algorithm.
        
        Args:
            measured_output (int): The current measured position of the motor.
        
        Returns:
            float: The actuation value for the motor.
        """
        if self.start_time is None:
            self.start_time = utime.ticks_ms()

        self.measured_output = measured_output
        error = self.setpoint - self.measured_output
        actuation_signal = self.Kp * error

        if len(self.time_buffer) < 200:
            # Append time increments of 10 milliseconds
            current_time = (utime.ticks_ms() - self.start_time) // 10
            self.time_buffer.append(current_time)
            self.position_buffer.append(self.measured_output)

        return actuation_signal

    def set_setpoint(self, setpoint):
        """! Sets a new setpoint for the controller.
        
        Args:
            setpoint (int): The new desired position for the motor.
        """
        self.setpoint = setpoint

    def set_Kp(self, Kp):
        """! Sets a new proportional gain for the controller.
        
        Args:
            Kp (float): The new proportional gain value.
        """     
        self.Kp = Kp
        
    def print_results(self):
        """Prints the time and position buffers."""
        for time, position in zip(self.time_buffer, self.position_buffer):
            print(time, position, sep=", ")
            print(" ")
        
        
    
if __name__ == '__main__':
    """! Entry point of the script."""
    
    enc = encoder_reader.Encoder(8, pyb.Pin.board.PC6, pyb.Pin.board.PC7)  
    moe = motor_control.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)
    
    # Initialize closed-loop control object
    close = ClosedLoopController(0, 0.1)

    # Set target setpoint and proportional gain (Kp)
    target_setpoint = 50000
    close.set_setpoint(target_setpoint)
    Kp = 0.01
    close.set_Kp(Kp)
    
    # Main control loop
    while True:
        current_position = enc.read()
        output = close.run(current_position)
        moe.set_duty_cycle(output)
        utime.sleep_ms(10)  # Sleep for 10 milliseconds
