
import RPi.GPIO as GPIO
import time
import os
import logging
from logging.handlers import RotatingFileHandler
from common import settings
from common import LedControl
from common import WatchDog
from pathlib import Path
import subprocess  # For executing a shell command
import traceback
import socket

logger = logging.getLogger(__name__)

# It's a class that runs a thread that checks the internet connection and blinks the LED's accordingly


class RunMode:
    def __init__(self, pin_PULSE_1: int, pin_PULSE_2, pin_PULSE_3, pin_PULSE_4, pin_OPERATION_MODE, pin_CATURE_APP,
                 pin_ETHERNET_STATUS, pin_WIFI_STATUS, pin_SERVER_STATUS, pin_UNDEFINED_2,timeToRestart, debug=False) -> None:
        self.__PULSE_1 = pin_PULSE_1
        self.__PULSE_2 = pin_PULSE_2
        self.__PULSE_3 = pin_PULSE_3
        self.__PULSE_4 = pin_PULSE_4
        self.__OPERATION_MODE = pin_OPERATION_MODE
        self.__CATURE_APP = pin_CATURE_APP
        self.__ETHERNET_STATUS = pin_ETHERNET_STATUS
        self.__WIFI_STATUS = pin_WIFI_STATUS
        self.__SERVER_STATUS = pin_SERVER_STATUS
        self.__UNDEFINED_2 = pin_UNDEFINED_2
        self.__DEBUG = debug 
        self.__TIMETORESTART =  300 if debug else timeToRestart
        self.__CurrentDir = os.getcwd()
    """
    It's a function that runs a thread that checks the internet connection and blinks the LED's
    accordingly
    :return: None
    """

    def run(self):
        try:
            # init variables
            __LED_OPERATION_MODE = LedControl.Led(
                self.__OPERATION_MODE, "__LED_OPERATION_MODE")
            # __LED_CATURE_APP = LedControl.Led(
            #     self.__CATURE_APP, "__LED_CATURE_APP")
            __LED_ETHERNET_STATUS = LedControl.Led(
                self.__ETHERNET_STATUS, "__LED_ETHERNET_STATUS")
            __LED_WIFI_STATUS = LedControl.Led(
                self.__WIFI_STATUS, "__LED_WIFI_STATUS")
            __LED_SERVER_STATUS = LedControl.Led(
                 self.__SERVER_STATUS, "__LED_SERVER_STATUS")
            # __LED_UNDEFINED_2 = LedControl.Led(
            #     self.__UNDEFINED_2, "__LED_UNDEFINED_2")
            __LED_OPERATION_MODE.on()
            time.sleep(0.5)
            __LED_ETHERNET_STATUS.on(time_off=0.1667, time_on=0.1667)
            time.sleep(0.5)
            __LED_WIFI_STATUS.on(time_off=0.1667, time_on=0.1667)
            time.sleep(0.5)
            __LED_SERVER_STATUS.on(time_off=0.1667, time_on=0.1667)

            logging.info("Start run mode. ")
            count = 1
            if not self.__DEBUG:
                try:
                    # Change the files to start the run mode
                    command = ['sudo', 'bash',
                               '/home/pi/Configurations/normal.sh']
                    commandResult = subprocess.call(command,
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.STDOUT
                                                    ) == 0  # if the command result is equal to 0 has connection
                except Exception as e:
                    logger.error("Error command.")
                    logger.error(e)
                    logger.error(traceback.format_exc())

                if not commandResult:
                    logging.error(
                        "Error trying to confifurate the normal mode.")

            # Checking the systems
            watchDog = WatchDog.ConnectionWatchDog(restartFileName=settings.RESTART_FILE_NAME, restartDateFormat=settings.RESTART_DATE_FORMAT,
                                                   urlTarget=settings.URL_TARGET, interfaceTarget=settings.INTERFACE_TARGET, timeToExec=settings.TIMETOEXEC, timeToRestart=self.__TIMETORESTART)
            watchDog.start()

            while watchDog.isAlive():
                logger.info("Internet watchDog is Running.")
                time.sleep(15)
                logger.info(watchDog.getConnectionsStatus)
                if not watchDog.getEthernetStatus():  # router connection status via ethernet
                    __LED_ETHERNET_STATUS.blink(time_off=0.1667, time_on=0.1667)
                else:
                    __LED_ETHERNET_STATUS.stopBlink()
                    __LED_ETHERNET_STATUS.on()

                if not watchDog.getWifiStatus():  # router connection status via wifi
                    __LED_WIFI_STATUS.blink(time_off=0.1667, time_on=0.1667)
                else:
                    __LED_WIFI_STATUS.stopBlink()
                    __LED_WIFI_STATUS.on()

                if not watchDog.getOpttimeServerStatus():  # server connection Status
                    __LED_SERVER_STATUS.blink(time_off=0.1667, time_on=0.1667)
                else:
                    __LED_SERVER_STATUS.stopBlink()
                    __LED_SERVER_STATUS.on()
                time.sleep(15)
            else:
                logger.info("Internet watchDog stopped.")

                # GPIO.output(27,0)
                # os.system("sudo bash /home/pi/Configurations/normal.sh")
            logger.warn("Proccess stopped unexpected.")
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("Error During Run mode.")


