import time
from machine import Pin

# The LED is the output, the buttons are inputs.
led = Pin(2, Pin.OUT)
button_on = Pin(12, Pin.IN, Pin.PULL_UP)
button_off = Pin(14, Pin.IN, Pin.PULL_UP)

def wait_for_button(pin, reversed = False):
    while True:
        time.sleep_ms(20)
        
        print(pin.value())
        
        # Every 20 ms, check if the button is pressed.
        if pin.value() != reversed:
            
            # Wait first.
            time.sleep_ms(20)
                
            # Is it still pressed? If so, we have avoided bounce.
            if pin.value() != reversed:
                return

try:
    while True:
        # The light should start off.
        led.value(0)
        wait_for_button(button_on, True)
        led.value(1)
        wait_for_button(button_off, True)
except:
    pass