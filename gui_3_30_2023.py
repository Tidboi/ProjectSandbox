import tkinter as tk
import time
import json
import serial
import os

saveButton = None
homeButton = None
warmButton = None
bakeButton = None
targetButton = None

checkWarmHoldTask = None
checkBakeHoldTask = None
pressStartTime = 0
heatStartTime = 0
bakeTempSetting = 80
bakeTimeSetting = 120
warmTempSetting = 20
warmTimeSetting = 90
currentTemp = 0.0
updateTimer = 0.0
stopUpdate = False
buttonsDisabled = False
cancelTimer = False
ser = None

filepath = "/home/eet3tz/Project_Repo/dev-sandbox/Projects/"
bakepath = os.path.join(filepath , "bakeSettings.json")
warmpath = os.path.join(filepath , "warmSettings.json")

def connectSerial():
    global ser
    num = 0
    
    while(1):
        myPort = '/dev/ttyUSB'  + str(num)
        try:
            ser = serial.Serial(port=myPort,baudrate=57600,bytesize=serial.SEVENBITS,parity=serial.PARITY_ODD,timeout=0.1)
            break
        except:
            if num >= 3:
                num = 0
            else:
                num = num + 1
            time.sleep(2)
    
    time.sleep(0.05)
    ser.write("INTYPE A, 1, 0, 0, 0, 2\n".encode())
    time.sleep(0.05)
    ser.write("INCRV A, 02\n".encode())
    time.sleep(0.05)
    ser.write("FILTER A, 1, 8, 1\n".encode())
    time.sleep(0.05)
    ser.write("TLIMIT A, 373\n".encode())
    time.sleep(0.05)
    ser.write("OUTMODE 1, 1, 1, 0\n".encode())
    time.sleep(0.05)
    ser.write("PID 1, 50, 20, 0\n".encode())
    time.sleep(0.05)
    ser.write("RAMP 1, 0, 0\n".encode())
    time.sleep(0.05)
    ser.write("HTRSET 1, 0, 2, 0, 0.4, 1\n".encode())
    time.sleep(0.05)
    ser.write("RANGE 1, 0\n".encode())
    time.sleep(0.05)
    ser.write("MOUT 1, 0\n".encode())
    time.sleep(0.05)

def clear_frame():
    for widget in window.winfo_children():
        widget.destroy()

def checkBakeHold():
    global pressStartTime
    if pressStartTime > 0:
        pressStartTime = 0
        bakeSettingsScreen()
        
def bakePress(event):
    global pressStartTime
    global checkBakeHoldTask
    global buttonsDisabled
    
    if buttonsDisabled:
        return
    
    if pressStartTime == 0:
        pressStartTime = time.time()
        checkBakeHoldTask = window.after(3000, checkBakeHold)
    
def bakeRelease(event):
    global pressStartTime
    global checkBakeHoldTask
    global buttonsDisabled
    
    if buttonsDisabled:
        return
    
    window.after_cancel(checkBakeHoldTask)
    if (time.time() - pressStartTime) < 5:
        bakeOutScreen()
    pressStartTime = 0
        
def checkWarmHold():
    global pressStartTime
    if pressStartTime > 0:
        pressStartTime = 0
        warmSettingsScreen()
        
def warmPress(event):
    global pressStartTime
    global checkWarmHoldTask
    global buttonsDisabled
    
    if buttonsDisabled:
        return
    
    if pressStartTime == 0:
        pressStartTime = time.time()
        checkWarmHoldTask = window.after(3000, checkWarmHold)
    
def warmRelease(event):
    global pressStartTime
    global checkWarmHoldTask
    global buttonsDisabled
    
    if buttonsDisabled:
        return
    
    window.after_cancel(checkWarmHoldTask)
    if (time.time() - pressStartTime) < 5:
        warmUpScreen()
    pressStartTime = 0

def targetPress(event):
    global pressStartTime
    global checktargetHoldTask
    global buttonsDisabled
    
    if buttonsDisabled:
        return
    
    if pressStartTime == 0:
        pressStartTime = time.time()
        checktargetHoldTask = window.after(3000, checktargetHold)
    
