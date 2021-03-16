#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, abort
from ..models import network, sensors
from . import api_tools


class AllSensorsCSV(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        user = api_tools.challenge_token(args['token'])
        net = user.networkList
        if(net == None):
            abort(404, message="Networks not found.")
       
        query = "SELECT * FROM sensors WHERE id_network = {}".format(net[0])
        
        for n in net[1:]:
            query += " OR id_network = {}".format(n)
        
        
        return api_tools.download_file(query)  
    
class GetSensorsByNetworkCSV(Resource):
    def get(self, netname):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        user = api_tools.challenge_token(args['token'])
        net = network.query.filter_by(name=netname).first()
        if(net != None):
            if net.id_network in user.networkList:
                query = "SELECT * FROM sensors WHERE id_network = {}".format(net.id_network)
                return api_tools.download_file(query)  
            else:
                abort(403, message="Access denied")   
        else:
             abort(404, message="Network not found")           
            
            
class GetParamByNetworkCSV(Resource):
    def get(self, netname):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        user = api_tools.challenge_token(args['token'])
        net = network.query.filter_by(name=netname).first()
        if(net != None):
            if net.id_network in user.networkList:
                sensorsList = sensors.query.filter_by(id_network=net.id_network).all()
                
                query = """SELECT * FROM "sensors_param" WHERE id_sensor = {}""".format(sensorsList[0].id_sensor)
                
                for n in sensorsList[1:]:
                    query += " OR id_sensor = {}".format(n.id_sensor)
            
                return api_tools.download_file(query)  
            else:
                abort(403, message="Access denied")   
        else:
            abort(404, message="Network not found")