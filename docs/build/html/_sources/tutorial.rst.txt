*****************
RPiSense Tutorial
*****************

The main purpose of `RPiSense` is to set macros for the Sense HAT that can quickly demonstrate some of the features of the board. This section covers some of the commands that you can use.

Type the following into a Terminal window and observe the results:

.. code-block:: bash

  sensehat color --bg red
  sensehat scroll --message Hello World
  sensehat date --bg blue --fg white
   
You should see that the first command displays red pixels on the LED matrix, the second has scrolling text that says "Hello World", and the third shows the date in white lettering on a blue background. These commands will be covered below. The macro uses the `argparse` module, so you also have a help option:


.. code-block:: bash

  sensehat --help

This should give you an output that looks like:

.. code-block:: bash

  usage: sensehat [-h] [--fg FG [FG ...]] [--bg BG [BG ...]]
                  [--char CHAR [CHAR ...]] [--msg MSG [MSG ...]] [--time TIME]
                  [--number NUMBER] [--speed SPEED] [--dim] [--convert]
                  [--scale SCALE] [--makey] [--script SCRIPT [SCRIPT ...]]
                  {clear,color,letter,scroll,ip,date,time,datetime,temperature,
		   pressure,humidity,level,compass,repeat,exec}

  This macro allows for quick control over the Sense HAT during demonstrations
  or for the execution of scripts.

  positional arguments:
    {clear,color,letter,scroll,ip,date,time,datetime,temperature,pressure,
     humidity,level,compass,repeat,exec}
                          command to run

  optional arguments:
    -h, --help            show this help message and exit
    --fg FG [FG ...]      name of foreground color (can also be "random")
    --bg BG [BG ...]      name of background color (can also be "random")
    --char CHAR [CHAR ...]
                          character to display
    --msg MSG [MSG ...]   message to display
    --time TIME           duration (seconds) for display
    --number NUMBER       number of times to display
    --speed SPEED         speed of text scroll
    --dim                 force LED matrix dim
    --convert             convert to American units
    --scale SCALE         scale sensitivity
    --makey               use keyboard (e.g. Makey Makey) for input
    --script SCRIPT [SCRIPT ...]
                          specify a script to execute

Common Options
==============

There are a few options that will be pertinent to several of the command that will follow, so they are summarized here.

Colors
------

.. code-block:: bash

  [--fg <name1 name2 name3 ...>] [--bg <name4 name5 name6 ...>]

These control the colors sent to the LED matrix. The first is a foreground color, which is the color of your message. It is defaulted to "white". The second is a background color, which is the color that message will be displayed on. It is defaulted to "black".

Both options use the `Colors`_ module. The arguments are names of colors that have been defined in the `colors.csv` file. You can choose "random" or one of the names defined within this file. All other strings are considered invalid references.

.. _`Colors`: RPiSense.html#module-RPiSense.Colors

You can specify more than one `fg` color and more than one `bg` color. If the length of one list is longer than the other, then the shorter list will be extended by repeating its last entry. For example:

.. code-block:: bash

  --fg white --bg red green blue

These options will result in three different iterations: white on red, white on green, and white on blue.

.. code-block:: bash

  --fg red green blue --bg white black

These options will also result in three different iterations: red on white, green on black, and blue on black.

Brightness
----------

The LED matrix is quite bright by default. You can dim this with a simple option.

.. code-block:: bash

  [--dim]

This option is a boolean that is defaulted to False. It is a configuration of the Sense HAT board itself, so you can use this as an option for any of the commands below.

Loops
-----

Each of the colors in the list of `fg` and `bg` arguments will be shown at least once.

.. code-block:: bash

  [--number NUMBER]

This option allows you to repeat the color cycle. It is defaulted to 1. For example:

.. code-block:: bash

  sensehat color --fg red --number 3

This will display a messge with a foreground color of "red" three times.

.. code-block:: bash

  sensehat color --fg red green --number 3

This will display a message with a foreground color of "red", then with a foreground color of "green", then "red", then "green", then "red", then "green".

You can control the amount of pause between iterations.

.. code-block:: bash

  [--time TIME]

This option specifies the number of seconds (integer or float) to wait between iterations. It is defaulted to one second. For example:

.. code-block:: bash

  sensehat color --fg red green --number 3 --time 2

This will display "red" for 2 seconds, "green" for 2 seconds, "red" for 2 seconds", "green" for 2 seconds, "red" for 2 seconds, and finally "green" for 2 seconds.

It has been suggested that each color should have its own separate pause time and each loop number should have its own separate pause time. However, the pause time should be thought of as a clock that ticks according to the greatest common factor. For example, "green" will be displayed twice as long as the pauses between if you execute:

.. code-block:: bash

  sensehat color --fg green green --number 3 --time 1

You can also display "blank" screens by using the color black for both the foreground and the background.

Commands
========

A few commands have been written simply to make the functionality of the Sense HAT accessible from a command prompt.

clear
-----

Use this to quickly clear the LED matrix display. Often, you will be running a script that uses the LED matrix and you will encounter an unhandled exception or abort, especially during an indefinite loop. Rather than leaving the LED matrix in its last state, you might want to clear it. Use this command:

.. code-block:: bash

  sensehat clear

There are no options to specify for this command.

color
-----

You can display a color on all pixels in the LED matrix.

