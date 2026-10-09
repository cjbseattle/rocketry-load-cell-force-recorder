import datetime
import csv
import random
import time
import keyboard
import threading

import serial
from pint import UnitRegistry
ureg = UnitRegistry()

"""
yes...

i know this code sucks okay

i know this is spaghetti code and is terrible

but it works (or should work)

and i dont care to make it good
"""

def askUntil(acceptedValues: list[str], askMessage: str):
    response = input(askMessage).lower()
    
    while response not in acceptedValues:
        response = input(askMessage).lower()
    
    return response

def massToForce(startMass: float, startType: float, endType: float):
    return ((startMass * ureg.Unit(startType)).to("kg") * ureg.gravity).to(endType).magnitude

active = threading.Event()
startRequested = threading.Event()
exitRequested = threading.Event()

debug = askUntil(["y", "n"], "debug? (y/n) ") == "y"
debugSave = askUntil(["y", "n"], "save debug to file? (y/n) ") == "y"
print()

if not debug:
    ser = serial.Serial("COM3", 112500)
elif debug and debugSave:
    print("ok, debug enabled and logging to file\n")
elif debug and not debugSave:
    print("ok, debug enabled and not logging to file\n")

print("keybinds:")
print("space - begin/end recording")
print("esc - exit program")
print("\npress space to continue . . .\n")

def newTest():
    fileDir = f"output/{datetime.datetime.now().strftime("%Y%m%d-%H%M-")}output.csv"
    
    print(f"new log starting for {fileDir}")
    if not debugSave:
        print("(but not saving in the file)")
    print()
    
    time.sleep(1)
    print("starting in . . .")
    for i in range(3, 0, -1):
        print(f"{i}")
        time.sleep(1)
    print()
    
    elapsedTime = 0.0
    massG = random.uniform(-10.0, 10.0)
    
    if not debug or debugSave:
        with open(fileDir, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            
            #headers
            writer.writerow(["Timestamp", "force (lbf)", "force (N)", "mass measurement (g)"])
            
            while active.is_set():
                if not debug:
                    serialOutput = ser.readline().decode().strip().split(",")
                    
                    if len(serialOutput) > 1:
                        elapsedTime = serialOutput[0]
                        massG = -1 * float(serialOutput[1])
                        forceLbf = massToForce(massG, "g", "lbf")
                        forceN = massToForce(massG, "g", "N")
                        
                        writer.writerow([elapsedTime, forceLbf, forceN, massG])
                else:
                    time.sleep(0.01)
                    
                    elapsedTime += 0.01
                    massG += random.uniform(-0.5, 0.5)
                    forceLbf = massToForce(massG, "g", "lbf")
                    forceN = massToForce(massG, "g", "N")
                    
                    writer.writerow([elapsedTime, forceLbf, forceN, massG])
                
                if active:
                    print(f"time: {elapsedTime:04.2f}s, force: {forceLbf:07.3f}lbf, {forceN:07.3f}N mass: {massG:07.3f}g")
    elif debug and not debugSave:
        while active.is_set():
            time.sleep(0.01)
                                
            elapsedTime += 0.01
            massG += random.uniform(-0.5, 0.5)
            forceLbf = massToForce(massG, "g", "lbf")
            forceN = massToForce(massG, "g", "N")

            if active:
                print(f"time: {elapsedTime:04.2f}s, force: {forceLbf:07.3f}lbf, {forceN:07.3f}N mass: {massG:07.3f}g")
        
    print(f"\ntest complete for {fileDir}\n")
    
    print("press esc to exit . . .\npress space to record again . . .\n")

def onSpacePressed():
    if active.is_set():
        active.clear()
    else:
        startRequested.set()

def onEscPressed():
    exitRequested.set()
    active.clear()

keyboard.add_hotkey("space", onSpacePressed)
keyboard.add_hotkey("esc", onEscPressed)

keyboard.wait("space")

while not exitRequested.is_set():
    if startRequested.is_set():
        startRequested.clear()
        active.set()
        newTest()