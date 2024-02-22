"""
Script Name: motor_control.py
Description: This script defines a MotorDriver class for controlling motors in an ME405 kit.
Author: Conor Schott, Fermin Moreno, Berent Baysal
Date: 2/22/24

Dependencies:
- pyb
"""

from pyb import *

class MotorDriver:
    """!
    This class implements a motor driver for an ME405 kit.
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """!
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety.
        @param en_pin: Pin for motor enable
        @param in1pin: Pin for IN1
        @param in2pin: Pin for IN2
        @param timer: Timer for PWM
        """
        self.en_pin = Pin(en_pin, Pin.OUT_OD, Pin.PULL_UP)
        self.in1 = Pin(in1pin, Pin.OUT_PP)
        self.in2 = Pin(in2pin, Pin.OUT_PP)
        self.tim = Timer(timer, freq=20_000)
        self.ch1 = self.tim.channel(1, Timer.PWM, pin=self.in1)
        self.ch2 = self.tim.channel(2, Timer.PWM, pin=self.in2)
        self.set_duty_cycle(0)
   
        #print("Creating a motor driver")

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level: A signed integer holding the duty
               cycle of the voltage sent to the motor
        """
        
        
        if level < 0:
            self.ch1.pulse_width_percent(0)  # Set CH1 to 0% duty cycle
            self.ch2.pulse_width_percent(abs(level))  # Use CH2 for torque control
        elif level > 0:
            self.ch2.pulse_width_percent(0)  # Set CH2 to 0% duty cycle
            self.ch1.pulse_width_percent(abs(level))  # Use CH1 for torque control
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)
            
        self.en_pin.high()  # Enable the motor
        
if __name__ == '__main__':

    moe = MotorDriver(Pin.board.PC1, Pin.board.PA0, Pin.board.PA1, 5)
    # Test with various duty cycles
    moe.set_duty_cycle(42)  # Forward at 50% duty cycle
    delay(5000)
   
    moe.set_duty_cycle(-42)  # Reverse at 50% duty cycle
    delay(5000)

    moe.set_duty_cycle(0)  # Stop the motor