def targetRelease(event):
    global pressStartTime
    global checktargetHoldTask
    global buttonsDisabled
    
    if buttonsDisabled:
        return
    
    window.after_cancel(checktargetHoldTask)
    if (time.time() - pressStartTime) < 5:
        targetUpScreen()
    pressStartTime = 0

def stopHeat():
    global heatStartTime
    heatStartTime = 0
    
    ser.write("RANGE 1, 0\n".encode())
    
    #clear_frame()
    mainScreen()
    
def incrementBakeTemp():
    global bakeTempSetting
    bakeTempSetting = bakeTempSetting + 1
    if bakeTempSetting > 80:
        bakeTempSetting = 80
    bakeTempStringVar.set(str(bakeTempSetting)  + " C")

def decrementBakeTemp():
    global bakeTempSetting
    bakeTempSetting = bakeTempSetting - 1
    if bakeTempSetting < 60:
        bakeTempSetting = 60
    bakeTempStringVar.set(str(bakeTempSetting) + " C")
    
def incrementBakeTime():
    global bakeTimeSetting
    bakeTimeSetting = bakeTimeSetting + 5
    if bakeTimeSetting > 900:
        bakeTimeSetting = 900
    bakeTimeStringVar.set(str(bakeTimeSetting) + " Mins")

def decrementBakeTime():
    global bakeTimeSetting
    bakeTimeSetting = bakeTimeSetting - 5
    if bakeTimeSetting < 5:
        bakeTimeSetting = 5
    bakeTimeStringVar.set(str(bakeTimeSetting) + " Mins")
    
def incrementWarmTemp():
    global warmTempSetting
    warmTempSetting = warmTempSetting + 1
    if warmTempSetting > 40:
        warmTempSetting = 40
    warmTempStringVar.set(str(warmTempSetting)  + " C")

def decrementWarmTemp():
    global warmTempSetting
    warmTempSetting = warmTempSetting - 1
    if warmTempSetting < 20:
        warmTempSetting = 20
    warmTempStringVar.set(str(warmTempSetting)  + " C")
    
def incrementWarmTime():
    global warmTimeSetting
    warmTimeSetting = warmTimeSetting + 5
    if warmTimeSetting > 900:
        warmTimeSetting = 900
    warmTimeStringVar.set(str(warmTimeSetting) + " Mins")

def decrementWarmTime():
    global warmTimeSetting
    warmTimeSetting = warmTimeSetting - 5
    if warmTimeSetting < 5:
        warmTimeSetting = 5
    warmTimeStringVar.set(str(warmTimeSetting) + " Mins")

def saveBakeSettings():
    global saveButton
    global homeButton
    
    bakeSettings = {"temp":bakeTempSetting,"time":bakeTimeSetting}
    with open(bakepath, "w+") as outfile:
        json.dump(bakeSettings, outfile)
    #homeButton.configure(state="disabled")
    #saveButton.configure(state="disabled")
    if saveButton != None:
        i = 0
        for i in range(0,5):
            saveButton.configure(bg='green')
            saveButton.configure(activebackground='green')
            window.update()
            time.sleep(0.25)
            saveButton.configure(bg='orange')
            saveButton.configure(activebackground='orange')
            window.update()
            time.sleep(0.25)
            i = i + 1

    #homeButton.configure(state="active")
    #saveButton.configure(state="active")


def saveWarmSettings():
    global saveButton
    global homeButton
    
    warmSettings = {"temp":warmTempSetting,"time":warmTimeSetting}
    with open(warmpath, "w+") as outfile:
        json.dump(warmSettings, outfile)
    
    #homeButton.configure(state="disabled")
    #saveButton.configure(state="disabled")
    if saveButton != None:
        i = 0
        for i in range(0,5):
            saveButton.configure(bg='green')
            saveButton.configure(activebackground='green')
            window.update()
            time.sleep(0.25)
            saveButton.configure(bg='orange')
            saveButton.configure(activebackground='orange')
            window.update()
            time.sleep(0.25)
            i = i + 1
    #homeButton.configure(state="active")
    #saveButton.configure(state="active")
    


