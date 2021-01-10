# i2c4lcd

## About

i2c4lcd is a simple Python script to easily control HD44780 compatible LCDs via port expander modules with the PCF8574 IC.
This is primarily designed for Raspberry Pi, and you will need to have installed smbus which can be found [here](https://pypi.org/project/smbus2/).

## Usage

```
python i2c4lcd.py -m <message> -l <line number> -a <text align (l|c|r)> -c <clear current display> -f <flash backlight>
```

### Simple Single String
```
python i2c4lcd.py -m "Hello World" -l 2 -a c
```
![](/images/print_single_clear.gif)


The display will be appended to without using the clear argument by default. This can be overwritten by setting the default in the user settings field.
```python
CLEAR_DISPLAY_DEFAULT = True
```


```
python i2c4lcd.py -m '"Hello World!" -l 3 -a c
```
![](/images/print_dontclear.gif)


### Text Alignment

The text alignment can be set. If no argument is provided, the text will be left aligned by default.

```
python i2c4lcd.py -m "Hello World" -l 2 -a l
```
```
python i2c4lcd.py -m "Hello World" -l 2 -a c
```
```
python i2c4lcd.py -m "Hello World" -l 2 -a r
```
![](/images/print_alignment.gif)


### Multi-line Input

```
python i2c4lcd.py -m '["Hello World!", "How are you?"]' -c
```
![](/images/print_multiple.gif)


### Display Flashing

When writing to the display, the display can be instructed to flash to prompt/notify the user. Flash speed and count can be overwritten in the user settings field.

```python
BACKLIGHT_FLASH_COUNT = 3
BACKLIGHT_FLASH_SPEED = 0.25 # 25ms
```

```
python i2c4lcd.py -m "Hello World!" -l 2 -a c -f
```
![](/images/print_flash.gif)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

