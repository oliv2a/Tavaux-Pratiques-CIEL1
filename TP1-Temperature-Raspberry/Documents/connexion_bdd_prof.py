#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import time

temp = 20
hum = 50


db = pymysql.connect(host='localhost',
                             user='root',
                             password='ghost',
                             database='bts_sn1')

cur = db.cursor()

cur.execute("""INSERT INTO mesures(temperature, humidite) VALUES(%s,%s)""", (temp,hum,))
db.commit()
db.close()
