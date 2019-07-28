from .cue_sdk import *
import time

dir_path = str(__file__).replace("Corsair.py","DLLs/CUESDK.x64_2015.dll")
print("[INFO] Corsair ICUE DLL Path : " + str(dir_path))
cue = CUESDK(dir_path)
global debug
global DeviceList
global NewDeviceID
DeviceList = []
NewDeviceID = []

def range_float(start, stop, step):
    while start < stop:
        yield start
        start += step


def debug():
    global debug
    if debug:
        return True
    else:
        return False

def debugON():
    print("[DEBUG] Debug Enabled.")
    global debug
    debug = True

def debugOFF():
    print("[DEBUG] Debug Disabled.")
    global debug
    debug = False

def DeviceInfo():
    global DeviceList
    print(("[INFO] There are " + str(cue.get_device_count())) +" connected Corsair devices." )
    for i in range(cue.get_device_count()):
        print("Device #" + str(i+1) , str(cue.get_device_info(i))) # For all details about the devices
        #print("Device #" + str(i+1) , str(cue.get_device_info(i)[1])) # For just names
        thing_to_append = (str(cue.get_device_info(i)[1]) +"_" +str(cue.get_device_info(i)[0]))
        DeviceList.append(thing_to_append)
    return DeviceList

def RequestControl():
    cue.RequestControl(CAM.ExclusiveLightingControl)
    print("[INFO] Successfully Requested Corsair ICUE Control")

def ReleaseControl():
    cue.ReleaseControl(CAM.ExclusiveLightingControl)
    print("[INFO] Successfully Released Corsair ICUE Control")

def BlackLED(LED_ID):
    led_color = CorsairLedColor(LED_ID, 0, 0, 0)
    cue.set_led_colors(led_color)


def ledOn(LED_ID,RVal,GVal,BVal,Duration):
    if debug():
        print("[DEBUG] LED_ID :", str(LED_ID),"R :", str(RVal) ,"G :",str(GVal)," B :" , str(BVal) , "Duration :" , str(Duration))
    led_color = CorsairLedColor(LED_ID, RVal, GVal, BVal)
    cue.set_led_colors(led_color)
    time.sleep(Duration)


def ledSmoothOn(LED_ID,RVal,GVal,BVal,Duration):
    for x in range_float(0, 2, 0.1):
        NRval = int((1 - abs(x - 1)) * RVal)
        NGval = int((1 - abs(x - 1)) * GVal)
        NBval = int((1 - abs(x - 1)) * BVal)
        if debug():
            print("[DEBUG] LED_ID :", str(LED_ID), "R :", str(NRval), "G :", str(NGval), " B :", str(NBval), "Duration :", str(Duration))
        led_color = CorsairLedColor(LED_ID, NRval, NGval , NBval)
        cue.set_led_colors(led_color)
        time.sleep(Duration)

def DeviceID(DeviceList):
    print(DeviceList)
    global  NewDeviceID
    for i in range(len(DeviceList)):
        if ".Mousepad" in DeviceList[i]:
            NewDeviceID.append("4" + str(DeviceList[i].replace(".Mousepad","".replace("_CDT",""))))
    for i in range(len(DeviceList)):
        if ".Mouse" in DeviceList[i]:
            NewDeviceID.append("1" + str(DeviceList[i].replace(".Mouse", "").replace("_CDT","")))
    for i in range(len(DeviceList)):
        if ".Keyboard" in DeviceList[i]:
            NewDeviceID.append("2" + str(DeviceList[i].replace(".Keyboard", "").replace("_CDT","")))
    for i in range(len(DeviceList)):
        if ".Headset" in DeviceList[i]:
            NewDeviceID.append("3" + str(DeviceList[i].replace(".Headset", "").replace("_CDT","")))
    return NewDeviceID



