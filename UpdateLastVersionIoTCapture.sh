#!/bin/bash

printf "Starting the update process..."
sleep 1
#Getting the actual date and setting the name of the log file.
_now=$(date +"%Y-%m-%dT%H:%M:%S") 
echo "Actual date:  " "$_now"
sudo mkdir /home/pi/githubRepository
# Moving into the directory to make the upatade.
cd /home/pi/githubRepository/
# Getting the most recent version of teh Iot capture code.
sudo wget https://github.com/harryace98/b8bf2b06-dbb0-40d7-8ffa-2bb13377a48e/raw/main/com.proalnet.iot-0.0.1-jar-with-dependencies.jar -O com.proalnet.iot-0.0.1-jar-with-dependencies.jar
# Saving the previus version in a backUp
sudo mv /home/pi/com.proalnet.iot-0.0.1-jar-with-dependencies.jar /home/pi/com.proalnet.iot-0.0.1-jar-with-dependencies.jar.bk
# Copy the file into the workspace directory.
sudo cp com.proalnet.iot-0.0.1-jar-with-dependencies.jar /home/pi/com.proalnet.iot-0.0.1-jar-with-dependencies.jar
sudo chown pi:pi /home/pi/com.proalnet.iot-0.0.1-jar-with-dependencies.jar
# Kill the java process for reset the app.
printf "Killing the actual IoT Capture Process... "
sudo killall java 
sleep 5
# Starting the Capture app.
cd /home/pi/
sudo java -jar com.proalnet.iot-0.0.1-jar-with-dependencies.jar > "consoleOutput-$_now.log" 2>&1 &
