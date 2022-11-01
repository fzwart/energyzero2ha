#!/usr/bin/python3

# EnergyZero script for fetching Electricity and Gas tariff information
# and send it to Home Assistant via MQTT.

import paho.mqtt.client as mqtt
import requests, datetime, yaml

with open("config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Config file Read successful")

mqttc = mqtt.Client(client_id="EnergyZero Scraper", clean_session=False)
mqttc.username_pw_set(config['mqtt_user'], password=config['mqtt_password'])

mqttc.connect(config['mqtt_host'], port=config['mqtt_port'], keepalive=60)

electricityEntity="""
  {
   "device": {
     "name"         : "EnergyZero",
     "identifiers"  : "EnergyZero",
     "manufacturer" : "Black Technologies"
   },
   "name"                : "EnergyZero Electricity Tariff",
   "unique_id"           : "EnergyZero Electricity Tariff",
   "state_topic"         : "homeassistant/sensor/energyzero_electricity_tariff/state",
   "command_topic"       : "homeassistant/sensor/energyzero_electricity_tariff/command",
   "unit_of_measurement" : "EUR/kWh"
  }"""

gasEntity="""
  {
   "device": {
     "name"         : "EnergyZero",
     "identifiers"  : "EnergyZero",
     "manufacturer" : "Black Technologies"
   },
   "name"                : "EnergyZero Gas Tariff",
   "unique_id"           : "EnergyZero Gas Tariff",
   "state_topic"         : "homeassistant/sensor/energyzero_gas_tariff/state",
   "command_topic"       : "homeassistant/sensor/energyzero_gas_tariff/command",
   "unit_of_measurement" : "EUR/m3"
  }"""

mqttc.publish(config['discovery_prefix']+"/sensor/energyzero_electricity_tariff/config", payload=electricityEntity)
mqttc.publish(config['discovery_prefix']+"/sensor/energyzero_gas_tariff/config", payload=gasEntity)

now = datetime.datetime.utcnow()
hour = str(now.hour)
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# known usageTypes for url: 1(electricity), 4(gas)

# Electricity
url = "https://api.energyzero.nl/v1/energyprices?fromDate="+str(now.date())+"T"+hour+"%3A00%3A00.000Z&tillDate="+str(now.date())+"T"+hour+"%3A59%3A59.999Z&interval=4&usageType=1&inclBtw=true"
r = requests.get(url)
tariff=r.json()['Prices'][0]['price']
print(dt_string + " Electricity tariff: "+str(tariff))
mqttc.publish(config['discovery_prefix']+"/sensor/energyzero_electricity_tariff/state", payload=tariff, retain=True)

# Gas
url = "https://api.energyzero.nl/v1/energyprices?fromDate="+str(now.date())+"T"+hour+"%3A00%3A00.000Z&tillDate="+str(now.date())+"T"+hour+"%3A59%3A59.999Z&interval=4&usageType=4&inclBtw=true"
r = requests.get(url)
tariff=r.json()['Prices'][0]['price']
print(dt_string + " Gas tariff: "+str(tariff))
mqttc.publish(config['discovery_prefix']+"/sensor/energyzero_gas_tariff/state", payload=tariff, retain=True)
