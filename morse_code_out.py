import RPi.GPIO as GPIO
import time

ledPin = 11    # RPI Board pin11

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ledPin, GPIO.OUT)   # Set ledPin's mode is output
	GPIO.output(ledPin, GPIO.LOW)  # Set ledPin low to off led
	
letters_list = '?'.join("abcdefghijklmnopqrstuvwxyz").split("?") #creates a list of the alphabet and morse code
morse_list = ('01', '1000', '1010', '100', '0', '0010', '110', '0000', '00', '0111', '101', '0100', '11', '10', '111', '0110', '1101', '010', '000', '1', '001', '0001', '011', '1001', '1011', '1100')
dot = 0.4 #sets the length of time for one short flash

def message_time():
	morse_message = '' #string where morse code will be added
	message = input("Input your message...   ").lower()
	for letter in message:
		print("Letter {}.".format(letter))
		flashes = morse(letter) #runs the function to change letter to morse code
		morse_message += flashes + ' '
		for flash in flashes: #turns binary morse code into flashes on LED
			if flash == '0':
				GPIO.output(ledPin, GPIO.HIGH) 
				time.sleep(dot)
				GPIO.output(ledPin, GPIO.LOW)
				time.sleep(dot)
			elif flash == '1':
				GPIO.output(ledPin, GPIO.HIGH) 
				time.sleep(3*dot)
				GPIO.output(ledPin, GPIO.LOW)
				time.sleep(dot)
			else:
				time.sleep(7*dot)
		time.sleep(3*dot)
	print(morse_message)	
	turn_off() 
	
def morse(input_letter, letters_list=letters_list):
	"""takes a letter as input and outputs the morse code equivalent"""
	if input_letter == ' ':
		return '/'
	for char in letters_list:
		if input_letter == char:
			return morse_list[letters_list.index(char)]
	return ' '


def turn_off():
	"""turns off LED and cleans up GPIO resources"""
	GPIO.output(ledPin, GPIO.LOW)     # led off
	GPIO.cleanup()                    # Release resource



if __name__ == '__main__':     # Program starts from here
	setup()
	try:
		message_time()
	except KeyboardInterrupt:  
		turn_off()

