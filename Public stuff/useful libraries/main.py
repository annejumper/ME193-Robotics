"""
Install first:
    pip install legoeducation
Then copy lelib.py from the SimpleLE repo into this project's folder.

"""

import time

import legoeducation as le
from lelib import colorSensor, controller, doubleMotor, singleMotor

# --- Bluetooth card info for your hardware -------------------------------
# Fill these in with the color/serial printed on your LEGO connection card.
# Valid values: le.LEGO_COLOR_RED, _YELLOW, _BLUE, _GREEN, _PURPLE,
# _MAGENTA, _AZURE, _ORANGE.
COLOR_SENSOR_CARD_COLOR = le.LEGO_COLOR_PURPLE
COLOR_SENSOR_CARD_SERIAL = 6065

CONTROLLER_CARD_COLOR = le.LEGO_COLOR_PURPLE
CONTROLLER_CARD_SERIAL = 6065

DOUBLE_MOTOR_CARD_COLOR = le.LEGO_COLOR_PURPLE
DOUBLE_MOTOR_CARD_SERIAL = 6065

SINGLE_MOTOR_CARD_COLOR = le.LEGO_COLOR_PURPLE
SINGLE_MOTOR_CARD_SERIAL = 6065



POLL_DELAY_S = 0.1  # seconds between reads

RED_SPEED = 100          # % speed for the red spin
WIGGLE_DEGREES = 45      # how far each side swings on yellow
WIGGLE_SPEED = 50        # % speed for the yellow wiggle
PURPLE_DEGREES = 90      # how far each side swings on purple
PURPLE_SPEED = 50        # % speed for the purple wiggle
SINGLE_MOTOR_SPEED = 50  # % speed for the left-stick single motor spin

dm = doubleMotor()
sm = singleMotor()
sm_state = None  # "ccw", "cw" or "stopped": what the single motor was last told to do
last_color = None  # color seen on the previous poll



# --- Empty handler functions ----------------------------------------------
# Fill these in with whatever behavior you want.

def DoRed():
    print("red")
    dm.run(RED_SPEED)  # both sides full speed



def DoYellow():
    print("yellow")
    if last_color != "Yellow":
        # just switched to yellow: stop and make this spot the center
        dm.stop()
        dm.set_speed_left(WIGGLE_SPEED)
        dm.set_speed_right(WIGGLE_SPEED)
        dm.motor_reset_relative_position()
    # blocking=False starts the left side without waiting, so both sides
    # move together; the right side's call waits for its move to finish.
    # left forward, right back
    dm.motor_run_to_relative_position(WIGGLE_DEGREES, motor=le.MOTOR_LEFT, blocking=False)
    dm.motor_run_to_relative_position(-WIGGLE_DEGREES, motor=le.MOTOR_RIGHT)
    # left back, right forward
    dm.motor_run_to_relative_position(-WIGGLE_DEGREES, motor=le.MOTOR_LEFT, blocking=False)
    dm.motor_run_to_relative_position(WIGGLE_DEGREES, motor=le.MOTOR_RIGHT)



def DoBlue():
    print("blue")



def DoTeal():
    pass



def DoGreen():
    pass



def DoPurple():
    # One back-and-forth cycle: the two motors turn 90 degrees in opposite
    # directions, then swap. The main loop calls this again while the sensor
    # still sees purple, so it keeps wiggling until purple is removed.
    print("purple")
    for left_dir, right_dir in (
        (le.MOTOR_MOVE_DIRECTION_CLOCKWISE, le.MOTOR_MOVE_DIRECTION_COUNTERCLOCKWISE),
        (le.MOTOR_MOVE_DIRECTION_COUNTERCLOCKWISE, le.MOTOR_MOVE_DIRECTION_CLOCKWISE),
    ):
        # Start the left motor without waiting, then block on the right so
        # both sides move at the same time.
        dm.motor_run_for_degrees(PURPLE_DEGREES, direction=left_dir, motor=le.MOTOR_LEFT,
                                 speed=PURPLE_SPEED, blocking=False)
        dm.motor_run_for_degrees(PURPLE_DEGREES, direction=right_dir, motor=le.MOTOR_RIGHT,
                                 speed=PURPLE_SPEED, blocking=True)



def DoWhite():
    pass



def DoMagenta():
    pass



def DoOrange():
    pass



def DoAzure():
    pass



def DoNoColor():
    dm.stop()



def DoUnknownColor():
    pass



def set_single_motor(state):
    # Only send a command when the state changes, so holding the stick
    # doesn't resend the same command every poll.
    global sm_state
    if state == sm_state:
        return
    if state == "ccw":
        sm.motor_run(direction=le.MOTOR_MOVE_DIRECTION_COUNTERCLOCKWISE, speed=SINGLE_MOTOR_SPEED)
    elif state == "cw":
        sm.motor_run(direction=le.MOTOR_MOVE_DIRECTION_CLOCKWISE, speed=SINGLE_MOTOR_SPEED)
    else:
        sm.stop()
    sm_state = state



def DoLeftUp():
    set_single_motor("ccw")



def DoLeftDown():
    set_single_motor("cw")



def DoLeftReleased():
    set_single_motor("stopped")



def DoRightUp():
    pass



def DoRightDown():
    pass



def DoRightReleased():
    pass



# --- Dispatch helpers -------------------------------------------------

def handle_color(color_name):
    """Big switch statement on the color sensor's detected color."""
    global last_color
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
    last_color = color_name



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
    sensor = colorSensor()
    sensor.connect(card_serial=COLOR_SENSOR_CARD_SERIAL, card_color=COLOR_SENSOR_CARD_COLOR)

    ctl = controller()
    ctl.connect(card_serial=CONTROLLER_CARD_SERIAL, card_color=CONTROLLER_CARD_COLOR)

    dm.connect(card_serial=DOUBLE_MOTOR_CARD_SERIAL, card_color=DOUBLE_MOTOR_CARD_COLOR)

    sm.connect(card_serial=SINGLE_MOTOR_CARD_SERIAL, card_color=SINGLE_MOTOR_CARD_COLOR)

    try:
        while True:
            handle_color(sensor.detect_color())
            handle_controller(ctl)
            time.sleep(POLL_DELAY_S)
    except KeyboardInterrupt:
        dm.stop()
        sm.stop()



if __name__ == "__main__":
    main()
