# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
# Importeer bibliotheek voor systeemfuncties.
import sys
import spidev
spi = spidev.SpiDev()
import time
import threading
import datetime
import lcddriver
lcd = lcddriver.lcd()
lcd.lcd_clear()
from RPi import GPIO

#US
TRIG=23
ECHO=24
#TEMP
DQ=4
#MOTOREN
motor1=21 #FRUITSAP POMP1
motor4=26 #PASSOA POMP4
motor2=19 #SAFARI POMP2
motor3=13 #PISANG POMP3
buzzer=20
#BUZZER

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(DQ,GPIO.IN)
GPIO.setup(motor1,GPIO.OUT)
GPIO.setup(motor2,GPIO.OUT)
GPIO.setup(motor3,GPIO.OUT)
GPIO.setup(motor4,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)





app = Flask(__name__)
app.config['SECRET_KEY'] = '55443322110'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
status= "0"
temp = "0"

# GPIO.output(led1,1)
# time.sleep(2)
# GPIO.output(led1,0)
# print('start')
# GPIO.output(19,1)
# time.sleep(13) #ALCOHOL TIJD
# GPIO.output(19,0)
# time.sleep(2)
# GPIO.output(21,1)
# time.sleep(10)  #FRUITSAP TIJD
# GPIO.output(21,0)
# time.sleep(2)
# GPIO.output(19,1)
# time.sleep(13) #ALCOHOL TIJD
# GPIO.output(19,0)
# time.sleep(2)
# GPIO.output(21,1)
# time.sleep(10)  #FRUITSAP TIJD
# GPIO.output(21,0)


# time.sleep(2)
# GPIO.output(13,1)
# time.sleep(5)
# GPIO.output(13,0)
# time.sleep(2)
# GPIO.output(26,1)
# time.sleep(5)
# GPIO.output(26,0)
# time.sleep(2)

lcd.lcd_clear()


#DataRepository.create_new_row()
def motor(FRUITSAP,ALCOHOL):
    print('start')
    GPIO.output(ALCOHOL,1)
    time.sleep(13)
    GPIO.output(ALCOHOL,0)
    time.sleep(2)
    GPIO.output(FRUITSAP,1)
    time.sleep(10)
    GPIO.output(FRUITSAP,0)
    time.sleep(2)
    GPIO.output(ALCOHOL,1)
    time.sleep(13)
    GPIO.output(ALCOHOL,0)
    time.sleep(2)
    GPIO.output(FRUITSAP,1)
    time.sleep(10)
    GPIO.output(FRUITSAP,0)
    

def motor_reinigen(FRUITSAP,PASSOA,PISANG,SAFARI):
    lcd.lcd_display_string('Reiniging bezig')
    GPIO.output(FRUITSAP,1)
    time.sleep(15)
    GPIO.output(FRUITSAP,0)

    time.sleep(1)

    GPIO.output(PISANG,1)
    time.sleep(15)
    GPIO.output(PISANG,0)

    time.sleep(1)

    GPIO.output(PASSOA,1)
    time.sleep(15)
    GPIO.output(PASSOA,0)

    time.sleep(1)

    GPIO.output(SAFARI,1)
    time.sleep(15)
    GPIO.output(SAFARI,0)

    time.sleep(1)
    lcd.lcd_display_string('Reiniging Klaar')
    time.sleep(5)
    lcd.lcd_clear()
def temperatuur_functie():
    sensorids = "28-0217b00ad1ff"
    tfile = open("/sys/bus/w1/devices/"+ sensorids +"/w1_slave") #RPi 2,3 met nieuwe kernel.
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    # Splits de regel in "woorden", er wordt gespleten op de spaties.
    # We selecteren hier het 10 "woord" [9] (tellend vanaf 0)
    temperaturedata = secondline.split(" ")[9]
    # De eerste 2 karakters zijn "t=", deze moeten we weghalen.
    # we maken meteen van de string een integer (nummer).
    temperature = float(temperaturedata[2:])
    # De temperatuurwaarde moeten we delen door 1000 voor de juiste waarde.
    temp = temperature / 1000
    print(f"Graden in Celsius = {temp}")

    return temp

def FSR():
    class MCP:
        @staticmethod
        def init():
            spi.open(0,0)   
            spi.max_speed_hz = 10 ** 5  
        
        @staticmethod
        def read_channel(channel):
            spidata = spi.xfer2([1,(8+channel)<<4,0]) 
            return ((spidata[1] & 3) << 8) + spidata[2]
 

    MCP.init()
    i=1
    
    
    channel_pot = MCP.read_channel(i) #waarde van CH0 lezen en opslaan in channel_pot
    voltage =  channel_pot * 0.00322266
    print("Waarde pot = {}v".format(voltage))
    i=i+1
    if voltage < 0.1:
        waarde = 2.5
    elif voltage >0.1 and voltage <1.65:
        waarde = 4
    elif voltage >1.5 and voltage <1.7:
        waarde = 6
    elif voltage >1.65 and voltage <3.2:
        waarde = 8
    elif voltage > 3.2:
        waarde = 11
    
    return waarde
