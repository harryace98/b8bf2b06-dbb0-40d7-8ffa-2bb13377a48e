#!/bin/bash
printf "Starting the update process..."
sleep 1
# Getting the actual date and setting the name of the log file.
_now=$(date +"%Y-%m-%dT%H:%M:%S")
echo "Actual date:  " "$_now"
# Moving into the directory to make the upatade.
cd /home/pi/Configurations/Setting/
# Saving the previus configurations in a backUp
sudo mv config.json config.json.bk
# Getting the most recent version of the configurations file.
printf "Downloading the current version of the configuration file..."
curl https://raw.githubusercontent.com/harryace98/b8bf2b06-dbb0-40d7-8ffa-2bb13377a48e/main/config.json > config.json
# Giving the correct file permission 
sudo chown pi:pi /home/pi/Configurations/Setting/config.json
# Kill the java process for reset the app.
printf "Killing the actual IoT Capture Process... "
sudo killall java 
sleep 5
# Starting the Capture app.
printf "Starting the capture App "
cd /home/pi/
sudo java -jar com.proalnet.iot-0.0.1-jar-with-dependencies.jar > "consoleOutput-$_now.log" 2>&1 &
