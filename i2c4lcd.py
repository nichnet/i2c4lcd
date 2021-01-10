import smbus
import time
import sys
import ast
import getopt


#  ---------- User Settings ----------

I2C_ADDRESS = 0x27 # i2c device address (in change of error, update to 0x3f address)

#Open i2c interface
#bus = smbus.SMBus(0) # Raspberry Pi Revision 1 = 0
bus = smbus.SMBus(1)  # Raspberry Pi Revision 2 = 1

# Display Settings
DISPLAY_WIDTH = 20 # Maximum characters per line
CLEAR_DISLPAY_DEFAULT  = False # Should display be cleared before writing.

# LCD RAM Addresses for the first 4 lines - add more or commment out,
# depending on your display, as the program determines the line count from this dictionary.
LINE_MEMORY_ADDRESSES = {
    '1': 0x80,
    '2': 0xC0,
    '3': 0x94,
    '4': 0xD4
   #'5': 0x00
}

# Backlight Settings
BACKLIGHT_DEFAULT_STATE = True # True = on | False = off
BACKLIGHT_FLASH_COUNT = 3    # Amount of flashes when flashing is enabled.
BACKLIGHT_FLASH_SPEED = 0.25 # 25ms delay between flash.

# ---------- End of settings ----------


# Mode constants
MODE_CHR = 1 # Send data mode
MODE_CMD = 0 # Send command mode

# Backlight constants
BACKLIGHT_ON  = 0x08
BACKLIGHT_OFF = 0x00

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

ENABLE = 0b00000100 # Enable bit


def show_single_message(message, line, align):
        #format the message
        message = format_message(message, align)
        #get line number mem address
        line_address = get_line_address(line)
        #show message on the display
        show_message(message, line_address)


def show_multiple_message(message, align):
    #get the lesser of the max lines or lines supplied in the array
    #the lesser of the two will be how many times to iterate.
    lines = 1
    if get_max_lines() < len(message):
        lines = get_max_lines()
    else:
        lines = len(message)

    for x in range(0, lines):
        #format the message
        formatted_msg = format_message(message[x], align)

        #get line number mem address
        line_address = get_line_address(x + 1) # offset the index to keep consistent with the line memory key map.

        #show message on the display
        show_message(formatted_msg, line_address)


def show_message(message, line):
  lcd_byte(line, MODE_CMD)

  for i in range(DISPLAY_WIDTH):
    lcd_byte(ord(message[i]), MODE_CHR)


def format_message(message, align):
    if align == 'c': #center
        return message.center(DISPLAY_WIDTH, " ")
    elif align == 'r': #right
        return message.rjust(DISPLAY_WIDTH, " ")

    #if L justified or something else, just default to L justified.
    return message.ljust(DISPLAY_WIDTH, " ")


def clear_display():
    lcd_byte(0x01, MODE_CMD)


def get_max_lines():
    return len(LINE_MEMORY_ADDRESSES)


def flash_display():
    for x in range(BACKLIGHT_FLASH_COUNT * 2):
        state = True

        state = ((x % 2) == 0) if BACKLIGHT_DEFAULT_STATE else ((x % 2) != 0)
        set_backlight(state)
        time.sleep(BACKLIGHT_FLASH_SPEED)

    #finally set final state
    set_backlight(BACKLIGHT_DEFAULT_STATE)


def set_backlight(state):
    bus.write_byte(I2C_ADDRESS, get_backlight_bit(state))


def get_backlight_bit(state):
    return BACKLIGHT_ON if state == True else BACKLIGHT_OFF


def get_line_address(line):
    #clamp the line number provided to > 0 < max lines
    line = max(1, min(line, get_max_lines()))

    #now get the line address from the dictionary.
    return LINE_MEMORY_ADDRESSES[str(line)]


def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | get_backlight_bit(BACKLIGHT_DEFAULT_STATE)
    bits_low = mode | ((bits<<4) & 0xF0) | get_backlight_bit(BACKLIGHT_DEFAULT_STATE)

    # high
    bus.write_byte(I2C_ADDRESS, bits_high)
    lcd_toggle_enable(bits_high)

    # low
    bus.write_byte(I2C_ADDRESS, bits_low)
    lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
    # Toggle enable
    sleep(E_DELAY)
    bus.write_byte(I2C_ADDRESS, (bits | ENABLE))
    sleep(E_PULSE)
    bus.write_byte(I2C_ADDRESS,(bits & ~ENABLE))
    sleep(E_DELAY)

def init_display():
    # Initialise display
    lcd_byte(0x33, MODE_CMD) # 110011 Initialise
    lcd_byte(0x32, MODE_CMD) # 110010 Initialise
    lcd_byte(0x06, MODE_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C, MODE_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, MODE_CMD) # 101000 Data length, number of lines, font size
    clear_display()
    sleep(E_DELAY)


def show_help_and_exit():
    print 'i2c4lcd.py -m <message> -l <line number> -a <text align (l|c|r)> -c <clear current display> -f <flash backlight>'
    exit(2)


def main(argv):
    message = ['']
    line = 1
    align = 'l'
    clear = CLEAR_DISLPAY_DEFAULT
    flash = False

    try:
        opts, args = getopt.getopt(argv, "hcfm:l:a:", ["message=", "line=", "align="])
    except getopt.GetoptError:
        show_help_and_exit()

    for opt, arg in opts:
        if opt == '-h':
            show_help_and_exit()
        elif opt == '-c':
             clear = True
        elif opt == '-f':
             flash = True
        elif opt in ("-m", "--message"):
            if len(arg) > 0:
                raw_msg = arg

                #determine if open and closes with []
                if raw_msg[0] == '[' and raw_msg[len(raw_msg) - 1] == ']':
                    message = ast.literal_eval(arg)
                else:
                    #single message
                    message = [arg]
        elif opt in ("-l", "--line"):
            line = int(arg)
        elif opt in ("-a", "--align"):
            align = arg

    #set text alignment default
    if align not in ("l", "c", "r"):
        align = 'l'

    #clear the display if necessary
    if clear == True:
        clear_display()

    #fill empty if list is empty
    if len(message) == 0:
        message = ['']

    #show message
    if len(message) > 1:
        show_single_message(message, align)
    else:
        show_multiple_message(message[0], line, align)

    #flash the display if necessary
    if flash == True:
        flash_display()


if __name__ == '__main__':
    init_display()
    main(sys.argv[1:])
