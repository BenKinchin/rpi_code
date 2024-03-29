import RPi.GPIO as GPIO
import smbus
import time
import sys

address = 0x48					#set initial variables
bus=smbus.SMBus(1)
cmd=0x40
ledPin = 11
dot = 0.4
letters_list = '?'.join("abcdefghijklmnopqrstuvwxyz").split("?") #lists of alphabet and morse
morse_list = ('01', '1000', '1010', '100', '0', '0010', '110', '0000', '00', '0111', '101', '0100', '11', '10', '111', '0110', '1101', '010', '000', '1', '001', '0001', '011', '1001', '1011', '1100')

def morse_to_letters(morse):
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
	GPIO.output(ledPin,GPIO.LOW)



def loop():
	"""Main progam loop"""
	#Initialises sensor value
	initial_vs = []
	for i in range(0,25):  #reads sensor value over two second and takes average
		value = analogRead(0)
		initial_vs.append(value)
		time.sleep(0.08)
	initial_v = sum(initial_vs) / 25
	print("READY...")
	GPIO.output(ledPin,GPIO.HIGH) #turns on LED when ready
	started = False    #variable checks whether message has started
	morse_message = '' #message decoded into morse
	final_message = '' #message decoded into regular letters
	u_t = 0.98	   #upper and lower bounds of the voltage, change these for different light settings
	l_t = 0.8

	while True:
		value = analogRead(0)	#Continuously reads Voltage from LDR


		if value > initial_v * u_t and started == True : #Checks if light has been turned off
			start =time.time()		#starts timer
			while True:
				value = analogRead(0)
				if time.time() - start > dot*15:   #prints message and end program if no data recieved
					print(morse_message)
					message_to_decode = morse_message.split(" ")
					for element in message_to_decode:
						final_message += morse_to_letters(element)
					print(final_message)
					turn_off()
				if value < initial_v * l_t :    #checks for voltage increase
					time_of_pause = time.time() - start
					#decides if pause is new letter, space, or accidental based on length
					#if pause is long then the message prints
					if time_of_pause > dot * 0.5:
						if time_of_pause > dot*1.5 and time_of_pause < dot*6:
							morse_message += ' '
						elif time_of_pause > dot*6 and time_of_pause < dot*12:
							morse_message += ' / '
						
						else:
							None
						break
				


		if value < initial_v * l_t :  #Checks for voltage dip (caused by LED shining)
			started = True			  #Message has started
			start =time.time()		  #Starts timer

			while True:
				value = analogRead(0)
				if value > initial_v * u_t :
					time_of_beep = time.time() - start	#times length of beep
					break

			#decides whether beep is dot or dash based on length
			if time_of_beep > dot*0.5 and time_of_beep < dot*1.5:
				morse_message += '0'
				print('0')
			elif time_of_beep > dot*1.5 and time_of_beep < dot*3.5:
				morse_message += '1'
				print('1')
			else:
				None

def turn_off():
	"""Closes bus and cleans GPIO data"""
	bus.close()
	GPIO.cleanup()
	sys.exit()
	
if __name__ == '__main__': #Program starts here
	print ('Program is starting ... ')
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		turn_off()
