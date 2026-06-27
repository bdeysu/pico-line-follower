# Pico Line Maze Robot

An autonomous Raspberry Pi Pico robot that follows a black line, solves a tape maze, records the path, then reuses the saved route for a faster second run.

The project uses MicroPython and is organized into separate modules.

## Demo

[![Robot Demo](https://img.youtube.com/vi/nxiaHqnXbtw/0.jpg)](https://www.youtube.com/watch?v=nxiaHqnXbtw)

## Overview

This robot follows a black tape track on a white surface and handles common maze features such as:

* Straight paths
* Curved paths
* Corners
* T-junctions
* Crossroads
* Dead ends
* Finish zone detection

During the first run, the robot explores the maze using a right-hand rule strategy. It records the decisions made at each junction, simplifies the path, and saves the final route to the Pico memory.

On the next startup, if a saved path exists, the robot automatically switches to fast-run mode and follows the stored route instead of solving the maze again.

## System Diagram

## System Diagram

```text
                    +----------------+
                    |  Battery Pack  |
                    +--------+-------+
                             |
                             | Battery +
                             v
             +---------------+----------------+
             |                                |
             v                                v
       +-----------+                    +------------+
       | Pico VSYS |                    | TB6612 VM  |
       +-----------+                    +------------+

Battery - / GND
      |
      +------------------+------------------+
                         |                  |
                         v                  v
                    +----------+      +-------------+
                    | Pico GND |      | TB6612 GND  |
                    +----------+      +-------------+


                  +----------------------+
                  |   Raspberry Pi Pico  |
                  +----------------------+
                     |       |        |
                     |       |        |
       GP0-GP6 ------+       |        +------ GP10-GP14
       motor control         |               line sensors
                             |
                             +------ GP16-GP19
                                    motor encoders


+----------------------+       +----------------------+
| 5x TCRT5000 Sensors  |       |  Hall Encoder Motors |
| L2 L1 C R1 R2        |       | Left A/B, Right A/B  |
+----------------------+       +----------------------+
          |                              |
          |                              |
          v                              v
   Pico digital inputs            Pico encoder inputs


              +-----------------------------+
              |         TB6612FNG           |
              +-----------------------------+
              | VCC  <- Pico 3V3 OUT        |
              | VM   <- Battery +           |
              | GND  <- Common GND          |
              | PWMA <- GP0                 |
              | AIN1 <- GP1                 |
              | AIN2 <- GP2                 |
              | PWMB <- GP3                 |
              | BIN1 <- GP4                 |
              | BIN2 <- GP5                 |
              | STBY <- GP6                 |
              +-----------------------------+
                    |                 |
                    v                 v
              Left Motor         Right Motor
```


## Features

* Line following using a PD-style controller
* Right-hand-rule maze exploration
* Dead-end detection and recovery
* Path recording
* Path simplification
* Saved route stored on the Pico as `path.txt`
* Automatic mode selection:

  * `EXPLORE` mode if no saved path exists
  * `FAST_RUN` mode if a saved path is found
* Modular MicroPython code structure

## Repository Structure

```text
pico-line-maze-robot/
│
├── README.md
├── src/
│   ├── main.py
│   ├── config.py
│   ├── motors.py
│   ├── sensors.py
│   └── maze.py
│
├── docs/
│   ├── system_diagram.png
│
├── media/
│   └── demo.mp4
│
├── .gitignore
└── LICENSE
```

## Operating Modes

### Explore Mode

If no saved path is found, the robot starts in explore mode.

In this mode, the robot:

1. Follows the line.
2. Detects junctions and dead ends.
3. Chooses directions using the right-hand rule.
4. Records each decision.
5. Simplifies the path when dead ends are encountered.
6. Saves the optimized route after detecting the finish zone.

### Fast-Run Mode

If a saved `path.txt` file exists, the robot starts in fast-run mode.

In this mode, the robot:

1. Loads the saved route.
2. Follows the line.
3. Uses the saved commands at junctions.
4. Reaches the finish without re-solving the maze.

## Path Saving

The optimized path is saved on the Pico as:

```text
path.txt
```


Each character represents a decision:

| Symbol | Meaning     |
| ------ | ----------- |
| `L`    | Turn left   |
| `R`    | Turn right  |
| `S`    | Go straight |
| `B`    | Turn back   |

## Resetting the Saved Path

To force the robot to explore again, delete `path.txt` from the Pico.

Alternatively, temporarily set this value in the code:

```python
CLEAR_SAVED_PATH_ON_BOOT = True
```

Run the program once, then set it back to:

```python
CLEAR_SAVED_PATH_ON_BOOT = False
```


## Future Improvements

Possible future upgrades:

* Add a button to clear the saved path
* Add an OLED display for current mode and path output
* Add encoder-based turn correction
* Add obstacle detection
* Improve maze solving with graph-based mapping
* Add camera-based line detection

## License

This project is released under the MIT License.
