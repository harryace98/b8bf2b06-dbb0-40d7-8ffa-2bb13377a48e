from flask_restful import Resource
from flask import request, Response
import json
import traceback
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigAPI(Resource):
    def __init__(self, **kwargs):
        pass

    def get(self):
        resp = {"error": False, "message": None, "data": None}
        status = 200
        try:
            result = []
            ## put the logic here
            
            ##
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
            ## put the logic here
            ##
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

    def BuildWifiConfig(self, ssid, passwd):
        network = 'network={\n\tssid="' + ssid + \
            '"\n\tpsk="' + passwd + '"\n\tkey_mgmt=WPA-PSK\n}'
        logger.info(network)
        return '\nnetwork={\n\tssid="' + ssid + '"\n\tpsk="' + passwd + '"\n\tkey_mgmt=WPA-PSK\n}'
