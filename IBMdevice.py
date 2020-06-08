import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "h4div4"
deviceType = "raspberrypi"
deviceId = "12345"
authMethod = "token"
authToken = "70324836"
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        '''print(type(cmd.data))
        i=cmd.data['command']
        if i=='RED':
                print("pleasestopthevehicle")
        elif i=='ORANGE':
                print("Readytogo")
        elif i=='GREEN':
                print("Go")'''
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()
# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
while True:
        aqi=random.randint(50, 300)
        #print(aqi)
        noise =random.randint(10, 120)
        #Send Noise & Airqualityindex to IBM Watson
        data = { 'Noise' : noise, 'Airqualityindex': aqi }
        #print (data)
        def myOnPublishCallback():
            print ("Published Noise = %s db" % noise, "Airqualityindex = %s ppm" % aqi, "to IBM Watson")
        success = deviceCli.publishEvent("Pollution", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        deviceCli.commandCallback = myCommandCallback
# Disconnect the device and application from the cloud
deviceCli.disconnect()

