from Phidget22.Phidget import *
from Phidget22.PhidgetException import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.Encoder import *

from pynput import keyboard
from pynput.keyboard import Key, Listener

#import shutil
#import os
import traceback
import time

#Getting today's date, used for logging purposes
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

base_motor_flag = False
shoulder_motor_flag = False
elbow_motor_flag = False
wrist_motor_flag = False
claw_motor_flag = False

stop_flag = False

VHubSerial_motors = 634722 #627531 #563134
VHubSerial_encoders = 561059

smoothing = 0.005   # Time delay (in seconds) for a motor to change from moving to stopped

motors = []
motors_info = []
motor_flag_list = [base_motor_flag, shoulder_motor_flag, elbow_motor_flag, wrist_motor_flag, claw_motor_flag]
encoders = []

def homepose():
    shoulder_test = 1
    while shoulder_test == 1:
        if shoulder_position >= 131 and shoulder_position <= 132:
            print("correct")
            lim = shoulder_motor.getVelocityLimit()
            shoulder_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing / 4)
            shoulder_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing / 4)
            shoulder_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing / 4)
            shoulder_motor.setVelocityLimit(0)
            shoulder_test = 0
        elif shoulder_position <= 132:
            print(f"less {shoulder_position}")
            shoulder_motor.setVelocityLimit(4)
        elif shoulder_position >= 131:
            print(f"more {shoulder_position}")
            shoulder_motor.setVelocityLimit(-4)

    elbow_test = 1
    while elbow_test == 1:
        if elbow_position >= 179 and elbow_position <= 181:
            print("correct")
            lim = elbow_motor.getVelocityLimit()
            elbow_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing / 4)
            elbow_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing / 4)
            elbow_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing / 4) 
            elbow_motor.setVelocityLimit(0)
            elbow_test = 0
        elif elbow_position <= 181:
            print(f"less {elbow_position}")
            elbow_motor.setVelocityLimit(5)
        elif elbow_position >= 179:
            print(f"more {elbow_position}")
            elbow_motor.setVelocityLimit(-5)
    
# Set motors into motion, function motor.setVelocityLimit() sets speed in degrees / second
def on_press(key):

    try:
        #Set Arm to home position
        #Shoulder Position: 131.7408, Elbow Position: 179.952
        if key.char == 'z':
            print("key for z works")
            homepose()

        # Base motor movement keys
        if key.char == 'q' and motor_flag_list[0] == True:
            if not base_motor.getIsMoving():
                base_motor.setVelocityLimit(10)
        elif key.char == 'w' and motor_flag_list[0] == True:
            if not base_motor.getIsMoving():
                base_motor.setVelocityLimit(-10)

        # Shoulder motor movement keys
        if key.char == 'r' and motor_flag_list[1] == True:
            if not shoulder_motor.getIsMoving():
                shoulder_motor.setVelocityLimit(5)
        elif key.char == 'e' and motor_flag_list[1] == True:
            if not shoulder_motor.getIsMoving():
                shoulder_motor.setVelocityLimit(-5)

        # Elbow motor movement keys
        if key.char == 'a' and motor_flag_list[2] == True:
            if not elbow_motor.getIsMoving():
                elbow_motor.setVelocityLimit(10)
        elif key.char == 's' and motor_flag_list[2] == True:
            if not elbow_motor.getIsMoving():
                elbow_motor.setVelocityLimit(-10)

        # Wrist motor movement keys
        if key.char == 'd' and motor_flag_list[3] == True:
            if not wrist_motor.getIsMoving():
                wrist_motor.setVelocityLimit(10)
        elif key.char == 'f' and motor_flag_list[3] == True:
            if not wrist_motor.getIsMoving():
                wrist_motor.setVelocityLimit(-10)

        # Claw motor movement keys
        if key.char == 'g' and motor_flag_list[4] == True:
            if not claw_motor.getIsMoving():
                claw_motor.setVelocityLimit(10)
        elif key.char == 'h' and motor_flag_list[4] == True:
            if not claw_motor.getIsMoving():
                claw_motor.setVelocityLimit(-10)

        # Pass on 'p' press
        if key.char == 'p':
            pass

    except AttributeError:
        print("Special key {0} pressed".format(key))


