# BeokThermostatHelper

I created this scrpt as as was annoyed how BeOk BOT-313W Thermostat and similar models are handling temperature.

It only has accuracy down to ±0.5℃. What it means in practice is:

When yuo set temperature to be: 20℃ it will tunr itself on only when room temperature drops to 19℃ and keep heating on until it is 21℃. With where in my house were it reaches 21℃ making temperature diference 2℃ between on and off, even more radiators are still hot when it reachins 21℃ so it will effectively now heat up to 22℃.

This script limits will turn heating on when it is 19.5℃ and turn heating off when it is 20℃ (even with hot radiators it should it never exceeds 21℃)

## How it works
Once you have your thermostat ON and set temperature is less than require it will add 1.5℃ to current desired for 10 seconds only.
This will trigger heating to turn ON and wait until it reaches desired temperature and turn it OFF.

There is a delay to prevent flicking switch ON/OFF too often so script waits for 2 minutes before it will switch ON to OFF or otherwise.

## Compatibility (should work with)
* BeOk BOT-313W
* Floureon Smart WiFi Thermostat
* Beca WiFi Thermostat

## Configuration

Before you can run the script you need to configure the thermostat ip + mac in main file `beokThermostat.py`

```
# set this variables
strHost = '192.168.1.100' #thermostat ip
strMac = 'AA:BB:CC:DD:EE:FF' #thermostat mac address
```

## Running script
I use cron to run this script every minute.
```
* * * * * /home/user/BeokThermostatHelper/beokThermostat.py
```

you can run it manually with

```
python beokThermostat.py
```

## Resource
I came up with idea for this script after seeing this post:
https://hackaday.io/project/162466-beok-bot-313w-thermostat-hack#
