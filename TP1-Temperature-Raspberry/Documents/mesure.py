#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import time
from datetime import datetime
from time import strftime
import gy_30
import smbus
import sys
#import smbus2 as smbus#,smbus2
import adafruit_sgp30
#sensor_3 = adafruit_sgp30.Adafruit_SGP30(i2c)
#sensor_3.iaq_init()
#sensor_3.set_iaq_baseline(0x8973, 0x8AAE)
sensor_1 = gy_30.GY_30()

# Conversion pour trame de reception
def ConvertToDecimal(entree):
	converted = ((entree[0]-48)*100+(entree[1]-48)*10+(entree[2]-48))
	return converted


# Slave Addresses
I2C_SLAVE_ADDRESS = 11 #0x0b ou 11

h = datetime.now()
date_time = h.strftime("%Y-%m-%d %H:%M:%S")
print(date_time)


bus = smbus.SMBus(1) # Rev 2 Pi uses 1
config = [0x08, 0x00]
bus.write_i2c_block_data(0x38, 0xE1, config)
time.sleep(0.5)
byt = bus.read_byte(0x38)
#print(byt&0x68)
MeasureCmd = [0x33, 0x00]
bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
time.sleep(0.5)
data = bus.read_i2c_block_data(0x38,0x00, 0x6)
temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
ctemp = ((temp*200) / 1048576) - 50
print(u'Temperature: {0:.1f}°C'.format(ctemp))
tmp = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
ctmp = int(tmp * 100 / 1048576)
print(u'Humidity: {0}%'.format(ctmp))

valeur_LR = int(round(sensor_1.getLight()))
print(valeur_LR)

MeasureCmd = [0x, 0x00]
bus.write_i2c_block_data(I2C_SLAVE_ADDRESS, 0x00, MeasureCmd)
time.sleep(0.5)
data=bus.read_i2c_block_data(I2C_SLAVE_ADDRESS,0x00,21)
print("receive from slave:")
print(data)
Vent_moyen = ConvertToDecimal(data[6:9])
print ("Vitesse moyenne :",Vent_moyen," km/h")
Vent_mini = ConvertToDecimal(data[9:12])
print ("Vitesse mini :",Vent_mini," km/h")
Vent_max = ConvertToDecimal(data[12:15])
print ("Vitesse max :",Vent_max," km/h")
Dir_moyen = ConvertToDecimal(data[15:18])
print ("Direction moyenne :",Dir_moyen," °")
Dir_inst = ConvertToDecimal(data[18:21])
print ("Direction instantanée :",Dir_inst," °")

db = pymysql.connect(host='localhost',
                             user='root',
                             password='ghost',
                             database='Projet_2021')

cur = db.cursor()

cur.execute("""INSERT INTO Valeurs_a_transmettre(date,speed_avg,speed_min,speed_max,dir_avg,dir_inst,hygro,temperature,lum) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (date_time,Vent_moyen,Vent_mini,Vent_max,Dir_moyen,Dir_inst,ctmp,ctemp,valeur_LR,))
db.commit()
db.close()