def on_release(key):
    global base_motor, shoulder_motor, elbow_motor, wrist_motor, claw_motor, stop_flag
    try:
        # Base motor off
        if (key.char == 'q' or key.char == 'w') and motor_flag_list[0] == True:
            lim = base_motor.getVelocityLimit()
            base_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing / 4)
            base_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing / 4)
            base_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing / 4)
            base_motor.setVelocityLimit(0)

        # Shoulder motors off
        if (key.char == 'e' or key.char == 'r') and motor_flag_list[1] == True:
            lim = shoulder_motor.getVelocityLimit()
            shoulder_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing / 4)
            shoulder_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing / 4)
            shoulder_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing / 4)
            shoulder_motor.setVelocityLimit(0)

        # Elbow motor off
        if (key.char == 'a' or key.char == 's') and motor_flag_list[2] == True:
            lim = elbow_motor.getVelocityLimit()
            elbow_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing / 4)
            elbow_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing / 4)
            elbow_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing / 4)
            elbow_motor.setVelocityLimit(0)

        # Wrist motor off
        if (key.char == 'd' or key.char == 'f') and motor_flag_list[3] == True:
            lim = wrist_motor.getVelocityLimit()
            wrist_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing / 4)
            wrist_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing / 4)
            wrist_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing / 4)
            wrist_motor.setVelocityLimit(0)

        # Claw motor off
        if (key.char == 'g' or key.char == 'h') and motor_flag_list[4] == True:
            lim = claw_motor.getVelocityLimit()
            claw_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing / 4)
            claw_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing / 4)
            claw_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing / 4)
            claw_motor.setVelocityLimit(0)

        # End program when 'p' is pressed
        if key.char == 'p':

            print("p is pressed")

            # Elbow motor shutdown
            while (elbow_position >= 182 or elbow_position <= 178) and motor_flag_list[2] == True:
                if elbow_position >= 182:
                    if (elbow_position -180) >= 20:
                        elbow_motor.setVelocityLimit(-10 * 3 / 4)
                    elif (elbow_position -180) >= 10 and (elbow_position -180) <= 20:
                        elbow_motor.setVelocityLimit(-10 / 2)
                    elif (elbow_position -180) >= 2 and (elbow_position -180) <= 10:
                        elbow_motor.setVelocityLimit(-10 / 4)
                if elbow_position <= 178:
                    if (elbow_position -180) <= -20:
                        elbow_motor.setVelocityLimit(10 * 3 / 4)
                    elif (elbow_position -180) <= -10 and (elbow_position -180) >= -20:
                        elbow_motor.setVelocityLimit(10 / 2)
                    elif (elbow_position -180) <= -2 and (elbow_position -180) >= -10:
                        elbow_motor.setVelocityLimit(10 / 4)
            elbow_motor.setVelocityLimit(0)
            print("elbow has been shutdown")

            # Shoulder motor shutdown
            while (shoulder_position >= 130 or shoulder_position <= 129) and motor_flag_list[1] == True:
                if shoulder_position >= 130:
                    if (shoulder_position -130) >= 20:
                        shoulder_motor.setVelocityLimit(-5 * 3 / 4)
                    elif (shoulder_position -130) >= 10 and (shoulder_position -130) <= 20:
                        shoulder_motor.setVelocityLimit(-5 / 2)
                    elif (shoulder_position -130) >= 0 and (shoulder_position -130) <= 10:
                        shoulder_motor.setVelocityLimit(-5 / 4)
                if shoulder_position <= 129:
                    if (shoulder_position -130) <= -20:
                        shoulder_motor.setVelocityLimit(5 * 3 / 4)
                    elif (shoulder_position -130) <= -10 and (shoulder_position -130) >= -20:
                        shoulder_motor.setVelocityLimit(5 / 2)
                    elif (shoulder_position -130) <= -1 and (shoulder_position -130) >= -10:
                        shoulder_motor.setVelocityLimit(5 / 4)
            shoulder_motor.setVelocityLimit(0)
            print("Shoulder has been shutdown")

            print(f"\nQuitting program...")

            for i in range(len(motors)):
                if(motors[i].getAttached() == True):
                    motors[i].setEngaged(False)
                    motors[i].close()
   
            stop_flag = True

    except AttributeError:
        print("Special key {0} released".format(key))
        

