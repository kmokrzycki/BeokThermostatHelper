#!/usr/bin/python3
import broadlink 
import json
import time
from datetime import datetime, timezone
import sqlite3
from pathlib import Path

idleTime = 5

# set this variables
strHost = '192.168.0.90' #ip device
strMac = '78:0F:77:FA:85:8A' #mac device

db = sqlite3.connect( '/home/krzysiek/BeokPy/data/beok.db')

cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, action TEXT, desired_temp REAL, current_temp REAL, created_at DATE)
''')

db.commit()

# other stuff: 
strType = '0x4ead' #HYSEN THERMOSTAT TYPE

#convert mac string 
macbytes = bytearray.fromhex(strMac.replace(':',''))

#get the broadlink hysen device
device = broadlink.hysen((strHost,80),macbytes,strType)

# get auth for futher comunications 
device.auth()

now = datetime.utcnow()
# do wathever you want with data :) 
data = device.get_full_status()
# print(json.dumps(data, separators=(',', ':')))
print ("%s Power %d - Fire %d. Current temp: %f VS desired %f." % (now, data['power'], data['active'], data['room_temp'], data['thermostat_temp']))

if (data['power'] == 1):

    cursor.execute('''SELECT id, action, created_at FROM events WHERE created_at >= datetime('now', '-2 minutes')''')
    all_rows = cursor.fetchall()

    if (len(all_rows) == 0):
        if (data['active'] == 1 and data['room_temp'] >= data['thermostat_temp']):
            desiredTemp = data['thermostat_temp']
            print('We need to switch off')
            device.set_temp(desiredTemp - 1.5)
            time.sleep(15)
            device.set_temp(desiredTemp)
            cursor.execute('''INSERT INTO events(action, desired_temp, current_temp ,created_at) VALUES(?,?,?,?)''', ('OFF', data['thermostat_temp'] ,data['room_temp'],now))
            db.commit()

        elif (data['active'] == 0 and data['room_temp'] < data['thermostat_temp']):
            desiredTemp = data['thermostat_temp']
            print('We need to switch on')
            device.set_temp(desiredTemp + 1.5)
            time.sleep(15)
            device.set_temp(desiredTemp)
            cursor.execute('''INSERT INTO events(action, desired_temp, current_temp ,created_at) VALUES(?,?,?,?)''', ('ON', data['thermostat_temp'] ,data['room_temp'],now))
            db.commit()
        #else: 
            #print('No need to do anything current temp: %f desired %f.' % (data['room_temp'], data['thermostat_temp']))
    else:
        print('''There was action taken less than 2 minutes ago''')