def update():
    global stopUpdate
    global currentTemp
    global updateTimer
    global warmButton
    global bakeButton
    global buttonsDisabled
    global cancelTimer
    
    if updateTimer == 0:
        updateTimer = time.time()
    elif time.time() - updateTimer > 1:      
        if not stopUpdate:
            ser.write("CRDG?\n".encode())
            response=ser.read(10).decode()
            try:
                response=response.splitlines()[0]
                try:
                    response=response.split('+')[1]
                except:
                    pass
                response = str(round(float(response),1))
                currentTemp = float(response)
                if currentTemp == -273.1:
                    tempStringVar.set("-- C")
                    if heatStartTime > 0:
                        cancelTimer = True
                    if warmButton != None and bakeButton != None and buttonsDisabled == False:
                        buttonsDisabled = True
                else:
                    cancelTimer = False
                    tempStringVar.set(response  + " C")
                    if warmButton != None and bakeButton != None and buttonsDisabled == True:
                        warmButton.configure(state="active")
                        bakeButton.configure(state="active")
                        buttonsDisabled = False
                        mainScreen()
            except:
                print("Error")
                
            updateTimer = 0
    #window.update()
    window.after(10, update)

def bakeTimer():
    global currentTemp
    global bakeTempSetting
    global bakeTimeSetting
    global heatStartTime
    global cancelTimer
    
    if cancelTimer == True:
        heatStartTime = 0
        stopHeat()
        return
    
    if heatStartTime == 0:
        heatStartTime = time.time()
    elif ((time.time() - heatStartTime) / 60) >= bakeTimeSetting:
        heatStartTime = 0
        stopHeat()
        return
    window.after(1000, bakeTimer)
    
def warmTimer():
    global currentTemp
    global warmTempSetting
    global warmTimeSetting
    global heatStartTime
    global cancelTimer
    
    if cancelTimer == True:
        heatStartTime = 0
        stopHeat()
        return
    
    if heatStartTime == 0:
        heatStartTime = time.time()
    elif ((time.time() - heatStartTime) / 60) >= warmTimeSetting:
        heatStartTime = 0
        stopHeat()
        return
    window.after(1000, warmTimer)
    

def bakeOutScreen():
    clear_frame()
    
    global stopUpdate
    stopUpdate = False
    
    ser.flushInput()
    setTemp = "SETP 1, " + str(bakeTempSetting) + "\n"
    ser.write(setTemp.encode())
    time.sleep(0.05)
    ser.write("RANGE 1, 3\n".encode())
    
    bakeOutLabel=tk.Label(window, text="BAKE OUT", font=("Helvetica", 32))
    bakeOutLabel.place(relx=0.5,rely=0.15,anchor='center')
    
    tempLabel=tk.Label(window, textvariable=tempStringVar, fg='red', font=("Helvetica", 96))
    tempLabel.place(relx=0.5,rely=0.5,anchor='center')
    
    stopButton=tk.Button(window, text='STOP', bg='red', height=2, width=8, fg='white', font=("Helvetica", 34), activeforeground='white', activebackground='red', command=stopHeat)
    stopButton.place(relx=0.5,rely=0.80,anchor='center')
    window.after(1000, bakeTimer)
    window.after(10, update)
    

def warmUpScreen():
    clear_frame()
    
    global stopUpdate
    stopUpdate = False
    
    ser.flushInput()
    setTemp = "SETP 1, " + str(warmTempSetting) + "\n"
    ser.write(setTemp.encode())
    time.sleep(0.05)
    ser.write("RANGE 1, 3\n".encode())
    
    warmUpLabel=tk.Label(window, text="WARM UP", font=("Helvetica", 32))
    warmUpLabel.place(relx=0.5,rely=0.15,anchor='center')
    
    tempLabel=tk.Label(window, textvariable=tempStringVar, fg='red', font=("Helvetica", 96))
    tempLabel.place(relx=0.5,rely=0.5,anchor='center')
    
    stopButton=tk.Button(window, text='STOP', bg='red', height=2, width=8, fg='white', font=("Helvetica", 34), activeforeground='white', activebackground='red', command=stopHeat)
    stopButton.place(relx=0.5,rely=0.80,anchor='center')
    window.after(1000, warmTimer)
    window.after(10, update)
    

