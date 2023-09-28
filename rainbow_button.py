import time
from machine import Pin, PWM
import neopixel

# Define custom colors here
colors = [
    (255, 0, 0),
    (255, 64, 0),
    (255, 192, 0),
    (0, 255, 0),
    (0, 64, 255),
    (128, 0, 255),
    (192, 0, 192)
]

brightness = 0.01

# The NeoPixel uses a different color range.
# Use this ratio to convert between the two.
ratio = 1023 / 255

# Set up RGBLED
rgb_pin_nums = [15, 2, 0]
rgb_pwms = [PWM(Pin(pin_num, Pin.OUT), 10000) for pin_num in rgb_pin_nums]

# NeoPixel Display, not to be confused with NumPy.
npd = neopixel.NeoPixel(Pin(19, Pin.OUT), 8)

# Button pin
button = Pin(13, Pin.IN, Pin.PULL_UP)

def set_color(color):
    color = (
        round(color[0] * brightness),
        round(color[1] * brightness),
        round(color[2] * brightness),
    )
    
    # The RGB channels are backwards: BGR
    for i in range(3):
        rgb_pwms[2 - i].duty(1023 - round(color[i] * ratio))
    
    npd.fill(color)
    npd.write()

# Initialize to no color.
set_color((0, 0, 0))

while True:
    for color in colors:        
        # Wait until the button is pressed.
        # Make sure to deal with bounce.
        while True:
            time.sleep_ms(20)
            
            if not button.value():
                time.sleep_ms(20)
                
                if not button.value():
                    break
        
        # When the button has been pressed, set the color.
        set_color(color)
        
        # Wait until the button is unpressed.
        while not button.value():
            time.sleep_ms(20)