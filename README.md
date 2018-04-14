# RPiSense

https://github.com/dbullockphd/RPiSense

This package was written for the purpose of making easy demonstrations with the Sense HAT for Raspberry Pi.

## Installation and Setup

Anytime you are looking to install something on your Raspberry Pi, make sure that everything is up-to-date. Open the Terminal (look for it along the top toolbar) and type this command:

```bash
sudo apt-get upgrade
```

This will check the package index of applications installed on the system and generate an update priority list.

```bash
sudo apt-get update
```

Type "Y" and hit enter to accept the changes if prompted. This will actually install those updates.

If your Raspberry Pi is running low on disk space, you may also want to run a cleanup.

```bash
sudo apt-get autoremove
```

### Minimal Install

Follow these steps to make sure that `RPiSense` works correctly.

Download this source code to the Raspberry Pi:

```bash
mkdir -p /home/pi/src
git clone https://github.com/dbullockphd/RPiSense
```

Sense HAT has a Python API that allows you to communicate with it easily. This installation is required for `RPiSense` to work, so make sure you have it.

```bash
sudo apt-get install sense-hat
```

### Other Recommended Installations

`RPiSense` was written to support an electronics and computer programming course. The Raspberry Pi's were installed with configurations and software for the touchscreen, an Arduino board, and data visualizations projects. If you are not interested in these, then you can skip this section.

This installs a touchscreen keyboard:

```bash
sudo apt-get install matchbox-keyboard
```

If you are using the touchscreen keyboard, you may also want the configuration file that was sent out with the Raspberry Pi's as part of the course.

```bash
mkdir -p /home/pi/.matchbox
cp /home/pi/src/RPiSense/configs/keyboard.xml /home/pi/.matchbox/
```

If you want to use Arduino with the Raspberry Pi, you need the IDE:

```
sudo apt-get install arduino
```

Part of the computer programming course is to map some weather programs, so `matplotlib` is also recommended:

```
sudo pip install python-matplotlib
```

### Environment Variables

To take advantage of the macros on the system, it is recommended that you add a line to a launch script whenever Terminal is opened.

```bash
echo "source /home/pi/src/RPiSense/setup.sh" >> /home/pi/.bash_aliases
```

## Macros

The main purpose of `RPiSense` is to have macros for the Sense HAT that can quickly demonstrate some of the features of the Sense Hat. This section covers some of the commands that you can use.

Type the following into a Terminal window and observe the results:

```bash
sensehat color --bg red
sensehat scroll --message Hello World
sensehat date --bg blue --fg white
```

You should see that the first command displays red pixels on the LED matrix, the second has scrolling text that says "Hello World", and the third shows the date in white lettering on a blue background. Available commands are:

- `clear` -- Clear the LED matrix. This is useful if you interrupted a script that was controlling the LED matrix.
- `color` -- Display a solid color across all pixels in the LED matrix.
- `letter` -- Display a single letter to the LED matrix.
- `scroll` -- Display a scrolling text message across the LED matrix.
- `ip` -- Display the current IP address on the LED matrix.
- `date` -- Display the current date.
- `time` -- Display the current time.
- `datetime` -- Display the current date and time.
- `temperature` -- Display the current temperature.
- `pressure` -- Display the current pressure.
- `humidity` -- Display the current humidity.
- `level` -- Display the tilt of the Sense HAT in the style of a bubble level.
- `compass` -- Display the direction of North
- `repeat` -- Play a game of repetition.

The macros also have a few options defined by the macro. If you are not sure what options are available, try the help option:

```bash
sensehat --help
```

The most important for demonstrations are `--fg` and `--bg` options, which are the foreground and background colors, respectively. When a macro calls for text to be displayed, it will be shown in the foreground color on top of a background color.

## Classes and Functions

There are a few classes that are written to support the execution of the `sensehat` macro.

### Colors.py

This is a handle for named colors so that you can reference colors by name rather than RGB integers. The class reads a CSV file containing information pulled from `matplotlib`.

