from Phidget22.Phidget import *
from Phidget22.PhidgetException import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Stepper import *

from pynput import keyboard
from pynput.keyboard import Key, Listener
#import os
#import shutil
import traceback
import time

base_motor_flag = False
shoulder_motor_flag = False
elbow_motor_flag = False
wrist_motor_flag = False
claw_motor_flag = False

stop_flag = False

VHubSerial = 634722 #627531 #563134

grip_strength = 20   # % of max

smoothing = 0.001   # Controls how quickly motors change from moving to stopping

motors = []
motors_info = []
motor_flag_list = [base_motor_flag, shoulder_motor_flag, elbow_motor_flag, wrist_motor_flag, claw_motor_flag]


def on_press(key):
    
    try:
        # Base motor movement keys
        if key.char == 'q' and motor_flag_list[0] == True:
            if not base_motor.getIsMoving():
                base_motor.setVelocityLimit(30)
        elif key.char == 'w' and motor_flag_list[0] == True:
            if not base_motor.getIsMoving():
                base_motor.setVelocityLimit(-30)

        # Shoulder motor movement keys
        if key.char == 'r' and motor_flag_list[1] == True:
            if not shoulder_motor.getIsMoving():
                shoulder_motor.setVelocityLimit(50)
        elif key.char == 'e' and motor_flag_list[1] == True:
            if not shoulder_motor.getIsMoving():
                shoulder_motor.setVelocityLimit(-50)

        # Elbow motor movement keys
        if key.char == 'a' and motor_flag_list[2] == True:
            if not elbow_motor.getIsMoving():
                elbow_motor.setVelocityLimit(50)
        elif key.char == 's' and motor_flag_list[2] == True:
            if not elbow_motor.getIsMoving():
                elbow_motor.setVelocityLimit(-50)

        # Wrist motor movement keys
        if key.char == 'd' and motor_flag_list[3] == True:
            if not wrist_motor.getIsMoving():
                wrist_motor.setVelocityLimit(50)
        elif key.char == 'f' and motor_flag_list[3] == True:
            if not wrist_motor.getIsMoving():
                wrist_motor.setVelocityLimit(-50)

        # Claw motor movement keys
        if key.char == 'g' and motor_flag_list[4] == True:
            if not claw_motor.getIsMoving():
                
                claw_motor.setVelocityLimit(20)
        elif key.char == 'h' and motor_flag_list[4] == True:
            if not claw_motor.getIsMoving():
                claw_motor.setVelocityLimit(-20)

        # Pass on ESC press
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
            time.sleep(smoothing)
            base_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing)
            base_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing)
            base_motor.setVelocityLimit(0)

        # Shoulder motors off
        if (key.char == 'e' or key.char == 'r') and motor_flag_list[1] == True:
            lim = shoulder_motor.getVelocityLimit()
            shoulder_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing)
            shoulder_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing)
            shoulder_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing)
            shoulder_motor.setVelocityLimit(0)

        # Elbow motor off
        if (key.char == 'a' or key.char == 's') and motor_flag_list[2] == True:
            lim = elbow_motor.getVelocityLimit()
            elbow_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing)
            elbow_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing)
            elbow_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing)
            elbow_motor.setVelocityLimit(0)

        # Wrist motor off
        if (key.char == 'd' or key.char == 'f') and motor_flag_list[3] == True:
            lim = wrist_motor.getVelocityLimit()
            wrist_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing)
            wrist_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing)
            wrist_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing)
            wrist_motor.setVelocityLimit(0)

        # Claw motor off
        if (key.char == 'g' or key.char == 'h') and motor_flag_list[4] == True:
            lim = claw_motor.getVelocityLimit()
            claw_motor.setVelocityLimit(lim * 3 / 4)
            time.sleep(smoothing)
            claw_motor.setVelocityLimit(lim / 2)
            time.sleep(smoothing)
            claw_motor.setVelocityLimit(lim / 4)
            time.sleep(smoothing)
            claw_motor.setVelocityLimit(0)

        # End listener on ESC
        if key.char == 'p':
            print("Quitting programming...")

            for i in range(len(motors)):
                if(motors[i].getAttached() == True):
                    motors[i].setEngaged(False)
   
            stop_flag = True

    except AttributeError:
        print("Special key {0} released".format(key))
        

# Handlers
def onAttach(self):
    print("Motor {0} attached!".format(self.getHubPort()))
    motor_flag_list[self.getHubPort()] = True
    
def onDetach(self):
    print("Detach!")
    #print("Motor {0} detached!".format(motor_number))

def onError(self,code, description):
    print("Code: " + ErrorEventCode.getName(code))
    print("Description: " + str(description))
    print("----------")

# Device Initalization
def initialize_motors():
    global motors, motors_info

    for i in range(len(motors)):
        motors[i].setDeviceSerialNumber(VHubSerial)
        motors[i].setHubPort(i)
        # print("Hub Port Set \n")
        motors[i].setOnAttachHandler(onAttach)
        # print("Attach Handler Set\n")
        motors[i].setOnDetachHandler(onDetach)
        motors[i].setOnErrorHandler(onError)
        try: 
            motors[i].openWaitForAttachment(300)  # if having motor connection timout issues, increase this number
        except:
            print("Motor " + str(i) + " not attached")

        if (motors[i].getAttached() == True):
            motors[i].setControlMode(StepperControlMode.CONTROL_MODE_RUN)
            motors[i].setCurrentLimit(motors_info[i][0])
            motors[i].setHoldingCurrentLimit(motors_info[i][1])
            motors[i].setRescaleFactor(1.8/ 16/motors_info[i][2])
            motors[i].setAcceleration(50)
            motors[i].setVelocityLimit(0)
            motors[i].setEngaged(True)
            motors[i].setDataInterval(motors[i].getMinDataInterval())


# MAIN
def main():
    
    global motors, motors_info, base_motor, shoulder_motor, elbow_motor, wrist_motor, claw_motor, stop_flag
    # Declare and initialize motors and motor info (current limit, holding current, gear ratio)
    base_motor = Stepper()           # Rotates base
    base_motor_info = [2.8, 1, 77]
    shoulder_motor = Stepper()       # Rotates shoulder
    shoulder_motor_info = [2.8, 2.8, 15]
    elbow_motor = Stepper()          # Rotates elbow
    elbow_motor_info = [2.8, 1, 15]
    wrist_motor = Stepper()          # Rotates wrist
    wrist_motor_info = [0.67, 0.67, 100]
    claw_motor = Stepper()           # Pinches claw
    claw_motor_info = [0.67 * grip_strength / 100, 0, 100]
    
    # Note that the order of these matters in the .setHubPort initialization
    motors = [base_motor, shoulder_motor, elbow_motor, wrist_motor, claw_motor]
    motors_info = [base_motor_info, shoulder_motor_info, elbow_motor_info, wrist_motor_info, claw_motor_info]
    

    try:
        Log.enable(LogLevel.PHIDGET_LOG_INFO, "PhidgetArmLog.log")
        initialize_motors()

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        while(stop_flag == False):
            time.sleep(1)

        for i in range(len(motors)):
                if(motors[i].getAttached() == True):
                    motors[i].close()

    except PhidgetException as ex:
        #We will catch Phidget Exceptions here, and print the error informaiton.
        traceback.print_exc()
        print("")
        print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)

    print("DONE")



if __name__ == "__main__":
	main()
