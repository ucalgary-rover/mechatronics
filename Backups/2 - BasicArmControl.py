from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Stepper import *

from pynput import keyboard
from pynput.keyboard import Key, Listener
#import os
#import shutil
import traceback
import time


def on_press(key):
    global base_motor, shoulder_motor1, shoulder_motor2, elbow_motor, wrist_motor, claw_motor
    try:
        # Base motor movement keys
        if key.char == 'q':
            if not base_motor.getIsMoving():
                base_motor.setVelocityLimit(30)
        elif key.char == 'w':
            if not base_motor.getIsMoving():
                base_motor.setVelocityLimit(-30)

        # Shoulder motor movement keys
        if key.char == 'e':
            if not shoulder_motor1.getIsMoving():
                shoulder_motor1.setVelocityLimit(50)
                shoulder_motor2.setVelocityLimit(-50)
        elif key.char == 'r':
            if not shoulder_motor1.getIsMoving():
                shoulder_motor1.setVelocityLimit(-50)
                shoulder_motor2.setVelocityLimit(50)

        # Elbow motor movement keys
        if key.char == 'a':
            if not elbow_motor.getIsMoving():
                elbow_motor.setVelocityLimit(50)
        elif key.char == 's':
            if not elbow_motor.getIsMoving():
                elbow_motor.setVelocityLimit(-50)

        # Wrist motor movement keys
        if key.char == 'd':
            if not wrist_motor.getIsMoving():
                wrist_motor.setVelocityLimit(50)
        elif key.char == 'f':
            if not wrist_motor.getIsMoving():
                wrist_motor.setVelocityLimit(-50)

        # Claw motor movement keys
        if key.char == 'g':
            if not claw_motor.getIsMoving():
                claw_motor.setVelocityLimit(20)
        elif key.char == 'h':
            if not claw_motor.getIsMoving():
                claw_motor.setVelocityLimit(-20)

        # Pass on ESC press
        if key.char == 'p':
            pass

    except AttributeError:
        print("Special key {0} pressed".format(key))


def on_release(key):
    global base_motor, shoulder_motor1, shoulder_motor2, elbow_motor, wrist_motor, claw_motor
    try:
        # Base motor off
        if (key.char == 'q' or key.char == 'w'):
            base_motor.setVelocityLimit(0)

        # Shoulder motors off
        if (key.char == 'e' or key.char == 'r'):
            shoulder_motor1.setVelocityLimit(0)
            shoulder_motor2.setVelocityLimit(0)

        # Elbow motor off
        if (key.char == 'a' or key.char == 's'):
            elbow_motor.setVelocityLimit(0)

        # Wrist motor off
        if (key.char == 'd' or key.char == 'f'):
            wrist_motor.setVelocityLimit(0)

        # Claw motor off
        if (key.char == 'g' or key.char == 'h'):
            claw_motor.setVelocityLimit(0)

        # End listener on ESC
        if key.char == 'p':
            print("Quitting programming...")
            base_motor.setEngaged(False)
            shoulder_motor1.setEngaged(False)
            shoulder_motor2.setEngaged(False)
            elbow_motor.setEngaged(False)
            wrist_motor.setEngaged(False)
            claw_motor.setEngaged(False)
            return False

    except AttributeError:
        print("Special key {0} released".format(key))
        
def onAttach(motor_number):
    print("Motor {0} attached!".format(motor_number))

def onDetach(self):
    print("Detach!")
    #print("Motor {0} detached!".format(motor_number))

def onError(self,code, description):
    print("Code: " + ErrorEventCode.getName(code))
    print("Description: " + str(description))
    print("----------")

def initialize_motors(motors, motors_info):
    for i in range(len(motors)):
        motors[i].setDeviceSerialNumber(620000)
        motors[i].setHubPort(i)
        motors[i].setOnAttachHandler(onAttach(i))
        motors[i].setOnDetachHandler(onDetach)
        motors[i].setOnErrorHandler(onError)
        motors[i].openWaitForAttachment(5000)
        motors[i].setControlMode(StepperControlMode.CONTROL_MODE_RUN)
        motors[i].setCurrentLimit(motors_info[i][0])
        motors[i].setHoldingCurrentLimit(motors_info[i][1])
        motors[i].setRescaleFactor(1.8/ 16/motors_info[i][2])
        motors[i].setAcceleration(50)
        motors[i].setVelocityLimit(0)
        motors[i].setEngaged(True)
        motors[i].setDataInterval(motors[i].getMinDataInterval())



# -----------------------------------------------------  MAIN  ----------------------------------------------------------------------
# Declare and initialize motors and motor info (current limit, holding current, gear ratio)
base_motor = Stepper()           # Rotates base
base_motor_info = [2.8, 1, 77]
shoulder_motor1 = Stepper()      # Reference motor to rotate shoulder joint
shoulder_motor1_info = [2.8, 2.8, 15]
shoulder_motor2 = Stepper()      # Support motor to rotate shoulder joint (inverse of shoulder_motor1)
shoulder_motor2_info = [2.8, 0, 15]
elbow_motor = Stepper()          # Rotates elbow
elbow_motor_info = [2.8, 1, 15]
wrist_motor = Stepper()          # Rotates wrist
wrist_motor_info = [0.67, 0.67, 100]
claw_motor = Stepper()           # Pinches claw
claw_motor_info = [0.67, 0, 100]
             
all_motor_names = [base_motor, shoulder_motor1, shoulder_motor2, elbow_motor, wrist_motor, claw_motor]
all_motor_info = [base_motor_info, shoulder_motor1_info, shoulder_motor2_info, elbow_motor_info, wrist_motor_info, claw_motor_info]


try:
    Log.enable(LogLevel.PHIDGET_LOG_INFO, "PhidgetArmLog.log")
    initialize_motors(all_motor_names, all_motor_info)

    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:        
        listener.join()              
    #try:
    #    input("Press Enter to Stop\n")
    #except (Exception, KeyboardInterrupt):
    #    pass

    base_motor.close()
    shoulder_motor1.close()
    shoulder_motor2.close()
    elbow_motor.close()
    wrist_motor.close()
    claw_motor.close()

except PhidgetException as ex:
    #We will catch Phidget Exceptions here, and print the error informaiton.
    traceback.print_exc()
    print("")
    print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)


print("DONE")