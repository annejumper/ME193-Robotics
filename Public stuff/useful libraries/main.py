"""
Install first:
    pip install legoeducation
Then copy lelib.py from the SimpleLE repo into this project's folder.

"""

import time

import legoeducation as le
from lelib import colorSensor, controller, doubleMotor

# --- Bluetooth card info for your hardware -------------------------------
# Fill these in with the color/serial printed on your LEGO connection card.
# Valid values: le.LEGO_COLOR_RED, _YELLOW, _BLUE, _GREEN, _PURPLE,
# _MAGENTA, _AZURE, _ORANGE.
COLOR_SENSOR_CARD_COLOR = le.LEGO_COLOR_ORANGE
COLOR_SENSOR_CARD_SERIAL = 7552

CONTROLLER_CARD_COLOR = le.LEGO_COLOR_ORANGE
CONTROLLER_CARD_SERIAL = 7552

DOUBLE_MOTOR_CARD_COLOR = le.LEGO_COLOR_ORANGE
DOUBLE_MOTOR_CARD_SERIAL = 7552

WIGGLE_DEGREES = 90  # how far each motor swings per stroke
WIGGLE_SPEED = 50    # motor speed (%) for the orange wiggle

POLL_DELAY_S = 0.1  # seconds between reads

dm = None  # double motor, connected in main()



# --- Empty handler functions ----------------------------------------------
# Fill these in with whatever behavior you want.

def DoRed():
    print("red")



def DoYellow():
    print("yellow")



def DoBlue():
    print("blue")



def DoTeal():
    pass



def DoGreen():
    pass



def DoPurple():
    pass



def DoWhite():
    pass



def DoMagenta():
    pass



def DoOrange():
    # One back-and-forth cycle: the two motors turn 90 degrees in opposite
    # directions, then swap. The main loop calls this again while the sensor
    # still sees orange, so it keeps wiggling until orange is removed.
    print("orange")
    for left_dir, right_dir in (
        (le.MOTOR_MOVE_DIRECTION_CLOCKWISE, le.MOTOR_MOVE_DIRECTION_COUNTERCLOCKWISE),
        (le.MOTOR_MOVE_DIRECTION_COUNTERCLOCKWISE, le.MOTOR_MOVE_DIRECTION_CLOCKWISE),
    ):
        # Start the left motor without waiting, then block on the right so
        # both sides move at the same time.
        dm.motor_run_for_degrees(WIGGLE_DEGREES, direction=left_dir, motor=le.MOTOR_LEFT,
                                 speed=WIGGLE_SPEED, blocking=False)
        dm.motor_run_for_degrees(WIGGLE_DEGREES, direction=right_dir, motor=le.MOTOR_RIGHT,
                                 speed=WIGGLE_SPEED, blocking=True)



def DoAzure():
    pass



def DoNoColor():
    pass



def DoUnknownColor():
    pass



def DoLeftUp():
    pass



def DoLeftDown():
    pass



def DoLeftReleased():
    pass



def DoRightUp():
    pass



def DoRightDown():
    pass



def DoRightReleased():
    pass



# --- Dispatch helpers -------------------------------------------------

def handle_color(color_name):
    """Big switch statement on the color sensor's detected color."""
    match color_name:
        case "Red":
            DoRed()
        case "Yellow":
            DoYellow()
        case "Blue":
            DoBlue()
        case "Teal":
            DoTeal()
        case "Green":
            DoGreen()
        case "Purple":
            DoPurple()
        case "White":
            DoWhite()
        case "Magenta":
            DoMagenta()
        case "Orange":
            DoOrange()
        case "Azure":
            DoAzure()
        case "No color":
            DoNoColor()
        case _:
            DoUnknownColor()



def handle_controller(ctl):
    """Big switch statement on the controller's joystick state."""
    if ctl.left_up():
        left_state = "up"
    elif ctl.left_down():
        left_state = "down"
    else:
        left_state = "released"

    if ctl.right_up():
        right_state = "up"
    elif ctl.right_down():
        right_state = "down"
    else:
        right_state = "released"

    match left_state:
        case "up":
            DoLeftUp()
        case "down":
            DoLeftDown()
        case "released":
            DoLeftReleased()

    match right_state:
        case "up":
            DoRightUp()
        case "down":
            DoRightDown()
        case "released":
            DoRightReleased()



# --- Main loop -------------------------------------------------------------

def main():
    global dm

    sensor = colorSensor()
    sensor.connect(card_serial=COLOR_SENSOR_CARD_SERIAL, card_color=COLOR_SENSOR_CARD_COLOR)

    ctl = controller()
    ctl.connect(card_serial=CONTROLLER_CARD_SERIAL, card_color=CONTROLLER_CARD_COLOR)

    dm = doubleMotor()
    dm.connect(card_serial=DOUBLE_MOTOR_CARD_SERIAL, card_color=DOUBLE_MOTOR_CARD_COLOR)

    try:
        while True:
            handle_color(sensor.detect_color())
            handle_controller(ctl)
            time.sleep(POLL_DELAY_S)
    except KeyboardInterrupt:
        dm.stop()



if __name__ == "__main__":
    main()