waarde=FSR()
print(waarde)
def functionUS():
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start =time.time()
        
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()

    pulse_duration= pulse_end - pulse_start

    distance = pulse_duration *17150

    distance = round(distance,2)

    print(f"Afstand={distance} CM")

    return distance
def refresh():
    while True:

        temperatuur=temperatuur_functie()#Sensor 1
        glas_detectie=functionUS()#Sensor 2
        waarde_fsr=FSR()#Sensor 3
        #print(temperatuur)
        #print(afstand)
        datum=datetime.datetime.now()
        datum_correct=datum.strftime("%Y-%m-%d %H:%M:%S")
        print(datum_correct)
        DataRepository.create_new_row(datum_correct,waarde_fsr,1,None,3)
        DataRepository.create_new_row(datum_correct,temperatuur,1,None,2)
        DataRepository.create_new_row(datum_correct,glas_detectie,1,None,1)
        
        print(f"Waarde gewichtsensor ={waarde_fsr}")
        socketio.emit('B2F_status_update',{'FSR':waarde_fsr,'TS':temperatuur,'US':glas_detectie})    
        time.sleep(60)  

threading.Timer(5, refresh).start()

        



                





#API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@socketio.on('connect')
def initial_connection():
    Grafiek1=DataRepository.read_id_actuator(1)
    Grafiek2=DataRepository.read_id_actuator(2)
    Grafiek3=DataRepository.read_id_actuator(3)
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    #temperatuur=temperatuur_functie()
    #waarde_US=functionUS()
    #datum=datetime.datetime.now()
    #waarde=FSR()
    #datum_correct=datum.strftime("%Y-%m-%d %H:%M:%S")
    #print(waarde)
    socketio.emit('B2F_status_update',{'sensorId':Grafiek1,'sensorId2':Grafiek2, 'sensorId3':Grafiek3})

@socketio.on('F2B_passoa')
def produceer_cocktail():
    datum=datetime.datetime.now()
    datum_correct=datum.strftime("%Y-%m-%d %H:%M:%S")
    lcd.lcd_clear()
    lcd.lcd_display_string("Passoa wordt gemaakt", 1)
    DataRepository.create_new_row(datum_correct,None,1,4,None)
    DataRepository.create_new_row(datum_correct,None,1,1,None)
    # waarde_US=functionUS()
    # waarde= FSR()
    # #print(waarde)
    # #print(waarde_US)
    # if waarde_US<8 and waarde<12:
    #     motor(21,26)#FRUITSAP + PASSOA
    # else:
    #     GPIO.output(buzzer,2)
    #     time.sleep(1)
    #     GPIO.output(buzzer,0)
    DataRepository.create_new_row(datum_correct,None,0,4,None)
    DataRepository.create_new_row(datum_correct,None,0,1,None)
    lcd.lcd_clear()
    lcd.lcd_display_string("Passoa is klaar", 1)
    time.sleep(5)
    lcd.lcd_clear()

@socketio.on('F2B_pisang')
def produceer_cocktail():
    datum=datetime.datetime.now()
    datum_correct=datum.strftime("%Y-%m-%d %H:%M:%S")
    DataRepository.create_new_row(datum_correct,None,1,3,None)
    DataRepository.create_new_row(datum_correct,None,1,1,None)
    lcd.lcd_clear()
    lcd.lcd_display_string("Pisang wordt gemaakt", 1)
    # waarde_US=functionUS()
    # waarde=FSR()
    # if waarde_US<8 and waarde<12:
    #     motor(21,13)#FRUITSAP + PISANG
    # else:
    #     GPIO.output(buzzer,2)
    #     time.sleep(1)
    #     GPIO.output(buzzer,0)
    lcd.lcd_clear()
    lcd.lcd_display_string("Pisang is klaar", 1)
    time.sleep(5)
    lcd.lcd_clear()
    DataRepository.create_new_row(datum_correct,None,0,3,None)
    DataRepository.create_new_row(datum_correct,None,0,1,None)

@socketio.on('F2B_safari')
def produceer_cocktail():
    datum=datetime.datetime.now()
    datum_correct=datum.strftime("%Y-%m-%d %H:%M:%S")
    lcd.lcd_clear()
    lcd.lcd_display_string("Safari wordt gemaakt", 1)
    DataRepository.create_new_row(datum_correct,None,1,2,None)
    DataRepository.create_new_row(datum_correct,None,1,1,None)

    # waarde_us=functionUS()
    # waarde=FSR()
    # if waarde_US<8 and waarde<12:
    #     motor(21,19)#FRUITSAP + SAFARI
    # else:
    #     GPIO.output(buzzer,2)
    #     time.sleep(1)
    #     GPIO.output(buzzer,0)
    lcd.lcd_clear()
    lcd.lcd_display_string("Safari is klaar", 1)
    time.sleep(5)
    lcd.lcd_clear()
    DataRepository.create_new_row(datum_correct,None,0,2,None)
    DataRepository.create_new_row(datum_correct,None,0,1,None)

@socketio.on('F2B_spoeling')
def reiniging():
    time.sleep(5)
    motor_reinigen(21,16,20,25)




if __name__ == '__main__':
   socketio.run(app, debug=False, host='0.0.0.0')
    