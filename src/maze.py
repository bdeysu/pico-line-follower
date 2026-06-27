from time import sleep, ticks_ms, ticks_diff
import os

import config as cfg
from motors import move, stop
from sensors import read_sensors, b, all_black, active_count

#Path save/load

def delete_saved_path():
    try:
        os.remove(cfg.PATH_FILE)
        print("Deleted old path.txt")
    except:
        print("No old path.txt")


def save_path(path):
    try:
        f = open(cfg.PATH_FILE, "w")
        f.write("".join(path))
        f.close()
        print("Saved path:", path)
    except Exception as e:
        print("Save failed:", e)


def load_path():
    try:
        f = open(cfg.PATH_FILE, "r")
        data = f.read()
        f.close()

        result = []

        for char in data:
            if char in ["L", "S", "R", "B"]:
                result.append(char)

        print("Loaded path:", result)
        return result

    except:
        print("No saved path")
        return []


#Maze Detection

def is_real_junction(values):
    if all_black(values):
        return True

    count = active_count(values)

    # Real junction should include center and many sensors black
    if b(values, 2) and count >= 4:
        return True

    return False


def left_available(values):
    return b(values, 0) or b(values, 1)


def right_available(values):
    return b(values, 3) or b(values, 4)


def straight_available(values):
    return b(values, 1) or b(values, 2) or b(values, 3)


#Movement helpers

def forward_time(seconds):
    move(cfg.FORWARD_SPEED, cfg.FORWARD_SPEED)
    sleep(seconds)
    stop()
    sleep(0.05)


def turn_left():
    print("TURN LEFT")

    move(-cfg.TURN_SPEED, cfg.TURN_SPEED)
    sleep(0.28)

    start = ticks_ms()

    while True:
        values = read_sensors()

        if b(values, 1) or b(values, 2) or b(values, 3):
            break

        move(-cfg.TURN_SPEED, cfg.TURN_SPEED)
        sleep(0.01)

        if ticks_diff(ticks_ms(), start) > 1800:
            break

    stop()
    sleep(0.08)


def turn_right():
    print("TURN RIGHT")

    move(cfg.TURN_SPEED, -cfg.TURN_SPEED)
    sleep(0.28)

    start = ticks_ms()

    while True:
        values = read_sensors()

        if b(values, 1) or b(values, 2) or b(values, 3):
            break

        move(cfg.TURN_SPEED, -cfg.TURN_SPEED)
        sleep(0.01)

        if ticks_diff(ticks_ms(), start) > 1800:
            break

    stop()
    sleep(0.08)


def turn_back():
    print("TURN BACK")

    move(cfg.TURN_SPEED, -cfg.TURN_SPEED)
    sleep(0.50)

    start = ticks_ms()

    while True:
        values = read_sensors()

        if b(values, 1) or b(values, 2) or b(values, 3):
            break

        move(cfg.TURN_SPEED, -cfg.TURN_SPEED)
        sleep(0.01)

        if ticks_diff(ticks_ms(), start) > 2600:
            break

    stop()
    sleep(0.08)


def go_straight():
    print("GO STRAIGHT")
    forward_time(0.25)


#Path logic

path = []
fast_index = 0

# After a dead end, do not apply right-hand rule blindly again
returning_from_dead_end = False


def mark_returning_from_dead_end():
    global returning_from_dead_end
    returning_from_dead_end = True


def simplify_path():
    if len(path) < 3:
        return

    if path[-2] != "B":
        return

    angle = {
        "L": 270,
        "S": 0,
        "R": 90,
        "B": 180,
    }

    direction = {
        0: "S",
        90: "R",
        180: "B",
        270: "L",
    }

    total = angle[path[-3]] + angle[path[-2]] + angle[path[-1]]
    total = total % 360

    replacement = direction[total]

    path.pop()
    path.pop()
    path.pop()
    path.append(replacement)


def record(direction):
    path.append(direction)
    simplify_path()

    print("recorded:", direction)
    print("path:", path)


def choose_right_hand(left, straight, right):
    print("choices:", "L", left, "S", straight, "R", right)

    # Normal right-hand rule
    if right:
        return "R"
    elif straight:
        return "S"
    elif left:
        return "L"
    else:
        return "B"


def choose_after_dead_end(left, straight, right):
    print("BACKTRACK choices:", "L", left, "S", straight, "R", right)

    # After returning from a dead end, do not choose right first again.
    # Right often means going back to the already explored/start path.
    if left:
        return "L"
    elif straight:
        return "S"
    elif right:
        return "R"
    else:
        return "B"


def next_fast_command(optimized_path):
    global fast_index

    if fast_index >= len(optimized_path):
        print("FAST RUN ERROR: no more commands")
        return None

    direction = optimized_path[fast_index]
    fast_index += 1

    print("fast command:", direction)

    return direction


def execute(direction, should_record=True):
    if direction is None:
        stop()
        return

    if should_record:
        record(direction)

    if direction == "L":
        turn_left()
    elif direction == "R":
        turn_right()
    elif direction == "S":
        go_straight()
    elif direction == "B":
        turn_back()


#Junction handler

def handle_junction(mode, optimized_path):
    global returning_from_dead_end

    stop()
    sleep(0.04)

    # Move to center of junction
    move(35, 35)
    sleep(0.12)
    stop()
    sleep(0.04)

    values = read_sensors()
    print("junction values:", values)

    left = left_available(values)
    straight = straight_available(values)
    right = right_available(values)

    if mode == "EXPLORE":
        if returning_from_dead_end:
            direction = choose_after_dead_end(left, straight, right)
            returning_from_dead_end = False
        else:
            direction = choose_right_hand(left, straight, right)

        execute(direction, should_record=True)

    else:
        direction = next_fast_command(optimized_path)
        execute(direction, should_record=False)