def bakeSettingsScreen():
    clear_frame()
    
    global stopUpdate
    stopUpdate = True
    
    global homeButton
    homeButton=tk.Button(window, text='HOME', height=2, width=6, fg='white', bg='orange', font=("Helvetica",28), activeforeground='white', activebackground='orange', command=mainScreen)
    homeButton.place(relx=0.12, rely=0.15, anchor='center')
    
    global saveButton
    saveButton=tk.Button(window, text='SAVE', height=2, width=6, fg='white', bg='orange', font=("Helvetica",28), activeforeground='white', activebackground='orange', command=saveBakeSettings)
    saveButton.place(relx=0.88, rely=0.15, anchor='center')
    
    bakeOutLabel=tk.Label(window, text="BAKE OUT", font=("Helvetica", 48))
    bakeOutLabel.place(relx=0.5, rely=0.45, anchor='center')
    
    tempTextLabel=tk.Label(window, text="TEMP:", font=("Helvetica",34), fg='orange')
    tempTextLabel.place(relx=0.12, rely=0.68, anchor='center')
    
    tempLabel=tk.Label(window, textvariable=bakeTempStringVar, font=("Helvetica",34))
    tempLabel.place(relx=0.3, rely=0.68, anchor='center')
    
    timeTextLabel=tk.Label(window, text="TIME:", font=("Helvetica",34), fg='orange')
    timeTextLabel.place(relx=0.68,rely=0.68,anchor='center')
    
    timeLabel=tk.Label(window, textvariable=bakeTimeStringVar, font=("Helvetica",34))
    timeLabel.place(relx=0.88,rely=0.68,anchor='center')
    
    incTempButton=tk.Button(window, text="+1", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=incrementBakeTemp)
    incTempButton.place(relx=0.1, rely=0.85, anchor='center')
    
    decTempButton=tk.Button(window, text="-1", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=decrementBakeTemp)
    decTempButton.place(relx=0.3, rely=0.85, anchor='center')
    
    incTimeButton=tk.Button(window, text="+5", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=incrementBakeTime)
    incTimeButton.place(relx=0.7, rely=0.85, anchor='center')
    
    decTimeButton=tk.Button(window, text="-5", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=decrementBakeTime)
    decTimeButton.place(relx=0.9, rely=0.85, anchor='center')
    

def warmSettingsScreen():
    clear_frame()
    
    global stopUpdate
    stopUpdate = True
    
    global homeButton
    homeButton=tk.Button(window, text='HOME', height=2, width=6, fg='white', bg='orange', font=("Helvetica",28), activeforeground='white', activebackground='orange', command=mainScreen)
    homeButton.place(relx=0.12, rely=0.15, anchor='center')
    
    global saveButton
    saveButton=tk.Button(window, text='SAVE', height=2, width=6, fg='white', bg='orange', font=("Helvetica",28), activeforeground='white', activebackground='orange', command=saveWarmSettings)
    saveButton.place(relx=0.88, rely=0.15, anchor='center')
    
    
    warmUpLabel=tk.Label(window, text="WARM UP", font=("Helvetica", 48))
    warmUpLabel.place(relx=0.5, rely=0.45, anchor='center')
    
    tempTextLabel=tk.Label(window, text="TEMP:", font=("Helvetica",34), fg='orange')
    tempTextLabel.place(relx=0.12, rely=0.68, anchor='center')
    
    tempLabel=tk.Label(window, textvariable=warmTempStringVar, font=("Helvetica",34))
    tempLabel.place(relx=0.3, rely=0.68, anchor='center')
    
    timeTextLabel=tk.Label(window, text="TIME:", font=("Helvetica",34), fg='orange')
    timeTextLabel.place(relx=0.68,rely=0.68,anchor='center')
    
    timeLabel=tk.Label(window, textvariable=warmTimeStringVar, font=("Helvetica",34))
    timeLabel.place(relx=0.88,rely=0.68,anchor='center')
    
    incTempButton=tk.Button(window, text="+1", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=incrementWarmTemp)
    incTempButton.place(relx=0.1, rely=0.85, anchor='center')
    
    decTempButton=tk.Button(window, text="-1", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=decrementWarmTemp)
    decTempButton.place(relx=0.3, rely=0.85, anchor='center')
    
    incTimeButton=tk.Button(window, text="+5", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=incrementWarmTime)
    incTimeButton.place(relx=0.7, rely=0.85, anchor='center')
    
    decTimeButton=tk.Button(window, text="-5", height=2, width=4, font=("Helvetica",24), fg='white', bg='orange', activeforeground='white', activebackground='orange', command=decrementWarmTime)
    decTimeButton.place(relx=0.9, rely=0.85, anchor='center')
    


