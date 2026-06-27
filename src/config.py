# Motor pins: TB6612FNG

PWMA_PIN = 0
AIN1_PIN = 1
AIN2_PIN = 2

PWMB_PIN = 3
BIN1_PIN = 4
BIN2_PIN = 5

STBY_PIN = 6

LEFT_DIR = -1
RIGHT_DIR = -1


# TCRT5000s

# Sensor order: L2, L1, C, R1, R2
SENSOR_PINS = [10, 11, 12, 13, 14]

BLACK = 1


# Line following tuning

BASE_SPEED = 50
MIN_SPEED = 30
MAX_SPEED = 82

KP = 9.5
KD = 18.0

# If robot rides one side:
# try +0.5, +1.0 or -0.5, -1.0
LINE_OFFSET = 0.0

# Movement tuning

TURN_SPEED = 43
FORWARD_SPEED = 42

# Timing

FINISH_TIME_MS = 800
DEAD_END_TIME_MS = 850

MAIN_LOOP_MS = 25

# Path saving

PATH_FILE = "path.txt"

# Set True once to erase old saved path.
# Run once, then set back to False.
CLEAR_SAVED_PATH_ON_BOOT = False
