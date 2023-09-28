import time
from machine import Pin, PWM

# Helper function
def time_ms():
    return time.time_ns() // 1000000

# A class to handle buttons more easily.
class Button:
    _was_pressed = False
    _time_pressed = -1
    
    def __init__(self, pin_num, bounce_ms = 20):
        self._pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self._bounce_ms = bounce_ms
    
    def is_pressed(self):
        
        # NOTE: The value signal is inverted.
        
        if self._was_pressed:
            curr_time = time_ms()
            
            # If the time has exceeded the delay, check again.
            # If the button is still pressed, we have avoided bounce.
            if curr_time - self._time_pressed >= self._bounce_ms and not self._pin.value():
                return True
                print(curr_time - self._time_pressed)
                print(self._pin.value())
            
        else:
            # If the button was was pressed, record the time.
            if not self._pin.value():
                self._was_pressed = True
                self._time_pressed = time_ms()
            
        return False

# A class to keep track of individual LED PWMs.
class LightPWM: 
    def __init__(self, pin_num):
        self._pwm = PWM(Pin(pin_num, Pin.OUT), 10000)
    
    def duty(self, value):
        self._pwm.duty(value)
    
    # The lights should all turn off when the program ends.
    def deinit(self):
        self._pwm.deinit()

# A collection of lights that can do certain actions autonomously.
class LightBar:
    def __init__(self, pin_nums):
        self._pwms = [LightPWM(pin_num) for pin_num in pin_nums]
        self.reset()
    
    def reset(self):
        self._curr_light = len(self._pwms) - 1
        self.soft_reset()
    
    # Doesn't reset the position.
    def soft_reset(self):
        for pwm in self._pwms:
            pwm.duty(0)
    
    # Make the lights turn on and off individually in a loop.
    def light_mod(self, curr_time, delay_ms = 100):
        
        # If the delay has expired, switch the light to the next one.
        if curr_time >= delay_ms:
            self._pwms[self._curr_light].duty(0)
            self._curr_light = (self._curr_light + 1) % len(self._pwms)
            self._pwms[self._curr_light].duty(255)
    
    # Make the lights gradually turn off according to some pattern.
    def light_wave(self, curr_time, delay_ms = 100, pattern = [1023 >> i for i in range(10)]):
        
        # If the delay has expired, switch the light to the next one.
        if curr_time >= delay_ms:
            
            length = len(self._pwms)
            
            self._curr_light = (self._curr_light + 1) % length
            
            for i in range(length):
                self._pwms[i].duty(pattern[(self._curr_light - i) % length])

def main():
    # Pin setup is largely handled by the above classes.
    light_bar = LightBar([15, 2, 0, 4, 5, 18, 19, 21, 22, 23])
    button_mod = Button(33)
    button_wave = Button(32)
    
    while True:
        
        if button_mod.is_pressed():
            
            # Falling edge.
            # We don't want to immediately exit.
            while button_mod.is_pressed():
                time.sleep_ms(20)
            
            # Perform this behaviour until a button is pressed again.
            while not (button_wave.is_pressed() or button_mod.is_pressed()):
                time.sleep_ms(20)
                light_bar.light_mod(time_ms(), 100)
            
            # If the button was pressed again, use falling edge detection.
            while button_mod.is_pressed():
                time.sleep_ms(20)
            
            light_bar.soft_reset()
        
        if button_wave.is_pressed():
            
            # Falling edge.
            # We don't want to immediately exit.
            while button_wave.is_pressed():
                time.sleep_ms(20)
            
            # Perform this behaviour until a button is pressed again.
            while not (button_mod.is_pressed() or button_wave.is_pressed()):
                time.sleep_ms(20)
                light_bar.light_wave(time_ms(), 100)
            
            # If the button was pressed again, use falling edge detection
            while button_wave.is_pressed():
                time.sleep_ms(20)
            
            light_bar.soft_reset()

main()