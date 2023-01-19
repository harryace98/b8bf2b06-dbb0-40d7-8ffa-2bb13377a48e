
import RPi.GPIO as GPIO
import time
import os
import logging
from logging.handlers import RotatingFileHandler
from common import settings
from common import LedControl
from common import WatchDog
from pathlib import Path
import sys
import subprocess  # For executing a shell command
import traceback

logger = logging.getLogger(__name__)

# It's a class that runs a thread that checks the internet connection and blinks the LED's accordingly
class RunMode:
    def __init__(self, pin_PULSE_1:int, pin_PULSE_2, pin_PULSE_3, pin_PULSE_4, pin_OPERATION_MODE, pin_CATURE_APP,
                 pin_WIFI_STATUS, pin_SERVER_STATUS, pin_UNDEFINED_1, pin_UNDEFINED_2, debug) -> None:
        self.__PULSE_1 = pin_PULSE_1
        self.__PULSE_2 = pin_PULSE_2
        self.__PULSE_3 = pin_PULSE_3
        self.__PULSE_4 = pin_PULSE_4
        self.__OPERATION_MODE = pin_OPERATION_MODE
        self.__CATURE_APP = pin_CATURE_APP
        self.__WIFI_STATUS = pin_WIFI_STATUS
        self.__SERVER_STATUS = pin_SERVER_STATUS
        self.__UNDEFINED_1 = pin_UNDEFINED_1
        self.__UNDEFINED_2 = pin_UNDEFINED_2
        self.__DEBUG = debug
    """
    It's a function that runs a thread that checks the internet connection and blinks the LED's
    accordingly
    :return: None
    """
    def run(self):
        try:
            ## init variables
            __LED_OPERATION_MODE = LedControl.Led(self.__OPERATION_MODE, "__LED_OPERATION_MODE")
            __LED_CATURE_APP = LedControl.Led(self.__CATURE_APP, "__LED_CATURE_APP")
            __LED_WIFI_STATUS = LedControl.Led(self.__WIFI_STATUS, "__LED_WIFI_STATUS")
            __LED_SERVER_STATUS = LedControl.Led(self.__SERVER_STATUS, "__LED_SERVER_STATUS")
            __LED_UNDEFINED_1 = LedControl.Led(self.__UNDEFINED_1, "__LED_UNDEFINED_1")
            __LED_UNDEFINED_2 = LedControl.Led(self.__UNDEFINED_2, "__LED_UNDEFINED_2")
            __LED_OPERATION_MODE.on()
            __LED_WIFI_STATUS.blink(time_off=0.1667, time_on=0.1667)
            __LED_SERVER_STATUS.blink(time_off=0.1667, time_on=0.1667)
            logging.info("Start run mode. ")

            if not self.__DEBUG:
                # Change the files to start the run mode
                command = ['sudo', 'bash', '/home/pi/Configurations/normal.sh']
                commandResult = subprocess.call(command,
                                                stdout=subprocess.DEVNULL,
                                                stderr=subprocess.STDOUT) == 0 ## if the command result is equal to 0 has connection
                if not commandResult:
                    logging.error("Error trying to confifurate the normal mode.")

            # Checking the systems
            watchDog = WatchDog.ConnectionWatchDog(restartFileName=settings.RESTART_FILE_NAME, restartDateFormat=settings.RESTART_DATE_FORMAT,
                                                    urlTarget=settings.URL_TARGET, interfaceTarget=settings.INTERFACE_TARGET, timeToExec=settings.TIMETOEXEC)
            watchDog.start()
            while watchDog.isAlive():
                logger.info("Internet watchDog is Running.")
                time.sleep(15)
                connectionErrors = watchDog.getError()
                logger.info(connectionErrors)                
                if connectionErrors[0]: ## router connection status
                    __LED_WIFI_STATUS.blink(time_off=0.1667, time_on=0.1667)
                else:
                    __LED_WIFI_STATUS.stopBlink()
                    __LED_WIFI_STATUS.on()
                if connectionErrors[1]: ## server connection Status
                    __LED_SERVER_STATUS.blink(time_off=0.1667, time_on=0.1667)
                else:
                    __LED_SERVER_STATUS.stopBlink()
                    __LED_SERVER_STATUS.on()
                time.sleep(45)
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
                 pin_WIFI_STATUS, pin_SERVER_STATUS, pin_UNDEFINED_1, pin_UNDEFINED_2, debug) -> None:
        self.__PULSE_1 = pin_PULSE_1
        self.__PULSE_2 = pin_PULSE_2
        self.__PULSE_3 = pin_PULSE_3
        self.__PULSE_4 = pin_PULSE_4
        self.__OPERATION_MODE = pin_OPERATION_MODE
        self.__CATURE_APP = pin_CATURE_APP
        self.__WIFI_STATUS = pin_WIFI_STATUS
        self.__SERVER_STATUS = pin_SERVER_STATUS
        self.__UNDEFINED_1 = pin_UNDEFINED_1
        self.__UNDEFINED_2 = pin_UNDEFINED_2
        self.__DEBUG = debug

    def run(self):
        try:
            __LED_OPERATION_MODE = LedControl.Led(self.__OPERATION_MODE, "__LED_OPERATION_MODE")
            __LED_CATURE_APP = LedControl.Led(self.__CATURE_APP, "__LED_CATURE_APP")
            __LED_WIFI_STATUS = LedControl.Led(self.__WIFI_STATUS, "__LED_WIFI_STATUS")
            __LED_SERVER_STATUS = LedControl.Led(self.__SERVER_STATUS, "__LED_SERVER_STATUS")
            __LED_UNDEFINED_1 = LedControl.Led(self.__UNDEFINED_1, "__LED_UNDEFINED_1")
            __LED_UNDEFINED_2 = LedControl.Led(self.__UNDEFINED_2, "__LED_UNDEFINED_2")

            __LED_OPERATION_MODE.blink(time_off=0.1667, time_on=0.1667)
            __LED_CATURE_APP.blink(time_off=0.1667, time_on=0.1667)
            __LED_WIFI_STATUS.blink(time_off=0.1667, time_on=0.1667)
            __LED_SERVER_STATUS.blink(time_off=0.1667, time_on=0.1667)
            __LED_UNDEFINED_1.blink(time_off=0.1667, time_on=0.1667)
            __LED_UNDEFINED_2.blink(time_off=0.1667, time_on=0.1667)

            if not self.__DEBUG:
                command = ['sudo', 'bash', '/home/pi/Configurations/AP.sh']
                commandResult = subprocess.call(command,
                                                stdout=subprocess.DEVNULL,
                                                stderr=subprocess.STDOUT) == 0 ## if the command result is equal to 0 has connection
                if not commandResult:
                    logging.error("Error trying to confifurate the normal mode.")
            while (True):
                logging.info("Configuration Mode are enable.")
                time.sleep(7200)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("Error During Configuration mode.")
            return None
