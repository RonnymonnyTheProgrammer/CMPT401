from time import sleep_ms
from machine import Pin

# Set up pins for output
r_led = Pin(12, Pin.OUT)
g_led = Pin(14, Pin.OUT)
b_led = Pin(33, Pin.OUT)

try:
    while True:
        # Red light turns on and off
        r_led.value(1)
        sleep_ms(1000)
        r_led.value(0)
        
        # Green light turns on and off
        g_led.value(1)
        sleep_ms(1000)
        g_led.value(0)
        
        # Blue light turns on and off
        b_led.value(1)
        sleep_ms(1000)
        b_led.value(0)
except:
    pass