from digitalio import DigitalInOut, Direction, Pull
import pwmio
import board
from adafruit_debouncer import Debouncer
from time import time, sleep

# Keyboard imports
from usb_hid import devices
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Define some output pins:
LED_PIN = board.GP17
BUTTON_PIN = board.GP16

# Configure toggle button
button = DigitalInOut(BUTTON_PIN)
button.pull = Pull.DOWN
button.direction = Direction.INPUT
toggle_button = Debouncer(button)

# Configure the led pin as a pwd pin
led = pwmio.PWMOut(LED_PIN)

# Set up our toggle if the system is on or off
activated_toggle = 0

# Set up light controls
led_intensity = .1
led.duty_cycle = int(2**15 * led_intensity * activated_toggle)

# intialize keyboard
kbd = Keyboard(devices)

# Set up some flags
previous_button_status = False

# Set up timing
last_key_send = time()
TIME_TO_WAIT = 60

# Loop forever
while True:
    # Update the button value
    toggle_button.update()

    # Detect a falling edge
    if previous_button_status and not toggle_button.value:
        # Update light toggle to be on or off
        # We're doing this by using activated_toggle as an integer but checking it as a boolean ;)
        if not activated_toggle:
            activated_toggle += 1
        else:
            activated_toggle -= 1
        # Set the led duty_cycle
        led.duty_cycle = int(2**15 * led_intensity * activated_toggle)

    # If we're running then we should be sending keyboard commands
    if activated_toggle:
        # See if time waited is long enough
        if (time() - last_key_send) >= TIME_TO_WAIT:
            # Send an F24 since this key should no do anything
            kbd.send(Keycode.F24)
            print("SENDING KEYCODE")
            # Update last time the key was sent
            last_key_send = time()

    # Update the last button_status
    previous_button_status = toggle_button.value