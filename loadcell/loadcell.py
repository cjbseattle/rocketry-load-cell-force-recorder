import datetime
import csv

import serial

from pint import UnitRegistry
ureg = UnitRegistry()

def massToForce(startMass, startType, endType):
    return ((startMass * ureg.Unit(startType)).to("kg") * ureg.gravity).to_compact(endType).magnitude

ser = serial.Serial("COM3", 112500)

with open(f"output/{datetime.datetime.now().strftime("%Y%m%d-%H%M-")}output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    #headers
    writer.writerow(["Timestamp", "force (lbf)", "force (N)", "mass measurement (g)"])
    
    while True:
        serialOutput = ser.readline().decode().strip().split(",")
        
        if len(serialOutput) > 1:
            time = serialOutput[0]
            massG = -1 * float(serialOutput[1])
            forceLbf = massToForce(massG, "g", "lbf")
            forceN = massToForce(massG, "g", "N")
        
            writer.writerow([time, forceLbf, forceN, massG])
            
            print(f"time: {time}s, force: {forceLbf}lbf, {forceN}N mass: {massG}g")
