'''
// I dedicate all this code, all my work, to my wife, who will
// have to support me once it gets released into the public.
Author: Vreddhi Bhat
Contact: vbhat@akamai.com
'''

import json
from akamai.edgegrid import EdgeGridAuth
from cloudletApiWrapper import cloudlet
import argparse
import configparser
import requests


try:
    config = configparser.ConfigParser()
    config.read('config_BBY.txt')
    client_token = config['CREDENTIALS']['client_token']
    client_secret = config['CREDENTIALS']['client_secret']
    access_token = config['CREDENTIALS']['access_token']
    access_hostname = config['CREDENTIALS']['access_hostname']
    session = requests.Session()
    session.auth = EdgeGridAuth(
    			client_token = client_token,
    			client_secret = client_secret,
    			access_token = access_token
                )
except (NameError, AttributeError, KeyError):
    print("\nLooks like config/credentials are missing\n")
    exit()

parser = argparse.ArgumentParser()
parser.add_argument("-getGroups","--getGroups",help="Get all cloudlet Groups",action="store_true")
parser.add_argument("-getAllGroupIds","--getAllGroupIds",help="Get all cloudlet Group Ids",action="store_true")
parser.add_argument("-listAllCloudlets","--listAllCloudlets",help="Get all cloudlet Group Ids",action="store_true")


args = parser.parse_args()


if not args.getGroups and not args.getAllGroupIds and not args.listAllCloudlets:
    print("\nUse -h to know the options to run program\n")
    exit()


if args.getGroups:
    cloudletObject = cloudlet(access_hostname)
    cloudletGroupResponse = cloudletObject.listCloudletGroups(session)
    print(cloudletGroupResponse)


if args.getAllGroupIds:
    cloudletObject = cloudlet(access_hostname)
    cloudletGroupIds = cloudletObject.getAllGroupIds(session)
    print(cloudletGroupIds)

if args.listAllCloudlets:
    cloudletObject = cloudlet(access_hostname)
    cloudletList = cloudletObject.listAllCloudlets(session)
    print(json.dumps(cloudletList))
