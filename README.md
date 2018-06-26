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

## Additional Documentation

This README file is just to help you get the installation working. A more comprehensive documentation can be found at [].