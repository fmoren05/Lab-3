# Authors: Conor Schott, Fermin Moreno, Berent Baysal
# Class: Encoder
# Data: 16th February 2024
# Brief Description: This class implements an encoder reader using Pyboard's Timer and Pin modules.

from pyb import Timer, Pin
import time



class Encoder:
    """!
    This class implements an encoder reader.
    """
    
    

    def __init__(self, timer, enc_pin_A, enc_pin_B):
        """!
        Creates an encoder reader by configuring encoder pins and timer for encoder counting mode.
        @param timer: Timer for encoder counting
        @param enc_pin_A: Encoder channel A pin
        @param enc_pin_B: Encoder channel B pin
        """
        self.timer = Timer(timer, prescaler=0, period=0xFFFF)
        self.enc_chA = self.timer.channel(1, Timer.ENC_AB, pin=enc_pin_A)
        self.enc_chB = self.timer.channel(2, Timer.ENC_AB, pin=enc_pin_B)
        self.cur_value = 0
        self.prev_value = self.timer.counter()
        
        #print("Creating an encoder reader")
        
        

    def read(self):
        """!
        This method reads the encoder values.
        @return: Tuple containing the current encoder count, delta, and channel A and B values
        """

        # Calculate delta based on channel A value change
        delta = self.timer.counter() - self.prev_value

        # Handle overflow and underflow conditions
        if delta > 32767:
            delta -= 65536
        elif delta < -32768:
            delta += 65535
        
        # Store current values for next iteration
        self.prev_value = self.timer.counter()
        self.cur_value += delta
        time.sleep(.1)
        
        return self.cur_value



    def zero(self):
        """!
        Sets the count to zero at the current position for both encoders.
        """
        self.cur_value = 0
        
        

if __name__ == '__main__':
    
    # Specify encoder pins and timers for encoder1 and encoder2
    encoder1 = Encoder(4, Pin.board.PB6, Pin.board.PB7)
    encoder2 = Encoder(8, Pin.board.PC6, Pin.board.PC7)
    
    while True:
        
        # Read encoder1 values
        encoder1_value = encoder1.read()
        
        # Read encoder2 values
        encoder2_value = encoder2.read()

        # Print out values for both encoders
        
        print("Encoder 1 Value:", encoder1_value)
        print()
        print("Encoder 2 Value:", encoder2_value)
        print()