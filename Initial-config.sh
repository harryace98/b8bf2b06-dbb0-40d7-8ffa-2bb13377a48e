#!/bin/bash
# System Update
echo "Updating the system..."
sudo apt-get update
sudo apt-get upgrade -y

# Enable the ethernet module
 echo "Enable the ethernet module..."
 echo "dtoverlay=enc28j60" >> /boot/config.txt

 # Install modules
 echo "Installing the needed modules..."
 sudo apt-get install hostapd dnsmasq -y
 sudo apt-get install default-jdk -y
 sudo apt-get install python -y
 sudo apt-get install python3 -y
 sudo apt-get install python3-pip python3-dev python3-rpi.gpio python3-smbus -y
 sudo apt-get install i2c-tools -y

 #------------AP Mode-------------------

 # Creating the backups.
 echo "Creating the directories and files..."
 sudo mkdir /home/pi/Configurations
 sudo mkdir /home/pi/Configurations/AP


 sudo cp /etc/dhcpcd.conf /home/pi/Configurations/AP/dhcpcd.conf.orig
 sudo cp /etc/dnsmasq.conf /home/pi/Configurations/AP/dnsmasq.conf.orig
 sudo cp /etc/default/hostapd /home/pi/Configurations/AP/hostapd.orig

 # Create the directory tree for the capture application.
 sudo mkdir /home/pi/Configurations/Setting
 sudo mkdir /home/pi/LocalStorage/fileSended 
 # Create the needed files to run the capture application.
 sudo touch /home/pi/LocalStorage/accPulses.ctn
 sudo touch /home/pi/LocalStorage/fileSended/lstDelete.cln
 # Give the needed permissions
 sudo chown pi Configurations -R
 sudo chown pi LocalStorage -R

 # Configure dhcpcd
 sudo echo '
 interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant' >> /home/pi/Configurations/AP/dhcpcd.conf

# Configure dnsmasq
sudo echo '
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h' > /home/pi/Configurations/AP/dnsmasq.conf

# Configure hostapd.conf
sudo echo '
interface=wlan0
driver=nl80211
ssid=raspberry IoT
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=raspberry1234
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP' > /etc/hostapd/hostapd.config

# Configure hostapd
sudo echo '
# Defaults for hostapd initscript
#
# See /usr/share/doc/hostapd/README.Debian for information about alternative
# methods of managing hostapd.
#
# Uncomment and set DAEMON_CONF to the absolute path of a hostapd configuration
# file and hostapd will be started during system boot. An example configuration
# file can be found at /usr/share/doc/hostapd/examples/hostapd.conf.gz
#
DAEMON_CONF="/etc/hostapd/hostapd.conf"

# Additional daemon options to be appended to hostapd command:-
# 	-d   show more debug messages (-dd for even more)
# 	-K   include key data in debug messages
# 	-t   include timestamps in some debug messages
#
# Note that -B (daemon mode) and -P (pidfile) options are automatically
# configured by the init.d script and must not be added to DAEMON_OPTS.
#
#DAEMON_OPTS=""' > /home/pi/Configurations/AP/hostapd

sudo echo '
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6,1)
GPIO.output(27,1)
time.sleep(0.2)
GPIO.output(22,1)
time.sleep(0.2)
GPIO.output(23,1)
time.sleep(0.2)
GPIO.output(24,1)
time.sleep(0.2)
GPIO.output(16,1)
time.sleep(0.2)
GPIO.output(20,1)
time.sleep(0.2)
GPIO.output(21,1)
time.sleep(0.2)
GPIO.output(26,1)
time.sleep(0.2)
GPIO.output(19,1)
time.sleep(0.2)
GPIO.output(13,1)
time.sleep(0.2)
GPIO.output(27,0)
time.sleep(0.2)
GPIO.output(22,0)
time.sleep(0.2)
GPIO.output(23,0)
time.sleep(0.2)
GPIO.output(24,0)
time.sleep(0.2)
GPIO.output(16,0)
time.sleep(0.2)
GPIO.output(20,0)
time.sleep(0.2)
GPIO.output(21,0)
time.sleep(0.2)
GPIO.output(26,0)
time.sleep(0.2)
GPIO.output(19,0)
time.sleep(0.2)
GPIO.output(13,0)
time.sleep(0.2)' > /home/pi/Configurations/ledini.py