def mainScreen():   
    clear_frame()
    
    global stopUpdate
    global warmButton
    global bakeButton
    stopUpdate = False
    
    #Bake out button
    bakeButton=tk.Button(window, text='BAKE OUT', height=2, width=10, bg='orange', fg='white', font=("Helvetica", 38), activeforeground='white', activebackground='orange')
    bakeButton.place(relx=0.25,rely=0.8, anchor='center')

    bakeBindPress = bakeButton.bind("<ButtonPress>", bakePress)
    bakeBindRelease = bakeButton.bind("<ButtonRelease>", bakeRelease)

    #Warm up button
    warmButton=tk.Button(window, text='WARM UP', height=2, width=10, bg='orange', fg='white', font=("Helvetica", 38), activeforeground='white', activebackground='orange') 
    warmButton.place(relx=0.75,rely=0.8, anchor='center')

    warmBindPress = warmButton.bind("<ButtonPress>", warmPress)
    warmBindRelease = warmButton.bind("<ButtonRelease>", warmRelease)

    #Target button
    targetButton=tk.Button(window, text='target UP', height=2, width=10, bg='orange', fg='white', font=("Helvetica", 38), activeforeground='white', activebackground='orange') 
    targetButton.place(relx=0.125,rely=0.8, anchor='center')

    targetBindPress = targetButton.bind("<ButtonPress>", targetPress)
    targetBindRelease = targetButton.bind("<ButtonRelease>", targetRelease)

    if buttonsDisabled == True:
        warmButton.configure(state="disabled")
        bakeButton.configure(state="disabled")
        targetButton.configure(state="disabled")

        warmButton.unbind("<ButtonPress>", warmBindPress)
        warmButton.unbind("<ButtonRelease>", warmBindRelease)

        bakeButton.unbind("<ButtonPress>", bakeBindPress)
        bakeButton.unbind("<ButtonRelease>", bakeBindRelease)

        targetButton.unbind("<ButtonPress>", bakeBindPress)
        targetButton.unbind("<ButtonRelease>", bakeBindRelease)
    
    tempLabel=tk.Label(window, textvariable=tempStringVar, font=("Helvetica",96))
    tempLabel.place(relx=0.5,rely=0.5, anchor='center')
    
    window.after(10, update)
    
try:
    with open(bakepath,"r") as openfile:
        json_object = json.load(openfile)
        bakeTempSetting = json_object["temp"]
        bakeTimeSetting = json_object["time"]
except:
    saveBakeSettings()
    
try:
    with open(warmpath,"r") as openfile:
        json_object = json.load(openfile)
        warmTempSetting = json_object["temp"]
        warmTimeSetting = json_object["time"]
except:
    saveWarmSettings()

window=tk.Tk()

#String vars
tempStringVar = tk.StringVar()
tempStringVar.set(str(round(currentTemp, 1))  + " C")

bakeTempStringVar = tk.StringVar()
bakeTempStringVar.set(str(bakeTempSetting)  + " C")

bakeTimeStringVar = tk.StringVar()
bakeTimeStringVar.set(str(bakeTimeSetting) + " Mins")

warmTempStringVar = tk.StringVar()
warmTempStringVar.set(str(warmTempSetting)  + " C")

warmTimeStringVar = tk.StringVar()
warmTimeStringVar.set(str(warmTimeSetting) + " Mins")

window.title("TITLE")
window.geometry('800x480')

# connectSerial()
# ser.flushInput() 

mainScreen()

window.wm_attributes('-fullscreen', 'True')
# window.config(cursor="none")
tk.mainloop()
              
