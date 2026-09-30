import datetime
import csv

import serial

from pint import UnitRegistry
ureg = UnitRegistry()

def gramsToLbf(grams):
    return ((grams * ureg.gram).to("kg") * ureg.gravity).to("lbf").magnitude

ser = serial.Serial("COM3", 112500)

with open(f"output/{datetime.datetime.now().strftime("%Y%m%d-%H%M-")}output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    #headers
    writer.writerow(["Timestamp", "force (lbf)", "mass measurement (g)"])
    
    while True:
        serialOutput = ser.readline().decode().strip().split(",")
        
        if len(serialOutput) > 1:
            time = serialOutput[0]
            mass = -1 * float(serialOutput[1])
            force = gramsToLbf(mass)
        
            writer.writerow([time, force, mass])
            
            print(f"time: {time}s, force: {force}lbf, mass: {mass}g")