sudo echo '
#!/bin/bash
sudo cp /home/pi/Configurations/AP/dhcpcd.conf.orig /etc/dhcpcd.conf
sudo cp /home/pi/Configurations/AP/dnsmasq.conf.orig /etc/dnsmasq.conf
sudo cp /home/pi/Configurations/AP/hostapd.orig /etc/default/hostapd
sudo systemctl stop hostapd
sudo systemctl restart dhcpcd
sudo systemctl restart dnsmasq
sudo su
sudo ip link set dev wwan0 down
sudo echo Y > /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4,apn=<YOUR_APN>" --client-no-release-cid
sudo udhcpc -q -f -n -i wwan0
exit' > /home/pi/Configurations/normal.sh

sudo echo '
#!/bin/bash
sudo cp /home/pi/Configurations/AP/dhcpcd.conf /etc/dhcpcd.conf
sudo cp /home/pi/Configurations/AP/dnsmasq.conf /etc/dnsmasq.conf
sudo cp /home/pi/Configurations/AP/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp /home/pi/Configurations/AP/hostapd /etc/default/hostapd
sudo systemctl restart dhcpcd
sudo systemctl restart dnsmasq
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl restart hostapd
sudo su
sudo ip link set dev wwan0 down
sudo echo Y > /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4,apn=<YOUR_APN>" --client-no-release-cid
sudo udhcpc -q -f -n -i wwan0
exit' > /home/pi/Configurations/AP.sh

sudo echo '
#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.IN)

Status = GPIO.input(17)

if Status == 1:
        GPIO.output(27,1)
        os.system("sudo bash /home/pi/Configurations/AP.sh")
else:
        GPIO.output(27,0)
        os.system("sudo bash /home/pi/Configurations/normal.sh")' > /home/pi/Configurations/APmode.py


sudo echo '
#!/bin/bash
##Program to reestar the capture program.
sudo killall java&
sleep 10
_now=$(date +"%Y-%m-%dT%H:%M:%S") 
echo "Actual date:  " "$_now"
# Starting the Capture app.
cd /home/pi/
sudo java -jar com.proalnet.iot-0.0.1-jar-with-dependencies.jar > "consoleOutput-$_now.log" 2>&1 &
exit 0' > /home/pi/reboot.sh

 sudo echo '
 #!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

# init the RTC
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device

sudo python3 /home/pi/Configurations/ledini.py &

sleep 10

sudo python3 /home/pi/Configurations/APmode.py &

sleep 30
cd /home/pi
sudo bash reboot.sh &

exit 0' > /etc/rc.local

 #------------ Capture Application configuration -------------------
 echo "Updating and configurate de environment..."
 # Create directorty to save the app updates.
 sudo mkdir /home/pi/Configurations/githubRepository
 # Download the files for update the app.
 sudo curl https://raw.githubusercontent.com/harryace98/b8bf2b06-dbb0-40d7-8ffa-2bb13377a48e/main/UpdateLastVersionIoTCapture.sh > /home/pi/Configurations/githubRepository/UpdateLastVersionIoTCapture.sh
 sudo curl https://raw.githubusercontent.com/harryace98/b8bf2b06-dbb0-40d7-8ffa-2bb13377a48e/main/UpdateConfigFile.sh > /home/pi/Configurations/githubRepository/UpdateConfigFile.sh
 # update the program and the configurations
 sudo bash /home/pi/Configurations/githubRepository/UpdateLastVersionIoTCapture.sh
 sudo bash /home/pi/Configurations/githubRepository/UpdateConfigFile.sh