def KeyboardCheck():
    global NewDeviceID
    if ".Keyboard" in DeviceList:
        if "K95 RGB PLATINUM" in DeviceList:
            ledOn(CLK.G1, 0, 255, 0, 0.1)
            ledOn(CLK.G2, 0, 255, 0, 0.1)
            ledOn(CLK.G3, 0, 255, 0, 0.1)
            ledOn(CLK.G4, 0, 255, 0, 0.1)
            ledOn(CLK.G5, 0, 255, 0, 0.1)
            ledOn(CLK.G6, 0, 255, 0, 0.1)

            ledOn(CLK.G1, 0, 0, 0, 0.1)
            ledOn(CLK.G2, 0, 0, 0, 0.1)
            ledOn(CLK.G3, 0, 0, 0, 0.1)
            ledOn(CLK.G4, 0, 0, 0, 0.1)
            ledOn(CLK.G5, 0, 0, 0, 0.1)
            ledOn(CLK.G6, 0, 0, 0, 0.1)

            '''
            I do know that using for or while loop would be more effective way to do this.
            However, this process is to check all the dependencies were correctly installed. 
    
            If the importing cue_sdk module was not complete nor successful, CLK.G keys would be showing errors on the CLK is not defined.
            '''

            for i in range(170, 188, 1):
                ledOn(i, 0, 255, 0, 0.01)
                ledOn(i + 1, 0, 255, 0, 0.01)

            for i in range(170, 188, 1):
                ledOn(i, 0, 0, 0, 0.01)
                ledOn(i + 1, 0, 0, 0, 0.01)

            for i in range(188, 170, -1):
                ledOn(i, 0, 255, 0, 0.01)
                ledOn(i + 1, 0, 255, 0, 0.01)

            for i in range(188, 170, -1):
                ledOn(i, 0, 0, 0, 0.01)
                ledOn(i + 1, 0, 0, 0, 0.01)

            '''
            If this function was correctly executed, it means that there would be no issues when controlling Corsair ICUE SDK.
            At least for me, my pheperials (K95 RGB , Glaive , Void , MM800) were ready for me to control LEDs.
    
            If this crashes, The key LED mapping would be mismatched.  
    
            '''

        if "K95 RGB PLATINUM" not in DeviceList:
            for i in range(2):
                ledSmoothOn(CLK.Space, 0, 255, 0, 0.01)
            for i in range(1, 12, 1):
                ledOn(i, 0, 255, 0, 0.1)
            for i in range(1, 12, 1):
                ledOn(i, 0, 0, 0, 0.1)
            ledOn(CLK.F12, 0, 0, 0, 0.1)

        for i in range(len(NewDeviceID)):
            if NewDeviceID[i][1] == 2:
                print("[INFO]" , str(DeviceList[i].replace("2","")) , "Connected")
    else:
        print("[INFO] No Corsair Keyboard Detected")


def MousePadCheck():
    global NewDeviceID

    if "MM800RGB" in DeviceList:
        for i in range(2):
            ledSmoothOn(CLK.MM800_1, 0, 255, 0, 0.01)

        for i in range(155 , 160 , 1 ):
            ledOn(i, 0, 255, 0, 0.1)

        for i in range(155, 160, 1):
            ledOn(i, 0, 0, 0, 0.1)

        for i in range(len(NewDeviceID)):
            if NewDeviceID[i][1] == 4:
                print("[INFO]" , str(DeviceList[i].replace("4","")) , "Connected")
    else:
        print("[INFO] No Corsair Mouse Pad Detected")

def MouseCheck():
    global NewDeviceID

    if "GLAIVE RGB" in DeviceList:
        for i in range(2):
            ledSmoothOn(CLK.GLAV_2, 0, 255, 0, 0.01)

        for i in [CLK.GLAV_1 , CLK.GLAV_2 , CLK.GLAV_3]:
            ledOn(i, 0, 255, 0, 0.1)

        for i in [CLK.GLAV_1 , CLK.GLAV_2 , CLK.GLAV_3]:
            ledOn(i, 0, 0, 0, 0.1)

        for i in range(len(NewDeviceID)):
            if NewDeviceID[i][1] == 1:
                print("[INFO]" , str(DeviceList[i].replace("1","")) , "Connected")

    else:
        print("[INFO] No Corsair Mouse Pad Detected")


def HeadPhoneCheck():
    global NewDeviceID

    if "VOID PRO USB" in DeviceList:
        for i in range(2):
            ledSmoothOn(CLK.VOIDPRO_L, 0, 255, 0, 0.01)

        for i in [CLK.VOIDPRO_L , CLK.VOIDPRO_R]:
            ledOn(i, 0, 255, 0, 0.1)

        for i in [CLK.VOIDPRO_L , CLK.VOIDPRO_R]:
            ledOn(i, 0, 0, 0, 0.1)

        for i in range(len(NewDeviceID)):
            if NewDeviceID[i][1] == 3:
                print("[INFO]", str(DeviceList[i].replace("3", "")), "Connected")
    else:
        print("[INFO] No Corsair HeadPhone Pad Detected")



def FirstInit():
    RequestControl()


    KeyboardCheck()
    MousePadCheck()
    MouseCheck()
    HeadPhoneCheck()
