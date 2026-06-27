from time import sleep, ticks_ms, ticks_diff

import config as cfg
from motors import stop
from sensors import follow_line_once, all_black, read_sensors
import maze


if cfg.CLEAR_SAVED_PATH_ON_BOOT:
    maze.delete_saved_path()

OPTIMIZED_PATH = maze.load_path()

if len(OPTIMIZED_PATH) > 0:
    MODE = "FAST_RUN"
else:
    MODE = "EXPLORE"

print("Maze solver started")
print("MODE:", MODE)



finish_start = None
lost_start = None
junction_lock = False

#Main loop

while True:
    loop_start = ticks_ms()

    values, error = follow_line_once()
  
    # Finish detection
    if all_black(values):
        if finish_start is None:
            finish_start = ticks_ms()

        elif ticks_diff(ticks_ms(), finish_start) > cfg.FINISH_TIME_MS:
            stop()
            print("FINISH DETECTED")

            if MODE == "EXPLORE":
                print("FINAL PATH:")
                print(maze.path)

                maze.save_path(maze.path)

                print("Saved path. Reboot for FAST_RUN.")

            else:
                print("FAST RUN FINISHED")

            break

    else:
        finish_start = None
      
    # Dead end detection
    if error is None:
        if lost_start is None:
            lost_start = ticks_ms()

        lost_time = ticks_diff(ticks_ms(), lost_start)

        if lost_time > cfg.DEAD_END_TIME_MS:
            stop()
            print("DEAD END")

            if MODE == "EXPLORE":
                maze.record("B")
                maze.mark_returning_from_dead_end()

            maze.turn_back()

            lost_start = None
            junction_lock = True
            continue

    else:
        lost_start = None

    # Junction detection
    if maze.is_real_junction(values) and not junction_lock:
        maze.handle_junction(MODE, OPTIMIZED_PATH)
        junction_lock = True

    if junction_lock:
        current_values = read_sensors()

        if not maze.is_real_junction(current_values):
            junction_lock = False

    # Loop timing
    elapsed = ticks_diff(ticks_ms(), loop_start)

    if elapsed < cfg.MAIN_LOOP_MS:
        sleep((cfg.MAIN_LOOP_MS - elapsed) / 1000)
