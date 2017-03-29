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
parser.add_argument("-listAllPolicies","--listAllPolicies",help="List all cloudlet policies",action="store_true")
parser.add_argument("-getVPPolicyDetails","--getVPPolicyDetails",help="List all VP cloudlet policies",action="store_true")
parser.add_argument("-listPolicyVersions","--listPolicyVersions",help="List all versions of cloudlet policy")



args = parser.parse_args()


if not args.getGroups and not args.getAllGroupIds and not args.listAllCloudlets and not args.listAllPolicies and not args.getVPPolicyDetails \
and not args.listPolicyVersions:
    print("\nUse -h to know the options to run program\n")
    exit()


if args.getGroups:
    cloudletObject = cloudlet(access_hostname)
    cloudletGroupResponse = cloudletObject.listCloudletGroups(session)
    #print(json.dumps(cloudletGroupResponse.json()))
    count = 1
    for everyGroup in cloudletGroupResponse.json():
        print(str(count) + '. ' + 'Name: ' + everyGroup['groupName'] + ' ID: ' + str(everyGroup['groupId']))
        count += 1



if args.getAllGroupIds:
    cloudletObject = cloudlet(access_hostname)
    cloudletGroupIds = cloudletObject.getAllGroupIds(session)
    print(cloudletGroupIds)

if args.listAllCloudlets:
    cloudletObject = cloudlet(access_hostname)
    cloudletList = cloudletObject.listAllCloudlets(session)
    print(json.dumps(cloudletList))

if args.listAllPolicies:
    cloudletObject = cloudlet(access_hostname)
    print('Fetching all cloudlet Groups..')
    cloudletGroupResponse = cloudletObject.listCloudletGroups(session)
    print('Fetching policies for each group..')
    for everyGroup in cloudletGroupResponse.json():
        for everyCloudletGroup in everyGroup['capabilities']:
            cloudletId = everyCloudletGroup['cloudletId']
            groupId = everyGroup['groupId']
            cloudletPolicies = cloudletObject.listPolicies(session, groupId, cloudletId)
            if cloudletPolicies.status_code == 200:
                print('\nPolicy details for cloudletId: ' + str(cloudletId) + ' and groupId: ' + str(groupId) + ' is below:')
                print(json.dumps(cloudletPolicies.json()))
            else:
                print('\ncloudletId: ' + str(cloudletId) + ' and groupId: ' + str(groupId) + ' did not get any policy details')

if args.getVPPolicyDetails:
    cloudletObject = cloudlet(access_hostname)
    print('Fetching all cloudlet Groups..')
    cloudletGroupResponse = cloudletObject.listCloudletGroups(session)
    print('Fetching policies for each group..')
    for everyGroup in cloudletGroupResponse.json():
        groupId = everyGroup['groupId']
        cloudletPolicies = cloudletObject.listPolicies(session=session, groupId=groupId, cloudletCode='VP')
        if cloudletPolicies.status_code == 200:
            print('\nPolicy details are groupId: ' + str(groupId) )
            if 'vp_stage_www' in json.dumps(cloudletPolicies.json()):
                break
        else:
            print('groupId: ' + str(groupId) + ' has no VP Policies')
    for everyCloudletGroupInformation in cloudletPolicies.json():
        if everyCloudletGroupInformation['name'] == 'vp_stage_www':
            cloudletJsonInfo = everyCloudletGroupInformation
            print(json.dumps(cloudletJsonInfo))
    policyDetails = cloudletObject.getCloudletPolicy(session, cloudletJsonInfo['policyId'])
    print('\n\npolicyDetails: ' + json.dumps(policyDetails.json()))

if args.listPolicyVersions:
    policyName = args.listPolicyVersions
    cloudletObject = cloudlet(access_hostname)
    print('Fetching all cloudlet Groups..')
    cloudletGroupResponse = cloudletObject.listCloudletGroups(session)
    print('Fetching policies for each group..')
    for everyGroup in cloudletGroupResponse.json():
        groupId = everyGroup['groupId']
        cloudletPolicies = cloudletObject.listPolicies(session=session, groupId=groupId, cloudletCode='VP')
        if cloudletPolicies.status_code == 200:
            if policyName in json.dumps(cloudletPolicies.json()):
                break
        else:
            print('groupId: ' + str(groupId) + ' has no VP Policies')
    for everyCloudletGroupInformation in cloudletPolicies.json():
        if everyCloudletGroupInformation['name'] == policyName:
            print('Found the policy ' + policyName + '...\n')
            cloudletJsonInfo = everyCloudletGroupInformation
    policyVersionsDetails = cloudletObject.listPolicyVersions(session, cloudletJsonInfo['policyId'])
    #print('\n\npolicyDetails: ' + json.dumps(policyVersionsDetails.json()))
    if policyVersionsDetails.status_code == 200:
        for everyVersion in policyVersionsDetails.json():
            print('\nVersion: ' + str(everyVersion['version']))
            print('Created By: ' + everyVersion['createdBy'])
            print('Description: ' + everyVersion['description'])
            if 'matchRules' in everyVersion and everyVersion['matchRules'] is not None:
                for everyVersionsMatchRule in everyVersion['matchRules']:
                    if 'disabled' not in everyVersionsMatchRule:
                        print('Rule Name: ' + everyVersionsMatchRule['name'] + '   Percentage: ' + str(everyVersionsMatchRule['passThroughPercent']))







print('*************DONE************')