.. code-block:: bash

  sensehat color [--bg BG] [--number NUMBER>] [--time TIME]

At the end of all cycles, the display is cleared.

letter
------

You can display one letter at a time using the LED matrix.

.. code-block:: bash

  sensehat letter --char <CHAR1> [CHAR2 ...] [--fg FG] [--bg BG] [--number NUMBER] [--time TIME]

The `char` option is required but defaults to "X". More than one character can be specified but they should be separated by spaces.

At the end of all cycles, the display is cleared.

scroll
------

You can display a line of text that scrolls across the LED matrix.

.. code-block:: bash

  sensehat scroll --message <MSG1> [MSG2 ...] [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

The `message` option should be the text that you want to scroll. You can specify more than one message. However, if one of your messages contains a blank space (or other literals), it should be bookended by quotations.

The `speed` option controls how quickly the message will scroll. It is defaulted to 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

ip
----

You can have the IP address of the Raspberry Pi scroll on the LED matrix.

.. code-block:: bash

  sensehat ip [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

This is useful if you are going to SSH into the Raspberry Pi instead of connecting it to a monitor via HDMI.

The `speed` option controls how quickly the message will scroll. A typical value is 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

date
----

You can display the current date on the LED matrix.

.. code-block:: bash

  sensehat date [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

This is uses a generic feature of Python. However, it is useful to have this information displayed on the LED matrix for demonstrations.

The `speed` option controls how quickly the message will scroll. A typical value is 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

time
----

You can display the current time on the LED matrix.

.. code-block:: bash

  sensehat time [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

This is uses a generic feature of Python. However, it is useful to have this information displayed on the LED matrix for demonstrations.

The `speed` option controls how quickly the message will scroll. A typical value is 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

datetime
--------

You can display both the current date and time on the LED matrix.

.. code-block:: bash

  sensehat datetime [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

This is uses a generic feature of Python. However, it is useful to have this information displayed on the LED matrix for demonstrations.

The `speed` option controls how quickly the message will scroll. A typical value is 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

temperature
-----------

One of the sensors on the Sense HAT is a thermometer.

.. code-block:: bash

  sensehat temperature [--convert] [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

This temperature is measured on a Celsius scale by default. If you want to display the number in Fahrenheit, toggle the `convert` option.

The `speed` option controls how quickly the message will scroll. A typical value is 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

pressure
--------

One of the sensors on the Sense HAT is a barometer.

.. code-block:: bash

  sensehat pressure [--convert] [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

This pressure is measured on a millibar scale by default. If you want to display the number in inches of mercury, toggle the `convert` option.

The `speed` option controls how quickly the message will scroll. A typical value is 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

humidity
--------

One of the sensors on the Sense HAT is a hygrometer.

.. code-block:: bash

  sensehat humidity [--fg FG] [--bg BG] [--number NUMBER] [--time TIME] [--speed SPEED]

The `speed` option controls how quickly the message will scroll. A typical value is 0.05 and smaller numbers are faster.

At the end of all cycles, the display is cleared.

Scripts
=======

The previous commands showcased some of the basic capabilities of the Sense HAT by displaying quick information on the Sense HAT. More complicated scripts can be written that encode information and display it conditionally.

level
-----

One of the sensors on the Sense HAT is an accelerometer. This can be used to create an interactive leveler.

.. code-block:: bash 

  sensehat level [--fg FG] [--bg BG] [--scale SCALE]

This will display a dot that will drift "upwards" according to the orientation of the Sense HAT. If you are holding it perfectly level and then tilt it to the right, the "bubble" will "float" to the right. If you tilt it forward, it will "float" to the back.

The sensitivity to the angle of orientation is controlled by the `scale` option. It is defaulted to 30 and higher numbers are more sensitive to tilting.

This script is on an indefinite loop, so you will have to interrupt the script to stop it. You should run the `clear` command afterwards if you plan to continue to use the Sense HAT for other purposes.
  
compass
-------

One of the senseors on the Sense HAT is a magnetometer.

.. code-block:: bash

  sensehat compass [--fg FG] [--bg BG]

This will display a dot that will slide along the edge of a circle until it is on the northernmost point.

This script is on an indefinite loop, so you will have to interrupt the script to stop it. You should run the `clear` command afterwards if you plan to continue to use the Sense HAT for other purposes.
  
repeat
------

The Sense HAT has a manual joystick. A script has been written for a memory game.

.. code-block:: bash

  sensehat repeat [--makey]

This will display a sequence of squares that are either "up", "down", "left", or "right". Your goal is to memorize the sequence and repeat it back with the joystick. If you get it right, another entry will be added to the list. If you get it wrong, you have to start over.

This script was also written to be compatible with a Makey Makey microcontroller. In this case, enable the `makey` option and use the arrow keys instead of joystick inputs. The interface will be identical to a standard keyboard, so you can also use this option for keyboard interpretation.

This script is on an indefinite loop, but it will gracefully exit when you get the sequence wrong.
  
exec
----

This macro is also capable of executing scripts directly.

.. code-block:: bash

  sensehat exec --script <SCRIPT1> [SCRIPT2 ...]

The `script` option specifies which script to execute. You can have more than one script. This is just a convenience that allows you to write your own script using the same overhead of globals defined in this macro. The display is not cleared between scripts, so you have the option of stacking pixels on the display.
