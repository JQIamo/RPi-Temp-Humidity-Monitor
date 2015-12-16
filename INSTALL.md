# Installing the Scripts on Raspberry Pi #

You should have already compiled and installed the temperature sensor reading library.

You'll also need to execute most off these commands using `sudo`.

## Setup Configuration Information ##
Copy the default configuration file to the expected place, then copy it to setup our settings:

    mkdir -p /etc/templogger/
	cp templogger.conf.defaults /etc/templogger/templogger.conf.defaults
    cp /etc/templogger/templogger.conf.defaults /etc/templogger/templogger.conf

Now you'll want to edit `/etc/templogger/templogger.conf` to whichever values you'll be using.  Comments in that file (or `/etc/templogger/templogger.conf.defaults`) explain the options.

When you're finished, make sure the permissions are set to safe values.  We store passwords in the .conf, so we only want it to be readable by a user with sufficient permissions:

    chown root:root /etc/templogger/templogger.conf*
    chmod 711 /etc/templogger/templogger.conf*

## Install Dependencies

### Python-dev and Pip ###
We'll use `pip` to handle some other dependencies.  If you don't have it, or need to upgrade:

    sudo apt-get install python-pip python-dev build-essential
    sudo apt-get install --upgrade pip python-dev

### Adafruit\_Python\_DHT ###
We'll want to compile on the Raspberry Pi. We can do that in memory to speed that process up, so here's the recommended method:

1. Clone the Adafruit repository somewhere on disk:
 
    `git clone https://github.com/adafruit/Adafruit_Python_DHT.git`

2. Copy it into the shared memory space:

    `cp -r Adafruit_Python_DHT/ /dev/shm/`

3. Compile and install.

    `cd /dev/shm/Adafruit_Python_DHT`

    `sudo python setup.py install`

4. _(Optional)_ Copy compiled objects back to where you got them

    `sudo cp -r . <path_to_cloned_repository>`

5. Clean up _(Optional, will be erased at next restart)_

    `rm -rf /dev/shm/Adafruit_Python_DHT`

### InfluxDB Python Client ###

Pip should find and install dependencies for us, so you should only need to run:

    pip install influxdb
	pip upgrade influxdb

## Test Function ##

Before we install them in a repeating fashion, you should test that everything is working.  Manually run the script (will require sudo)

    ./readInfluxTemp.py

## Move Scripts ##
The nuts and bolts is handled in two script, one of which requires a little manual configuration

First, copy the scripts to their final locations and set permissions:

    cp readInfluxTemp.py /usr/local/sbin/readInfluxTemp.py
	chown root:root /usr/local/sbin/readInfluxTemp.py
	chmod 711 /usr/local/sbin/readInfluxTemp.py
    
    cp uploadMissedTemps /etc/cron.hourly/
	chown root:root /etc/cron.hourly/uploadMissedTemps
	chmod 711 /etc/cron.hourly/uploadMissedTemps

Next, setup the cron entry to run `readInfluxTemp.py` every minute. Edit the file `/etc/crontab` and 
add these lines to the end:

    ## Do influx temp logging every minute
    */1 *	* * *	root	/usr/local/sbin/readInfluxTemp.py > /dev/null

## Verify It is Working ##

To check if it is working, we'll watch the system log for an entry saying it ran the cron job. (You shouldn't need `sudo` for this

    tail -n10 -f /var/log/syslog

You should have to wait no longer than a minute for a line like

    Dec 16 13:29:01 disorderedpi /USR/SBIN/CRON[17471]: (root) CMD (/usr/local/sbin/readInfluxTemp.py > /dev/null)

to appear.  If it does, check the database you're writing to for the new points.