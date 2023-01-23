#!/usr/bin/env python3

import http.client as httplib
import threading
import socket
import struct
import os
import sys
import time
from datetime import datetime
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import traceback
import logging

logger = logging.getLogger(__name__)


class ConnectionWatchDog():
    def __init__(self, restartFileName="restarts.csv", restartDateFormat="%d/%m/%Y %H:%M:%S",
                 urlTarget="a39g730csmjomc-ats.iot.us-east-1.amazonaws.com", interfaceTarget="eth0", timeToExec=1800, timeToRestart=28800) -> None:
        self.__RESTART_FILE_NAME = restartFileName
        self.__RESTART_DATE_FORMAT = restartDateFormat
        self.__URL_TARGET = urlTarget
        self.__INTERFACE_TARGET = interfaceTarget
        self.__TIMETOEXEC = timeToExec
        self.__TIMETORESTART = timeToRestart
        self.stoppedFlag = threading.Event()
        # [0]: no connection to router via wifi # [1]: no connection to router via Ethernet
        # [2]: no connection to OpttimeServer # 
        #self.__hasConnectionErrorFlags = [False, False, False]
        self.__isWifiConnected = False
        self.__isEthernetConnected = False
        self.__isOpttimeServerConnected = False
        self.__hasConnection = False
        self.__isAlive = False
        self.__thread = None
        self.__firstLoopFlag = True

    def getStatus(self):
        return self.__hasConnection
        
    def getWifiStatus(self):
        return self.__isWifiConnected

    def getEthernetStatus(self):
        return self.__isEthernetConnected

    def getOpttimeServerStatus(self):
        return self.__isOpttimeServerConnected
        
    def getConnectionsStatus(self):
        return [self.__isEthernetConnected, self.__isWifiConnected, self.__isOpttimeServerConnected]
    def isAlive(self):
        self.__isAlive = self.__thread.is_alive()
        return self.__isAlive

    def getDefaultGateway(self):
        getaway = []
        """Read the default gateway directly from /proc."""
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    # If not default route or not RTF_GATEWAY, skip it
                    continue
                getaway.append(
                    {
                        "interface": fields[0],
                        "gateway": socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
                    })
            return getaway

    def __getLastRestart(self):
        try:
            f = open(self.__RESTART_FILE_NAME)
            lines = f.read().splitlines()
            last_line = lines[-1]
            return datetime.strptime(last_line, self.__RESTART_DATE_FORMAT)
        except Exception:
            return datetime.min
        finally:
            try:
                f.close()
            except:
                pass

    def __putRestartTimespan(self):
        with open(self.__RESTART_FILE_NAME, 'a') as f:
            f.write("\n" + datetime.now().strftime(self.__RESTART_DATE_FORMAT))
            f.close()

    # def __haveInternetByHTTP(self):
    #     return False
    #     # conn = httplib.HTTPConnection(self.__URL_TARGET, timeout=5)
    #     # try:
    #     #     conn.request("HEAD", "/")
    #     #     conn.close()
    #     #     return True
    #     # except:
    #     #     conn.close()
    #     #     logger.error("HTTP Connection Failed")
    #     #     return False

    def __isServerConnectedByPING(self):
        try:
            # Option for the number of packets as a function of
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            # Building the command. Ex: "ping -c 1 google.com"
            command = ['ping', param, '1', self.__URL_TARGET]
            commandResult = subprocess.call(command,
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.STDOUT) == 0  # if the command result is equal to 0 has connection
            self.__isOpttimeServerConnected = commandResult
            return commandResult
        except:
            return False

    def __RestartInterface(self):
        os.system("sudo ifdown --force " + self.__INTERFACE_TARGET)
        time.sleep(3)
        os.system("sudo ifup " + self.__INTERFACE_TARGET)

    def __RestartNetworkService(self):
        os.system("sudo service networking restart")
        time.sleep(3)
        os.system("sudo systemctl daemon-reload")
    def __RestartDevice(self):
        os.system("sudo reboot now")

    def __doWork(self):
        if self.__firstLoopFlag:
            self.__putRestartTimespan()
            self.__hasConnection = True
            self.__firstLoopFlag = False
        
        logger.info("Start Checkers to verify the connection.")
        # if self.__haveInternetByHTTP():
        #     logger.info("Internet working. HTTP check OK")
        # else:
        if self.__isServerConnectedByPING():  # we check if we have connection with the Opttime Server doing ping
            logger.info("Internet is working. PING check OK")
            self.__hasConnection = True
        else:
            self.__hasConnection = False
            logger.warn("Internet is not working. Ping no response.")

        if self.isRouterConected():
            self.__hasConnection = False
            logger.warn("Connection with the router is not Working.")

        lastRestartFromNow = (datetime.now() - self.__getLastRestart())
        if lastRestartFromNow.total_seconds() > self.__TIMETORESTART:
            logger.info("The Device will be Restarted")
            self.__RestartDevice()
        if self.__hasConnection:
            self.__putRestartTimespan()

    def isRouterConected(self):
        gateway = self.getDefaultGateway()
        logger.info(gateway)
        result = False
        temp = []
        self.__isEthernetConnected = False
        self.__isWifiConnected = False
        for Interface in gateway:
            # Option for the number of packets as a function of
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            # Building the command. Ex: "ping -c 1 google.com"
            command = ['ping', param, '1', Interface["gateway"],
                       '-I', Interface["interface"]]
            commandResult = subprocess.call(command,
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.STDOUT) == 0  # if the command result is equal to 0 has connection
            temp.append({
                "interface": Interface["interface"], "response": commandResult
            })
            if Interface["interface"] == "eth0":
                self.__isEthernetConnected = commandResult
            elif Interface["interface"] == "wlan0":
                self.__isWifiConnected = commandResult
            else:
                self.__isEthernetConnected = False
                self.__isWifiConnected = False
            result |= commandResult
        logger.info(temp)
        return result

    def __run(self, stopFlag, timeToWait):
        logger.info("start the wifi wd." + str(stopFlag.is_set()))
        while not stopFlag.is_set():
            try:
                logger.info("Starting Internet watchdog Proccess...")
                self.__doWork()
                time.sleep(timeToWait)
            except KeyboardInterrupt as e:
                sys.exit("Programa Finalizado" + str(e))
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                continue

    def start(self):
        try:
            self.stoppedFlag.clear()
            self.__thread = threading.Thread(
                name='Connection_WatchDog', target=self.__run, args=(self.stoppedFlag, self.__TIMETOEXEC))
            # start the thread
            self.__thread.start()
        except Exception as e:
            logger.error(
                "Error trying to start the Connection_WatchDog process.")
            logger.error(e)
            logger.error(traceback.format_exc())
            return None

    def reset(self):
        try:
            # set the semaphore so the thread will exit after sleep has completed
            self.stoppedFlag.set()
            # wait for the thread to exit
            self.__thread.join()
            logger.info("The Connection_WatchDog process was stopped.")
        except Exception as e:
            logger.error(
                "Error trying to stop the Connection_WatchDog process")
            logger.error(e)
            logger.error(traceback.format_exc())
            return None
