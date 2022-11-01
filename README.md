## Home Assistant EnergyZero tariff import
![EnergyZero](https://uploads-ssl.webflow.com/5fa5035d490fb94e2bd11ed6/600809fb7c0e552d50ce7abf_logo.svg)
<br><img src="https://design.home-assistant.io/images/logo.png" width="300" title="Home Assistant">

EnergyZero is a dutch energy supplier (https://www.energyzero.nl).
I wrote this script to scrape their API for tariff information on gas and electricity.
The data is then send to Home Assistant via MQTT. So having a Home Assistant and MQTT
up and running is a requirement.

This script is distributed as docker container so that it's easy to use for me and ready
for other to use.

Follow these steps to get the container up and running:

  1. Pull this repo:
     git clone git@github.com:fzwart/energyzero2ha.git
 
  2. Build the container:
     cd <clone directory>
     ./build.sh
 
  3. Set configuration options:
     cp config.yaml.example config.yaml
     vi config.yaml

  4. Run the container:
     docker-compose up -d
