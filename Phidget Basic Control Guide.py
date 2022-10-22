# Basic python Phidget Program to Test

from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import * #import stepper motor

import time
import traceback

# Phidget Workflow:
	# 1. Create Channel - variable to track phidget
	# 2. Address Channel - give the variable your phidget's addressing info
	# 3. Open Channel - will attempt to connect a phidget to the channel you created
	# 4. Detect Channel Attachement - wait for API to find the phidget you specified (can include exception handling)
	# 5. Operate on Channel - Use the API of your phidget device to control it
	# 6. Close Channel - One program is done, close the channel to free up the physical phidget device


# From here I want to create a basic control template for the motor driver phidget and also the vint hub

def attachHandler(self):
	print("Successfully attached motor!")


# This function will move the motor four times at four different velocities before stopping it
def motorMovement(motor):
	motor.setVelocityLimit(50)
	time.sleep(1)
	motor.setVelocityLimit(100)
	time.sleep(1)
	motor.setVelocityLimit(25)
	time.sleep(1)
	motor.setVelocityLimit(200)
	time.sleep(2)
	motor.setVelocityLimit(0)

def main():
	# vint hub addressing info
	vintSerialNum = 620000
	
	# Rescale factor
	controllerStepCount = 1/16
	motorStepAngle = 1.8
	gearRatio = 15
	rescaleFactor = motorStepAngle * controllerStepCount / gearRatio	#setting the resecale factor makes it so acceleration, velocity, and position
																		#units are all shared; We have it set so everything is in degrees,degrees/s,degrees/s^2
	
	currentLimit = 2.8
	holdingCurrentLimit = 0.3

	# initial values
	acceleration = 400  	# degrees/second^2 
	velocity = 0   			# degrees/second 

	try:
		# 1. Create Channel
		stepper0 = Stepper() #Creating a stepper object variable
		

		# 2. Detect Channel Attachement
		# AKA add handlers
			# Once a channel is attached, it launches an event that we can capture
			# Note that the attachement handler must have been called before attempting to attach the motor
			# code for attachment handler is under step 1
		
		stepper0.setOnAttachHandler(attachHandler)

		# 3. Address Channel
			# All addressing info can be found in the Control Panel
			# Can set the serial number of the device by simply doing this:
				# stepper0.setDeviceSerialNumber(69420)
			# If connected to a vint hub then the device inherints the serial number of the vint hub
			# The device then needs to be specified by selecting the appropriate vint hub channel
			# The vint serial number still needs to be specified
			# Can use the WriteLabel command to replace the serial number with a custom label name - stored in flash
			# With a vint Hub, the heirarchy of connections is as follows:
				# Set phdiget device serial number to match that of the vint hub
				# Set hub port that your phidget device attaches to on the vint hub
				# Set the channel number of your phidget (only needed if there are more than one channels)
		stepper0.setDeviceSerialNumber(vintSerialNum)   
		stepper0.setHubPort(0)

		# 4. Open Channel
			# This process starts the opening/attachement process by looking for phidgets based on the above addressing
			# openWaitForAttachement(time_ms) will halt the program for time_ms or until it finds a phidget
			# open() will start the searching process in the background and allow a phidget to connect at any point
			# in the program's life
		stepper0.openWaitForAttachment(5000)


		# 5. Operate on Channel - Use the API of your phidget device to control it
			# Write code to move the motors here

		# setup code 
		stepper0.setControlMode(StepperControlMode.CONTROL_MODE_RUN) # moves continuously at velocity limit when engaged 
		stepper0.setCurrentLimit(currentLimit)
		stepper0.setHoldingCurrentLimit(holdingCurrentLimit)
		stepper0.setRescaleFactor(rescaleFactor)
		stepper0.setAcceleration(acceleration)  
		stepper0.setVelocityLimit(velocity)

		stepper0.setEngaged(True)       # enables motor current
		stepper0.setDataInterval(stepper0.getMinDataInterval())  # how quickly the controller can update the motors velocity/accelartion values

		# movement code
		motorMovement(stepper0)

		stepper0.setEngaged(False)

		# 6. Close Channel
		stepper0.close()

	except PhidgetException as ex:
		#We will catch Phidget Exceptions here, and print the error informaiton.
		traceback.print_exc()
		print("")
		print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)


if __name__ == "__main__":
	main()
