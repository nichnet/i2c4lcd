# i2c4lcd

## Usage


```
python i2c4lcd.py -m "Hello World" -l 2 -a c
```
![](/images/print_single_clear.gif)

```
python i2c4lcd.py -m '"Hello World!" -l 3 -a c
```
![](/images/print_dontclear.gif)


### Text Alignment

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

```
python i2c4lcd.py -m "Hello World!" -l 2 -a c -f
```
![](/images/print_flash.gif)


