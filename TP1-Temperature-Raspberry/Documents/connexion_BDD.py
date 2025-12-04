#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysqldb
import time

temp = 20
hum = 50
lum = 500

db = pymysql.connect(host='localhost',
                             user='root',
                             password='pi',
                             database='bts_sn_1')

cur = db.cursor()

cur.execute("""INSERT INTO mesures(temperature, humidite, luminosite) VALUES(%s,%s,%s)""", (temp,hum, lum,))
db.commit()
db.close()