# Handlers
def onAttach_motor(self):
    print("Motor {0} attached!".format(self.getHubPort()))
    motor_flag_list[self.getHubPort()] = True

def onAttach_encoder(self):
    print("Encoder {0} attached!".format(self.getHubPort()))
    
def onDetach(self):
    print("Detach!")
    #print("Motor {0} detached!".format(motor_number))

def onError(self,code, description):
    print("Code: " + ErrorEventCode.getName(code))
    print("Description: " + str(description))
    print("----------")


#Encoder initialization
def initialize_encoders():
    for i in range(len(encoders)):
        encoders[i].setDeviceSerialNumber(VHubSerial_encoders)
        encoders[i].setHubPort(i)
        encoders[i].setOnAttachHandler(onAttach_encoder)
        encoders[i].setOnDetachHandler(onDetach)
        encoders[i].setOnErrorHandler(onError)
        
        try:
            encoders[i].openWaitForAttachment(300)
        except:
            print("Encoder " + str(i) + " not attached")
        
        if(encoders[i].getAttached() == True):

            encoders[i].setEnabled(True)
            
            #initialize position for each encoder (need to add scaling factor for any non-zero values)
            if (i == 0):
                base_encoder.setPosition(0)
            if (i == 1):
                shoulder_encoder.setPosition(0)
            if (i == 2):
                elbow_encoder.setPosition(0)
            if(i == 3):
                wrist_encoder.setPosition(0)
            if(i == 4):
                claw_encoder.setPosition(0)


# Motor Initalization
def initialize_motors():
    global motors, motors_info

    for i in range(len(motors)):
        motors[i].setDeviceSerialNumber(VHubSerial_motors)
        motors[i].setHubPort(i)
        # print("Hub Port Set \n")
        motors[i].setOnAttachHandler(onAttach_motor)
        # print("Attach Handler Set\n")
        motors[i].setOnDetachHandler(onDetach)
        motors[i].setOnErrorHandler(onError)
        try: 
            motors[i].openWaitForAttachment(300)  # If having motor connection timout issues, increase this number
        except:
            print("Motor " + str(i) + " not attached")

        if (motors[i].getAttached() == True):
            motors[i].setControlMode(StepperControlMode.CONTROL_MODE_RUN)
            motors[i].setCurrentLimit(motors_info[i][0])
            motors[i].setHoldingCurrentLimit(motors_info[i][1])
            motors[i].setRescaleFactor((1/16) * 1.8 * (1/motors_info[i][2]) * (1/motors_info[i][3])) # (1/16) * Step angle * (1/Gearbox ratio) * (1/Gear ratio)
            motors[i].setAcceleration(50)
            motors[i].setVelocityLimit(0)
            motors[i].setEngaged(True)
            motors[i].setDataInterval(motors[i].getMinDataInterval())


