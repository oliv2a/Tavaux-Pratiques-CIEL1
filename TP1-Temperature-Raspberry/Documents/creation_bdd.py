#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

db = pymysql.connect(host="localhost",user="root",passwd="raspberry",db="bts_sn1")

cur = db.cursor()

cur.execute("DROP TABLE IF EXISTS mesures")
db.commit()

cur.execute("CREATE TABLE mesures (id int(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT,date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,temperature DECIMAL(3,1) NOT NULL,humidite DECIMAL(2,0) UNSIGNED NOT NULL)")
db.commit()

cur.close()