The database of colors is in the file `colors.csv`. This contains the 8-bit integer for red (r), green (g), blue (b), hue (h), saturation (s), value (v), hue (H), luminosity (L), and saturation (S) and a character string for the name of the color.

Instantiate the class by specifying a sort order and whether to sort by ascending or descending values.

```python
from RPiSense.Colors import Colors
c1 = Colors (order=('r','g','b'), ascending=True)
c2 = Colors (order=('L', 'H', 'S'), ascending=True)
```

You can obtain the 8-bit integers for a specific color name by using a dictionary-like reference. This returns a tuple for the RGB values.

```python
print c1['blue']
print c1['green']
```

If you want 8-bit integers for other color modes, the `fetch` method returns a tuple for the mode you specify.

```python
print c1.fetch ('blue', mode='hsv')
print c1.fetch ('blue', mode='HLS')
```

If you want to randomly select a color, use the `random` method.

```python
print c1.random (mode='rgb')
print c1.random (mode='rgb')
print c1.random (mode='rgb')
```

This class was written to support several commands in the `sensehat` macro.

### Compass.py

This class takes raw information from the compass and displays a red dot in the direction of North along a blue circle.

Instantiate the class by specifying a reference to the Sense HAT API.

```python
from sense_hat import SenseHat
from RPiSense.Compass import Compass
sense = SenseHat ()
c = Compass (sense)
c.Update ()
```

The Sense HAT returns a three-dimensional vector toward North. This class automaticaly projects that into a the 2D axis of the LED matrix.

This class can also be called from the macro:

```bash
sensehat compass
```

### Convert.py

The Sense HAT units of measurement are Celsius for temperature and millibars for pressure. If you are in the United States, those numbers can be confusing.

`C2F` can convert the temperature from Celsius to Fahrenheit.

```python
from RPiSense.Convert import C2F
print C2F (37)
```

`mbar2inHG` can convert the pressure to inches of mercury.

```python
from RPiSense.Convert import mbar2inHg
print mbar2inHg (940)
```

This class was written to support the `temperature` and `pressure` commands in the `sensehat` macro.

### Level.py

This class mimics the behavior of a bubble-leveler. A white dot on the LED matrix will drift "upwards".

Instantiate this class with a reference to the Sense HAT API and a sensitivity scale (with a higher number allowing you to see the finer adjustments to leveling).

```python
from sense_hat import SenseHat
from RPiSense.Level import Level
sense = SenseHat ()
l = Level (sense, scale=30)
l.Update ()
```

This class can also be called from the macro:

```bash
sensehat level
```

### MakeyJoy.py

Some coding projects require the use of a directional indicator. The Sense HAT has a joystick, but generically you can also use a keyboard or a Makey Makey. This class can determine the direction based on whether it was configured for the joystick or the keyboard.

Instantiate this class with a reference to the Sense HAT API and a boolean for whether to use a keyboard input instead of the joystick.

```python
from sense_hat import SenseHat
from RPiSense.MakeyJoy import MakeyJoy
sense = SenseHat ()
mj = MakeyJoy (sense, makey=False)
print mj.GetEvent ()
```

This class was written to support the `repeat` command in the `sensehat` macro.


### RepeatMe.py

The LED matrix opens up a lot of possibilities for designing visual games. A simple demonstration is a game of repetition. Colored squares light up on the LED matrix in one of four directions (up, down, left, right) in sequence and you have to memorize the sequence and then repeat it. This class uses the `MakeyJoy` class, so you have the option of entering the sequence in on a keyboard or with the joystick.

Instatiate this class with a reference to the Sense HAT API, a timer to control the speed, and a boolean for whether to use a keyboard input instead of the joystick.

```python
from sense_hat import SenseHat
from RPiSense.RepeatMe import RepeatMe
sense = SenseHat ()
rm = RepeatMe (sense, t=0.5, makey=False)
```

This class can also be called from the macro:

```bash
sensehat repeat
```