# MAIN
def main():
    # All motors, encoders, and positions are declared as global variables
    global motors, motors_info, base_motor, shoulder_motor, elbow_motor, wrist_motor, claw_motor, stop_flag, encoders, base_encoder, shoulder_encoder, elbow_encoder, wrist_encoder, claw_encoder
    global base_position, base_initial_pos, elbow_position, elbow_initial_pos, shoulder_position, shoulder_initial_pos, wrist_position, wrist_initial_pos, claw_position, claw_initial_pos

    # Declare and initialize motors and motor info (current limit, holding current, gear box ratio, gear ratio)
    # Also declare initial motor positions (based on assumed starting position)
    base_motor = Stepper()
    base_motor_info = [2.8, 1, 77, 1]
    base_encoder = Encoder()
    base_initial_pos = 0

    shoulder_motor = Stepper()
    shoulder_motor_info = [2.8, 2.8, 15, 50/16]
    shoulder_encoder = Encoder()
    shoulder_initial_pos = 130

    elbow_motor = Stepper()
    elbow_motor_info = [2.8, 1, 15, 50/24]
    elbow_encoder = Encoder()
    elbow_initial_pos = 180

    wrist_motor = Stepper()
    wrist_motor_info = [0.67, 0.67, 100, 1]
    wrist_encoder = Encoder()
    wrist_initial_pos = 0

    claw_motor = Stepper()
    claw_motor_info = [0.67, 0.67, 100, 1]
    claw_encoder = Encoder()
    claw_initial_pos = 0
    
    # Note that the order of these motors/encoders matters in the .setHubPort initialization
    motors = [base_motor, shoulder_motor, elbow_motor, wrist_motor, claw_motor]
    motors_info = [base_motor_info, shoulder_motor_info, elbow_motor_info, wrist_motor_info, claw_motor_info]
    encoders = [base_encoder, shoulder_encoder, elbow_encoder, wrist_encoder, claw_encoder]

    try:
        # Data log saved into current working directory
        Log.enable(LogLevel.PHIDGET_LOG_INFO, "PhidgetArmLog.log")
        
        # Functions to initialize components
        print(f"\nInitializing...\n")
        initialize_encoders()
        print()
        initialize_motors()
        print(f"\nSuccessfully initialized!\n")

        # Listener to allow for keyboard input from user
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        #Logging

        file = open("PhidgetPositionLog.txt", "a")
        file.write( "-----------------------------------------------------------------------------\n")
        file.write(f"-                  Time of Log in: {dt_string}                      -\n")
        file.write( "-----------------------------------------------------------------------------\n")
        file.close()

        # Main loop of code, stop_flag becomes True when 'p' is pressed
        while(stop_flag == False):
            # Get current motor position from quadrature encoders using this formula:
            # encoder_count (reading from encoder) * cycle/count (encoder interface resolution) * rev/cycle (CPR of encoder) * degrees/rev * 1/gear_box_ratio * external_gear_ratio (for shoulder/elbow) 
            if(base_encoder.getAttached()):
                base_position = base_encoder.getPosition() * (1/4) * (1/300) * (360/1) * (1/77) + base_initial_pos
            if(shoulder_encoder.getAttached()):
                shoulder_position = shoulder_encoder.getPosition() * (1/4) * (1/300) * (360/1) * (1/15) * (16/50) + shoulder_initial_pos
            if(elbow_encoder.getAttached()):
                elbow_position = elbow_encoder.getPosition() * (1/4) * (1/300) * (360/1) * (1/15) * (24/50) + elbow_initial_pos
            if(wrist_encoder.getAttached()):
                wrist_position = wrist_encoder.getPosition() * (1/4) * (1/300) * (360/1) * (1/100) + wrist_initial_pos
            if(claw_encoder.getAttached()):
                claw_position = claw_encoder.getPosition() * (1/4) * (1/300) * (360/1) * (1/100) + claw_initial_pos

            # Print motor position information
            print("      Shoulder Position: " + str(shoulder_position) + "       Elbow Position: " + str(elbow_position))
            
            #Adding phidget motor postion information in PhidgetPositionLog.txt
            file = open("PhidgetPositionLog.txt", "a")
            file.write(f"\tShoulder Position: {shoulder_position}\t\tElbow Position: {elbow_position}\n")
            file.close()

            # Test to prove that motor.getPosition() gives accurate position readings (in degrees) when compared to encoder readings
            #print("      Motor Shoulder Position: " + str(shoulder_motor.getPosition() + 130) + "      Motor Elbow Position: " + str(elbow_motor.getPosition() + 180))

            #Time delay between each loop
            time.sleep(0.5)

    # Catch Phidget Exceptions here, and print the error information.
    except PhidgetException as ex:
        traceback.print_exc()
        print()
        print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)

    print(f"Successfully quit program.\n\nGoodbye!\n")



if __name__ == "__main__":
	main()
