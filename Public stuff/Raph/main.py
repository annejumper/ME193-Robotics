"""
Install first:
    pip install legoeducation
lelib.py is already in this folder, so no copying needed.

Color template: a color sensor spins the Double Motor's left motor on Blue
(clockwise) and Orange (counterclockwise).
Fill in / change the Do...() handler functions for whatever behavior you want.

"""

import time

import legoeducation as le
from lelib import colorSensor, doubleMotor

# --- Bluetooth card info for your hardware -------------------------------
# Fill these in with the color/serial printed on your LEGO connection card.
# Valid values: le.LEGO_COLOR_RED, _YELLOW, _BLUE, _GREEN, _PURPLE,
# _MAGENTA, _AZURE, _ORANGE.
DOUBLE_MOTOR_CARD_COLOR = le.LEGO_COLOR_ORANGE
DOUBLE_MOTOR_CARD_SERIAL = 7552

COLOR_SENSOR_CARD_COLOR = le.LEGO_COLOR_ORANGE
COLOR_SENSOR_CARD_SERIAL = 7552

POLL_DELAY_S = 0.1   # seconds between reads
LEFT_MOTOR_DEGREES = 360  # how far the left motor turns on Blue/Orange



# --- Color handler functions ----------------------------------------------
# Each one gets the double motor so it can move the car.

def DoRed(dm):
    pass



def DoYellow(dm):
    pass



def DoBlue(dm):
    print("blue -> left motor clockwise")
    dm.motor_run_for_degrees(degrees=LEFT_MOTOR_DEGREES,
                             direction=le.MOTOR_MOVE_DIRECTION_CLOCKWISE,
                             motor=le.MOTOR_LEFT)



def DoTeal(dm):
    pass



def DoGreen(dm):
    pass



def DoPurple(dm):
    pass



def DoWhite(dm):
    pass



def DoMagenta(dm):
    pass



def DoOrange(dm):
    print("orange -> left motor counterclockwise")
    dm.motor_run_for_degrees(degrees=LEFT_MOTOR_DEGREES,
                             direction=le.MOTOR_MOVE_DIRECTION_COUNTERCLOCKWISE,
                             motor=le.MOTOR_LEFT)



def DoAzure(dm):
    pass



def DoNoColor(dm):
    pass



def DoUnknownColor(dm):
    pass



# --- Dispatch helpers -------------------------------------------------

def handle_color(dm, color_name):
    """Big switch statement on the color sensor's detected color."""
    match color_name:
        case "Red":
            DoRed(dm)
        case "Yellow":
            DoYellow(dm)
        case "Blue":
            DoBlue(dm)
        case "Teal":
            DoTeal(dm)
        case "Green":
            DoGreen(dm)
        case "Purple":
            DoPurple(dm)
        case "White":
            DoWhite(dm)
        case "Magenta":
            DoMagenta(dm)
        case "Orange":
            DoOrange(dm)
        case "Azure":
            DoAzure(dm)
        case "No color":
            DoNoColor(dm)
        case _:
            DoUnknownColor(dm)



# --- Main loop -------------------------------------------------------------

def main():
    dm = doubleMotor()
    dm.connect(card_serial=DOUBLE_MOTOR_CARD_SERIAL, card_color=DOUBLE_MOTOR_CARD_COLOR)

    sensor = colorSensor()
    sensor.connect(card_serial=COLOR_SENSOR_CARD_SERIAL, card_color=COLOR_SENSOR_CARD_COLOR)

    last_color = None
    try:
        while True:
            # Only react when the color changes, so a spin doesn't repeat
            # every loop while the sensor sits on the same color.
            color = sensor.detect_color()
            if color != last_color:
                handle_color(dm, color)
                last_color = color
            time.sleep(POLL_DELAY_S)
    except KeyboardInterrupt:
        pass
    finally:
        dm.stop()



if __name__ == "__main__":
    main()