class ConfigurationMode:
    def __init__(self, pin_PULSE_1, pin_PULSE_2, pin_PULSE_3, pin_PULSE_4, pin_OPERATION_MODE, pin_CATURE_APP,
                 pin_ETHERNET_STATUS, pin_WIFI_STATUS, pin_SERVER_STATUS, pin_UNDEFINED_2, debug) -> None:
        self.__PULSE_1 = pin_PULSE_1
        self.__PULSE_2 = pin_PULSE_2
        self.__PULSE_3 = pin_PULSE_3
        self.__PULSE_4 = pin_PULSE_4
        self.__OPERATION_MODE = pin_OPERATION_MODE
        self.__CATURE_APP = pin_CATURE_APP
        self.__ETHERNET_STATUS = pin_ETHERNET_STATUS
        self.__WIFI_STATUS = pin_WIFI_STATUS
        self.__SERVER_STATUS = pin_SERVER_STATUS
        self.__UNDEFINED_2 = pin_UNDEFINED_2
        self.__DEBUG = debug
        self.__CurrentDir = os.getcwd()

    def run(self):
        try:
            # __LED_OPERATION_MODE = LedControl.Led(
            #     self.__OPERATION_MODE, "__LED_OPERATION_MODE")
            # __LED_CATURE_APP = LedControl.Led(
            #     self.__CATURE_APP, "__LED_CATURE_APP")
            # __LED_WIFI_STATUS = LedControl.Led(
            #     self.__ETHERNET_STATUS, "__LED_WIFI_STATUS")
            # __LED_SERVER_STATUS = LedControl.Led(
            #     self.__WIFI_STATUS, "__LED_SERVER_STATUS")
            # __LED_SERVER_STATUS = LedControl.Led(
            #     self.__SERVER_STATUS, "__LED_SERVER_STATUS")
            # __LED_UNDEFINED_2 = LedControl.Led(
            #     self.__UNDEFINED_2, "__LED_UNDEFINED_2")

            # __LED_OPERATION_MODE.blink(time_off=0.1667, time_on=0.1667)
            # __LED_CATURE_APP.blink(time_off=0.1667, time_on=0.1667)
            # __LED_WIFI_STATUS.blink(time_off=0.1667, time_on=0.1667)
            # __LED_SERVER_STATUS.blink(time_off=0.1667, time_on=0.1667)
            # __LED_SERVER_STATUS.blink(time_off=0.1667, time_on=0.1667)
            # __LED_UNDEFINED_2.blink(time_off=0.1667, time_on=0.1667)

            GPIO.setup(self.__OPERATION_MODE, GPIO.OUT)
            GPIO.setup(self.__CATURE_APP, GPIO.OUT)
            GPIO.setup(self.__ETHERNET_STATUS, GPIO.OUT)
            GPIO.setup(self.__WIFI_STATUS, GPIO.OUT)
            GPIO.setup(self.__SERVER_STATUS, GPIO.OUT)
            GPIO.setup(self.__UNDEFINED_2, GPIO.OUT)

            # update ap config
            self._SetWifiNamePassword()
            logger.info(self.__CurrentDir)
            if not self.__DEBUG:
                try:
                    command = ['sudo', 'bash',
                               '/home/pi/Configurations/AP.sh']
                    commandResult = subprocess.run(command,
                                                   stdout=subprocess.DEVNULL,
                                                   stderr=subprocess.STDOUT
                                                   ) == 0  # if the command result is equal to 0 has connection
                    if not commandResult:
                        logging.error(
                            "Error trying to confifurate the Configuration mode.")
                except Exception as e:
                    logger.error("Error command.")
                    logger.error(e)
                    logger.error(traceback.format_exc())
            logging.info("Configuration Mode are enable.")
            while (True):
                GPIO.output(self.__OPERATION_MODE, GPIO.HIGH)
                GPIO.output(self.__CATURE_APP, GPIO.HIGH)
                GPIO.output(self.__ETHERNET_STATUS, GPIO.HIGH)
                GPIO.output(self.__WIFI_STATUS, GPIO.HIGH)
                GPIO.output(self.__SERVER_STATUS, GPIO.HIGH)
                GPIO.output(self.__UNDEFINED_2, GPIO.HIGH)
                time.sleep(0.1667)
                GPIO.output(self.__OPERATION_MODE, GPIO.LOW)
                GPIO.output(self.__CATURE_APP, GPIO.LOW)
                GPIO.output(self.__ETHERNET_STATUS, GPIO.LOW)
                GPIO.output(self.__WIFI_STATUS, GPIO.LOW)
                GPIO.output(self.__SERVER_STATUS, GPIO.LOW)
                GPIO.output(self.__UNDEFINED_2, GPIO.LOW)
                time.sleep(0.1667)
        except Exception as e:
            logger.error("Error During Configuration mode.")
            logger.error(e)
            logger.error(traceback.format_exc())
            return None

    def _SetWifiNamePassword(self):
        hostName = socket.gethostname()
        config_lines = [
            'interface=wlan0',
            'driver=nl80211',
            'ssid={}_Config'.format(hostName),
            'hw_mode=g',
            'channel=7',
            'wmm_enabled=0',
            'macaddr_acl=0',
            'auth_algs=1',
            'ignore_broadcast_ssid=0',
            'wpa=2',
            'wpa_passphrase={}'.format(hostName),
            'wpa_key_mgmt=WPA-PSK',
            'wpa_pairwise=TKIP',
            'rsn_pairwise=CCMP'
        ]
        logger.info(config_lines)
        config = '\n'.join(config_lines)
        # writing to file
        with open("/home/pi/Configurations/AP/hostapd.conf", "w") as wifi:
            wifi.write(config)