#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os
import logging
from logging.handlers import RotatingFileHandler
from common import settings
from common import LedControl
from common import OperationModes
from pathlib import Path
import sys
import traceback

PIN_PULSE_1 = 27
PIN_PULSE_2 = 22
PIN_PULSE_3 = 23
PIN_PULSE_4 = 24
PIN_OPERATION_MODE = 16
PIN_CATURE_APP = 20
PIN_WIFI_STATUS = 21
PIN_SERVER_STATUS = 26
PIN_UNDEFINED_1 = 19
PIN_UNDEFINED_2 = 13
PIN_SWITCH_MODE = 17
DEBUG = False

logger = logging.getLogger()
GPIO.setmode(GPIO.BCM)

def start_logger():
    logformatter = logging.Formatter(settings.LOG_FORMAT)

    # print "Log format ",logformatter
    # print "Log level ",LOG_LEVEL
    filepath = Path(settings.LOG_FILE)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    logger.setLevel(settings.DEFAULT_LEVELS[settings.FILE_LOG_LEVEL])
    fh = RotatingFileHandler(
        settings.LOG_FILE, maxBytes=(1048576*5), backupCount=7)
    fh.setFormatter(logformatter)
    logger.addHandler(fh)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logging.Formatter(settings.CONSOLE_LOG_FORMAT))
    consoleHandler.setLevel(
        settings.DEFAULT_LEVELS[settings.CONSOLE_LOG_LEVEL])
    logger.addHandler(consoleHandler)

    # logging.basicConfig(filename=self.log_file_path,format=logformatter,level=settings.DEFAULT_LEVELS[LOG_LEVEL])

    logger.info("Program started")


def StartApp():
    try:
        start_logger()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("MyApp : unable to enable logger")

    try:
        GPIO.setup(PIN_SWITCH_MODE, GPIO.IN)
        operationMode = GPIO.input(17)

        if operationMode == 1:
            return OperationModes.ConfigurationMode(pin_PULSE_1=PIN_PULSE_1, pin_PULSE_2=PIN_PULSE_2,
                                          pin_PULSE_3=PIN_PULSE_3, pin_PULSE_4=PIN_PULSE_4,
                                          pin_OPERATION_MODE=PIN_OPERATION_MODE, pin_CATURE_APP=PIN_CATURE_APP,
                                          pin_WIFI_STATUS=PIN_WIFI_STATUS, pin_SERVER_STATUS=PIN_SERVER_STATUS,
                                          pin_UNDEFINED_1=PIN_UNDEFINED_1, pin_UNDEFINED_2=PIN_UNDEFINED_2, 
                                          debug=DEBUG)
        else:
            return OperationModes.RunMode(pin_PULSE_1=PIN_PULSE_1, pin_PULSE_2=PIN_PULSE_2,
                                          pin_PULSE_3=PIN_PULSE_3, pin_PULSE_4=PIN_PULSE_4,
                                          pin_OPERATION_MODE=PIN_OPERATION_MODE, pin_CATURE_APP=PIN_CATURE_APP,
                                          pin_WIFI_STATUS=PIN_WIFI_STATUS, pin_SERVER_STATUS=PIN_SERVER_STATUS,
                                          pin_UNDEFINED_1=PIN_UNDEFINED_1, pin_UNDEFINED_2=PIN_UNDEFINED_2, 
                                          debug=DEBUG)

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
        logger.error("Unable to start Initial Program")
        return None

try:
    if __name__ == '__main__':
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(PIN_PULSE_1, GPIO.OUT)
        # GPIO.setup(PIN_PULSE_2, GPIO.OUT)
        # GPIO.setup(PIN_PULSE_3, GPIO.OUT)
        # GPIO.setup(PIN_PULSE_4, GPIO.OUT)

        # GPIO.output(PIN_PULSE_1, 1)
        # GPIO.output(PIN_PULSE_2, 1)
        # GPIO.output(PIN_PULSE_3, 1)
        # GPIO.output(PIN_PULSE_4, 1)
        
        # time.sleep(3)
        my_app = StartApp()
        if my_app:
            if(len(sys.argv) > 2) and sys.argv[1]=="--mode" and sys.argv[2].upper() == "DEBUG":
                DEBUG = True
                logger.warn("*******    DEBUG MODE {}    ********".format(DEBUG))
            logger.info("Running Initial Program")
            my_app.run()
        else:
            logger.error("Error starting Initial Program")
        exit(1)
    else:
        gunicorn_app = StartApp()
except KeyboardInterrupt as e:
    print("Stopped by user. KeyboardInterrupt")
    GPIO.cleanup()
except Exception as e:
    print("Stopped by Eror.")
    logger.error(e)
    logger.error(traceback.format_exc())
    GPIO.cleanup()
