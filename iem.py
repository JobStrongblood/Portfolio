'''
JOB STRONGBLOOD WOHALI
Instrument Environment Monitor (IEM)

DESCRIPTION:
My IEM reads temperature and relative humidity and then analyzes those readings 
to determine if said readings are safe for various instruments, namely, piano
and cello. This is important because poor temperature and humidity levels 
can cause wood instruments to warp and go out of tune. Dangerous conditions
occure when the temperature is too hot or cold, when the humidity is too dry or 
wet, OR when the temperature or humidity is rapidly changing. 
'''

import time
import os
import requests
import board
import busio
import adafruit_bme280.basic

'''
FUNCTION NAME: Check Previous
PARAMETERS: reading, prev_reading, spike
RETURN VALUES: True OR False
DESCRIPTION: If a previous reading exists (i.e. this is not the first reading), 
function checks if sampling has spiked by a certain amount ("spike") 
determined elsewhere in the code. This is to prevent the warning system from 
engaging if the sensor simply has one extreme reading (an "anamoly"). 
'''
def check_prev(reading, prev_reading, spike):
    if prev_reading != None:
        if abs(reading - prev_reading) < spike:
            return True
        else:
            return False
    else:
        return True 


'''
FUNCTION NAME: Warning
PARAMETERS: message, webhook_local
RETURN VALUES: none
DESCRIPTION: Function responsible for sending the discord webhook messages it does
not create the messages; it only sends what is passed into it. It also prints the 
message along with its success status to the terminal.
'''        
def warning(message, webhook_local):
    print(message)

    data = {
        "content": message
    }

    response = requests.post(webhook_local, json=data)

    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed: {response.status_code}")


'''
FUNCTION NAME: Send Alert
PARAMETERS: alert_key, message, webhook_local, last_alerts, cooldown_local
RETURN VALUES: none
DESCRIPTION: Cooldown time monitor. Function monitors specific alert types and prevents 
those alerts from being sent more than once within the determined cooldown period. 
Checks last_alerts_local dictionary to determine the time of the last alert of this type
and, if it has been longer than the cooldown period, function calls the Warning function
and sends the alert that's been passed into it. Following this, it updates the last alerts
dictionary entry of that specific alert to reflect the current time (i.e. updates the  last
timestamp record of that alert having been sent)
'''
def send_alert(alert_key, message, webhook_local, last_alerts_local, cooldown_local):
    last_time = last_alerts_local.get(alert_key, 0)

    if time.time() - last_time >= cooldown_local:
        warning(message, webhook_local)
        last_alerts_local[alert_key] = time.time()


'''
FUNCTION NAME: Message Maker
PARAMETERS: t_condition_local, h_condition_local, instrument, webhook_local, 
last_alerts_local, alert_cooldown_local
RETURN VALUES: none
DESCRIPTION: Function creates message based off of tagged environment conditions and then 
passes that message along to the send alert function. For example: if the temperature 
condition does not have a value of "fine", the function will create a message saying the 
temperature is off. It then pieces together the specific instrument that has been inputted 
into the function and the environmental condition and inputs it into the Send Alert function.
Having done this, it repeats the process for humidity.
'''   
def message_maker(t_condition_local, h_condition_local, instrument, webhook_local, last_alerts_local, alert_cooldown_local):
    if t_condition_local != "fine":
        send_alert(
            f"{instrument}_temp_{t_condition_local}",
            f"Too {t_condition_local} for {instrument}",
            webhook_local,
            last_alerts_local,
            alert_cooldown_local
        )

    if h_condition_local != "fine":
        send_alert(
            f"{instrument}_humid_{h_condition_local}",
            f"Too {h_condition_local} for {instrument}",
            webhook_local,
            last_alerts_local,
            alert_cooldown_local
        )

#creates I2C instance, connecting BME280 to Raspberry Pi
i2c = busio.I2C(board.SCL, board.SDA)

#sets the address to 0x76 (the default for the BME280)
bme280 = adafruit_bme280.basic.Adafruit_BME280_I2C(i2c, address=0x76)

temp_history = [] #empty list of temperature history
humid_history = [] #empty list of humidity history
WINDOW_SIZE = 180 #180 samples, one every ten secs (i.e. 30 mins total)
prev_time = time.time() #sets the previous time to the current time at the start of the program
sample_interval = 10 #one sample every 10 secs

webhook = "https://discord.com/api/webhooks/1495876346746896446/Te873Cb_quYSZQfmI9wcM-eu9fY-Tv4xKCSSg_Uu2yUNqyjCDjun3wvLJZhz3C8e977s"

piano_t_min = 65 #piano min temp
piano_t_max = 75 #piano max temp
piano_h_min = 35 #piano min humidity
piano_h_max = 55 #piano max humidity

cello_t_min = 65 #cello min temp
cello_t_max = 80 #cello max temp
cello_h_min = 35 #cello min humidity
cello_h_max = 60 #cello max humidity

last_alerts = {}
alert_cooldown = 900  # 15 minutes

#sensor anomaly proofing
MAX_TEMP_SPIKE = 2
MAX_HUMID_SPIKE = 5

