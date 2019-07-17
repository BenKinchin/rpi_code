import RPi.GPIO as GPIO         #import required modules
import smbus
import time

address = 0x48					#set initial variables
bus=smbus.SMBus(1)
cmd=0x40
ledPin = 11
dot = 0.4
letters_list = '?'.join("abcdefghijklmnopqrstuvwxyz").split("?") #lists of alphabet and morse
morse_list = ('01', '1000', '1010', '100', '0', '0010', '110', '0000', '00', '0111', '101', '0100', '11', '10', '111', '0110', '1101', '010', '000', '1', '001', '0001', '011', '1001', '1011', '1100')
morse_message = '' #message decoded into morse
final_message = '' #message decoded into regular letters

time.sleep(0.5)
value = analogRead(0)
initial_v = value
time.sleep(1.5)
print("READY...")

def morse_to_letters(morse, morse_list=morse_list):
	"""takes morse code as input and outputs regular letters"""
	if morse== '/':
		return ' '
	for char in morse_list:
		if morse == char:
			return letters_list[morse_list.index(char)]
	return '?'


def analogRead(chn):
	"""Reads volage of LDR"""
	value = bus.read_byte_data(address,cmd+chn)
	return value

def setup():
	"""Sets up GPIO"""
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(ledPin,GPIO.OUT)
	GPIO.output(ledPin,GPIO.HIGH)

def light():
    """Checks whether light is on or off"""
    if value > initial_v * 0.95:
        return 'off'
    elif value < initial_v * 0.90:
        return 'on'
    else:
        return None

def pause_decoder(time_of_pause):
    """Takes time of pause as input and outputs space or new letter"""
    if time_of_pause > dot*1.5 and time_of_pause < dot*3.5:
        morse_message += ' '
    elif time_of_pause > dot*6 and time_of_pause < dot*9:
        morse_message += ' / '
    else:
        None
    flash_timer()

def pause_timer():
    """Times the length of pause and prints message if pause is > 10 dots long"""
    start_of_pause = time.time()    #starts timer
    while True:
        value = analogRead(0)       #Continuously reads voltage
        if time.time() - start_of_pause > dot*10:
            print(morse_message)
            message_to_decode = morse_message.split(" ")
            for element in message_to_decode:
                final_message += morse_to_letters(element)
            print(final_message)
            num = 1/0 #ends program

        if light() == 'on' :    #checks for voltage increase
            time_of_pause = time.time() - start
            if time_of_pause > 0.1:
                pause_decoder(time_of_pause)

def flash_timer():
    """Times length of flash and outputs dot or dash"""
    start_of_beep = time.time()		  #Starts timer
    while True:
        value = analogRead(0)         #Continuously checks voltage
        if light() == 'off' :
            time_of_beep = time.time() - start_of_beep	#calculates length of flash
            #decides whether flash was a dot or dash based on length
            if time_of_beep > dot*0.5 and time_of_beep < dot*1.5:
                morse_message += '0'
            elif time_of_beep > dot*1.5 and time_of_beep < dot*3.5:
                morse_message += '1'
            else:
                None
            pause_timer()

def loop():
	"""Main progam loop"""
	#Initialises sensor value

	while True:
		value = analogRead(0)	#Continuously reads Voltage from LDR
		if light() == 'on' :    #Checks for voltage dip (caused by LED shining)
			flash_timer()       #When LED turns on the flash timer function starts.


def turn_off():
	"""Closes bus and cleans GPIO data"""
	bus.close()
	GPIO.cleanup()

if __name__ == '__main__': #Program starts here
	print ('Program is starting ... ')
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		turn_off()
	except ZeroDivisionError:
		turn_off()
