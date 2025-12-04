#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysqldb
import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# TCN75A address, 0x48(72)
# Select configuration register, 0x01(01)
#		0x60(96)	12-bit ADC resolution
bus.write_byte_data(0x48, 0x01, 0x60)

# TCN75A address, 0x48(72)
# Read data back from 0x00(00), 2 bytes
# temp MSB, temp LSB
data = bus.read_i2c_block_data(0x48, 0x00, 2)

# Convert the data to 12-bits
temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
if temp > 2047 :
  temp -= 4096
cTemp = round(temp  * 0.0625,0)
print ("Temperature in Celsius : %.2f C" %cTemp)
print (cTemp)

db = pymysql.connect(host='localhost',
                             user='root',
                             password='raspberry',
                             database='Temperature')

cur = db.cursor()
cur.execute("""INSERT INTO mesures(temperature) VALUES(%s)""", (cTemp,))
db.commit()
db.close()