while True:
    #resets values to defaulted "unnacceptable" so the program is looking for errors.
    acceptable_cello = False
    acceptable_piano = False

    try: #so the program doesn't crash if sensor read fails
        current_time = time.time() #sets current time
        if current_time - prev_time >= sample_interval: #makes the program sample no more than 1 time every 10 seconds
            print("loop alive") #useful for debugging, is usually deleted from UI with the os.system("clear") command
            prev_time += sample_interval #adds sample interval to previous time, effectively setting to current time. Written this way to prevent drift in sampling times.
                
            try:
                #name temp and humid variables as BME280 readings
                temp = (bme280.temperature * (9/5)) + 32 #converts BME temperature reading from Celsius to Fahrenheit
                humid = bme280.humidity 
            except Exception as e: #error handling
                print(f"Sensor read error: ", e) #prints error
                continue
            
            #resets terminal UI with commands dependent on operating system
            if os.name == "nt": #windows
                os.system('cls')
            else: #linux/MacOS
                os.system('clear')

            #print vaues for terminal UI view
            print("Temp:", temp)
            print("Humidity:", humid)

            #names variables for the LAST values in lists BEFORE appending new values
            if temp_history: #if values exist in the list
                prev_temp = temp_history[-1] 
            else:
                prev_temp = None
            if humid_history: #if values exist in the list
                prev_humid = humid_history[-1]
            else:
                prev_humid = None
            
            #append new readings to lists
            temp_history.append(temp)
            humid_history.append(humid)

            #if lists are too long, pop the first (oldest) value, keeping a scrolling window
                #this will only happen when the window has reached its max size
            if len(temp_history) > WINDOW_SIZE:
                temp_history.pop(0)

            if len(humid_history) > WINDOW_SIZE:
                humid_history.pop(0)

            #determines how much values have changes within window time
            temp_range = max(temp_history) - min(temp_history)
            humid_range = max(humid_history) - min(humid_history)

            #PIANO LEVEL SPIKE WARNINGS
                #allows temp to change by up to 3 degrees F
            if temp_range > 3 and check_prev(temp, prev_temp, MAX_TEMP_SPIKE) == True:
                send_alert(
                    "piano_temp_spike",
                    f"Temperature rapidly changing. Not safe for piano.",
                    webhook,
                    last_alerts,
                    alert_cooldown)
                #allows humidity to change by up to 5 percent
            if humid_range > 5 and check_prev(humid, prev_humid, MAX_HUMID_SPIKE) == True:
                send_alert(
                    "piano_humid_spike",
                    f"Humidity rapidly changing. Not safe for piano.",
                    webhook,
                    last_alerts,
                    alert_cooldown)

            #CELLO LEVEL SPIKE WARNINGS
            #cellos are more succeptible to fast changes of temp or humidity
                #allows temp to change by up to 2 degrees F 
            if temp_range > 2 and check_prev(temp, prev_temp, MAX_TEMP_SPIKE) == True:
                send_alert(
                    "cello_temp_spike",
                    f"Temperature rapidly changing. Not safe for cello.",
                    webhook,
                    last_alerts,
                    alert_cooldown)
                #allows humidity to change by up to 3 percent
            if humid_range > 8 and check_prev(humid, prev_humid, MAX_HUMID_SPIKE) == True:
                send_alert(
                    "cello_humid_spike",
                    f"Humidity rapidly changing. Not safe for cello.",
                    webhook,
                    last_alerts,
                    alert_cooldown)

        #GENERAL RANGE CHECKS - checks exact reading value rather than rate of change. Tags each instrument's environement with current conditions

            #PIANO TEMPERATURE CHECK
            if temp > piano_t_max:
                t_condition = "hot"
            elif temp < piano_t_min:
                t_condition = "cold"
            else:
                t_condition = "fine"
            
            #PIANO HUMIDITY CHECK
            if humid < piano_h_min:
                h_condition = "dry"
            elif humid > piano_h_max:
                h_condition = "humid"
            else:
                h_condition = "fine"

            #if both temp and humidity checks pass
            if piano_h_min <= humid <= piano_h_max and piano_t_min <= temp <= piano_t_max:
                acceptable_piano = True
                print("acceptable environment for piano")
            elif check_prev(temp, prev_temp, MAX_TEMP_SPIKE) == True and check_prev(humid, prev_humid, MAX_HUMID_SPIKE) == True:
                message_maker(
                    t_condition, 
                    h_condition, 
                    "piano", 
                    webhook, 
                    last_alerts, 
                    alert_cooldown)

            #CELLO TEMPERATURE CHECK
            if temp > cello_t_max:
                t_condition = "hot"
            elif temp < cello_t_min:
                t_condition = "cold"

            #CELLO HUMIDITY CHECK
            if humid < cello_h_min:
                h_condition = "dry"
            elif humid > cello_h_max:
                h_condition = "humid"

            #if both temp and humidity checks pass
            if cello_h_min <= humid <= cello_h_max and cello_t_min <= temp <= cello_t_max:
                acceptable_cello = True
                print("acceptable environment for cello")
            elif check_prev(temp, prev_temp, MAX_TEMP_SPIKE) == True and check_prev(humid, prev_humid, MAX_HUMID_SPIKE) == True:
                message_maker(
                    t_condition, 
                    h_condition, 
                    "cello", 
                    webhook, 
                    last_alerts, 
                    alert_cooldown)

    except ValueError:
        continue
