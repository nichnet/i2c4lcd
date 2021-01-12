# i2c4lcd - Controller for HD44780 Compatible LCDs
i2c4lcd allows you to easily control HD44780 compatible LCDs via port expander modules with the PCF8574 IC.
This is primarily designed for Raspberry Pi. You will need to have installed python-smbus and i2c-tools.
<br/>
<br/>

## Getting Started

### Pi Setup
Using this for the Pi, you will need to enable automatic loading of I2C Kernal module. There are plenty of tutorials out there on how to do this.

Make the following connections from the Pi your port expander module:<br/>
- **GND   -- GND**<br/>
- **5V    -- VCC**<br/>
- **GPIO2 -- SDA**<br/>
- **GPIO3 -- SCL**
<br/>


Edit the Pi's /etc/modules file with:
```
sudo nano /etc/modules
```
and add the following lines, if they've not already been added (this will enable these modules at boot):
```
i2c-bcm2708
i2c-dev
```
<br/>

### Instsallation
As mentioned you will need to install smbus and i2c-tools:
```bash
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
```


Clone the repository:
```bash
git clone https://github.com/nichnet/i2c4lcd.git
```
<br/>
<br/>

## Usage

```
python i2c4lcd.py -m <message> -l <line number> -a <text align (l|c|r)> -c <clear current display> -f <flash backlight>
```
<br/>

### Simple Single String
```
python i2c4lcd.py -m "Hello World" -l 2 -a c
```
![](/images/print_single_clear.gif)


The display will be appended to without using the clear argument by default. This can be overwritten by setting the default in the user settings field:
```python
CLEAR_DISPLAY_DEFAULT = True
```

```
python i2c4lcd.py -m '"Hello World!" -l 3 -a c
```
![](/images/print_dontclear.gif)
<br/>

### Text Alignment

The text alignment can be set. If no argument is provided, the text will be left aligned by default.
You can set the alignment to "l" for left, "c" for center, and "r" for right alignment.

Below is an example calling the script with center alignment:
```
python i2c4lcd.py -m "Hello World" -l 2 -a c
```
![](/images/print_alignment.gif)
<br/>

### Multi-line Input

```
python i2c4lcd.py -m '["Hello World!", "How are you?"]' -c
```
![](/images/print_multiple.gif)
<br/>

### Display Flashing

When writing to the display, the display can be instructed to flash to prompt/notify the user. Flash speed and count can be overwritten in the user settings field:
```python
BACKLIGHT_FLASH_COUNT = 3
BACKLIGHT_FLASH_SPEED = 0.25 # 25ms
```

```
python i2c4lcd.py -m "Hello World!" -l 2 -a c -f
```
![](/images/print_flash.gif)

You can also override whether the backlight should be on or off by default in the user settings field. This is enabled by default:
```python
BACKLIGHT_DEFAULT_STATE = True
```
<br/>
<br/>

## Issues You May Face
You may run into a runtime error, this could be due to a memory address mismatch. Ensure your connection is proper and if the issue persists, run the following command to probe for devices.
```
sudo i2cdetect 0
```
or 
```
sudo i2cdetect 1
```
depending on your Pi version. 

Running this will immediately scan i2c bus 0 or 1 and return which memory address the device is located at. Update the user settings field as follows:
```python
I2C_ADDRESS = 0x27 # i2c device address (other typical address would be 0x3f)
```
<br/>
<br/>

## Extras
To interface with node.js, click [here](https://gist.github.com/nichnet/f7d64f01e9df4befce0b83a83fd92d18)
<br/>
<br/>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

<br/>
<br/>

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

