from machine import Pin, PWM
import config as cfg


# TB6612FNG motor control

PWMA = PWM(Pin(cfg.PWMA_PIN))
AIN1 = Pin(cfg.AIN1_PIN, Pin.OUT)
AIN2 = Pin(cfg.AIN2_PIN, Pin.OUT)

PWMB = PWM(Pin(cfg.PWMB_PIN))
BIN1 = Pin(cfg.BIN1_PIN, Pin.OUT)
BIN2 = Pin(cfg.BIN2_PIN, Pin.OUT)

STBY = Pin(cfg.STBY_PIN, Pin.OUT)

PWMA.freq(1000)
PWMB.freq(1000)
STBY.value(1)


def clamp(x, low, high):
    return max(low, min(high, x))


def left_motor(speed):
    speed = clamp(speed * cfg.LEFT_DIR, -100, 100)

    if speed > 0:
        AIN1.value(1)
        AIN2.value(0)
    elif speed < 0:
        AIN1.value(0)
        AIN2.value(1)
    else:
        AIN1.value(0)
        AIN2.value(0)

    PWMA.duty_u16(int(abs(speed) * 65535 / 100))


def right_motor(speed):
    speed = clamp(speed * cfg.RIGHT_DIR, -100, 100)

    if speed > 0:
        BIN1.value(1)
        BIN2.value(0)
    elif speed < 0:
        BIN1.value(0)
        BIN2.value(1)
    else:
        BIN1.value(0)
        BIN2.value(0)

    PWMB.duty_u16(int(abs(speed) * 65535 / 100))


def move(left, right):
    left_motor(left)
    right_motor(right)


def stop():
    move(0, 0)
