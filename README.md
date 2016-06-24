# RPi-Temp-Humidity-Monitor
Raspberry-Pi driven temperature and humidity sensing via DHT22.

Short-URL: http://git.io/vRFkn

## Ordering Boards:
v1.1 Boards are orderable from OSHPark at the following links:

- [PiTempLoggerv1.1-PiSide](https://oshpark.com/shared_projects/A5WHpdao) @ $34.50 per 3 boards
- [PiTempLoggerv1.1-Sensor](https://oshpark.com/shared_projects/NIQoCTse) @ $12.00 per 3 boards

They have been prototyped on a local board-fab machine, and a first run is en-route to the JQI.

## Other needed parts:
For one sensor baord:
- 1 DHT22 [from Adafruit?](https://www.adafruit.com/product/385)
- 1 of the above PiTempLoggerv1.1-Sensor
- 1 of 1-10k 1206 SMT resistor (use a lower resistance, e.g. 1-2k, if your ethernet cable is over 15 feet)
- 1 of 100nf 1206 SMT capacitor
- 1 of ethernet jack (Man. Part No. 555164-1, TE/Amp, get from any distributor)
- 1 Ethernet cable to connect to RPi (whatever length you need)

Per pi:
- 1 of the above PiTempLoggerv1.1-PiSide
- 8 of ethernet jack (Man. Part No. 555164-1, TE/Amp, get from any distributor)
- 1 of 26-pin 2x13 header
- 1 ribbon cable, either:
  - 26 pin
  - 40 pin
  - "Downgrade" cable [from Adafruit](https://www.adafruit.com/products/1986) <-Could also be made yourself with ribbon or connector
- 1 ethernet cable for network access


## Installing on a Raspberry Pi
See instructions in `INSTALL.md`
