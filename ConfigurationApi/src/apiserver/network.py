from flask_restful import Resource
from flask import request, Response
import json
import traceback
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class NetworkAPI(Resource):
    def __init__(self, **kwargs):
        pass

    def get(self):
        resp = {"error": False, "message": None, "data": None}
        status = 200
        try:

            result = []
            subprocess.run(["sudo iw wlan0 scan | egrep 'SSID|signal' > wifilist.txt"],
                           shell=True, stdout=subprocess.PIPE)
            fileName = "/home/opttime/gespline-services/api/wifilist.txt"
            wifiFile = open(fileName, "r")
            wifiFile.readlines
            for line in wifiFile.readlines():
                line = line.replace('\t', '')
                if line.find("SSID:") > -1:
                    temp = {}
                    lst = line.split(' ')
                    lst.remove('SSID:')
                    temp["SSID"] = " ".join(lst).replace('\n', '')
                    result.append(temp)
                # if line.startswith("\tpsk"):
                #     line = "ssid=" + '"' + ssid + '"'
            resp = result
            status = 200
        except Exception as e:
            logger.error(e)
            logger.error(type(e))
            logger.error(traceback.format_exc())
            status = 500
            resp["error"] = True
            resp["message"] = "Internal server error"
            # resp["message"] = "Internal server error"+str(e)
        return Response(json.dumps(resp), status=status, mimetype='application/json')

    def post(self, **kwargs):
        resp = {"error": False, "message": None, "data": {}}
        status = 200
        try:
            errMsg = self.validatePostData()
            if errMsg:
                resp["error"] = True
                resp["message"] = errMsg
                status = 400

            fileName = "/home/pi/API/wifilist.txt"
            fileObj = Path(fileName)
            
            wifi = self.BuildWifiConfig(
                ssid=request.json["ssid"], passwd=request.json["passwd"])
            subprocess.run(["sudo echo '" + wifi + "' >> /etc/wpa_supplicant/wpa_supplicant.conf"],
                           shell=True, stdout=subprocess.PIPE)
            if fileObj.exists():
                ArchivoError = open(fileName, "a")
                ArchivoError.write(wifi + "\n")
                ArchivoError.close()
        except Exception as e:
            logger.error(e)
            logger.error(type(e))
            logger.error(traceback.format_exc())
            status = 500
            resp["error"] = True
            resp["message"] = "Internal server error"
            # resp["message"] = "Internal server error"+str(e)
        return Response(json.dumps(resp), status=status, mimetype='application/json')

    def validatePostData(self):
        errMsg = None
        if not "ssid" in request.json:
            errMsg = "id required."
        elif not "passwd" in request.json:
            errMsg = "name required."
        return errMsg

    def _BuildWifiConfig(self, ssid, passwd):
        network = 'network={\n\tssid="' + ssid + \
            '"\n\tpsk="' + passwd + '"\n\tkey_mgmt=WPA-PSK\n}'
        logger.info(network)
        return '\nnetwork={\n\tssid="' + ssid + '"\n\tpsk="' + passwd + '"\n\tkey_mgmt=WPA-PSK\n}'
    
    def _isDuplicateNetworks(self, ssid):
        command = ['grep', '-n', '-c', ssid, 'file.txt']
        result = subprocess.call(command)
        return  result != 0
