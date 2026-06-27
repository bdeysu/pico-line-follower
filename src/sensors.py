from machine import Pin
from time import sleep
import config as cfg
from motors import move, clamp

# Sensor reading
sensors = []

for pin in cfg.SENSOR_PINS:
    sensors.append(Pin(pin, Pin.IN))


def read_sensors():
    values = []

    for sensor in sensors:
        total = 0

        for i in range(5):
            total += sensor.value()
            sleep(0.0007)

        if total >= 3:
            values.append(1)
        else:
            values.append(0)

    return values


def b(values, index):
    return values[index] == cfg.BLACK


def all_black(values):
    return values == [
        cfg.BLACK,
        cfg.BLACK,
        cfg.BLACK,
        cfg.BLACK,
        cfg.BLACK,
    ]


def no_line(values):
    return cfg.BLACK not in values


def active_count(values):
    count = 0

    for value in values:
        if value == cfg.BLACK:
            count += 1

    return count


#Line following

last_error = 0
previous_error = 0


def line_error(values):
    global last_error

    b0 = b(values, 0)  # L2
    b1 = b(values, 1)  # L1
    b2 = b(values, 2)  # C
    b3 = b(values, 3)  # R1
    b4 = b(values, 4)  # R2

    if no_line(values):
        return None

  
    if b0 and not b3 and not b4:
        error = -5
    elif b0 and b1:
        error = -4
    elif b1 and b2 and not b3:
        error = -2
    elif b1 and not b3 and not b4:
        error = -3
    elif b2 and not b1 and not b3:
        error = 0
    elif b1 and b2 and b3:
        error = 0
    elif b3 and b2 and not b1:
        error = 2
    elif b3 and not b0 and not b1:
        error = 3
    elif b4 and b3:
        error = 4
    elif b4 and not b0 and not b1:
        error = 5
    else:
        weights = [-5, -2, 0, 2, 5]
        total = 0
        count = 0

        for i in range(5):
            if values[i] == cfg.BLACK:
                total += weights[i]
                count += 1

        error = total / count

    error += cfg.LINE_OFFSET
    last_error = error

    return error


def follow_line_once():
    global previous_error

    values = read_sensors()
    error = line_error(values)

    if error is None:
        # Corner recovery
        if last_error < 0:
            move(-34, 46)
        else:
            move(46, -34)

        return values, None

    derivative = error - previous_error
    previous_error = error

    correction = cfg.KP * error + cfg.KD * derivative

    base = cfg.BASE_SPEED - abs(error) * 3.2
    base = clamp(base, cfg.MIN_SPEED, cfg.BASE_SPEED)

    left_speed = base + correction
    right_speed = base - correction

    left_speed = clamp(left_speed, -cfg.MAX_SPEED, cfg.MAX_SPEED)
    right_speed = clamp(right_speed, -cfg.MAX_SPEED, cfg.MAX_SPEED)

    move(left_speed, right_speed)

    return values, error
