'''
// I dedicate all this code, all my work, to my wife, who will
// have to support me once it gets released into the public.
Author: Vreddhi Bhat
Contact: vbhat@akamai.com
'''

import json


class cloudlet(object):
    def __init__(self,access_hostname):
        self.access_hostname = access_hostname

    def listCloudletGroups(self,session):
        """
        Function to fetch all groups

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        cloudletGroupRespose : cloudletGroupRespose
            (cloudletGroupRespose) Object with all details
        """
        cloudletGroupUrl = 'https://' + self.access_hostname + '/cloudlets/api/v2/group-info'
        cloudletGroupRespose = session.get(cloudletGroupUrl)
        return cloudletGroupRespose

    def getAllGroupIds(self,session):
        """
        Function to fetch all groupIDs only

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        groupIdList : List
            groupIdList with list of all groupIds
        """
        cloudletGroupUrl = 'https://' + self.access_hostname + '/cloudlets/api/v2/group-info'
        cloudletGroupResponse = session.get(cloudletGroupUrl)
        groupIdList = []
        if cloudletGroupResponse.status_code == 200:
            for everyItem in cloudletGroupResponse.json():
                groupIdList.append(everyItem['groupId'])
        return groupIdList

    def listAllCloudlets(self,session):
        """
        Function to fetch all cloudlets

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        cloudletList : List
            cloudletList with list of all cloudlets
        """
        groupIdList = self.getAllGroupIds(session)
        cloudletList = []
        for everyGroupId in groupIdList:
            listAllCloudletsUrl = 'https://' + self.access_hostname + '/cloudlets/api/v2/cloudlet-info?gid=' + str(everyGroupId)
            print('Fetching cloudlet for Group: ' + str(everyGroupId))
            listAllCloudletsResponse = session.get(listAllCloudletsUrl)
            if listAllCloudletsResponse.status_code == 200:
                cloudletList.append(listAllCloudletsResponse.json())
                print(json.dumps(listAllCloudletsResponse.json()))
                print('Added cloudlet info for Group: ' + str(everyGroupId) + ' to a list\n')
            else:
                print('Group: ' + str(everyGroupId) + ' did not yield any cloudlets\n')
        return cloudletList

    def listPolicies(self,session,groupId,cloudletId='optional',cloudletCode='optional'):
        """
        Function to fetch Policies from cloudletId and GroupId

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        policiesResponse : policiesResponse
            Policies of cloudlet Id
        """
        if cloudletCode == 'optional':
            policiesUrl = 'https://' + self.access_hostname + '/cloudlets/api/v2/policies?gid=' + str(groupId) + '&includeDeleted=false&cloudletId=' + str(cloudletId)
            policiesResponse = session.get(policiesUrl)
        elif cloudletCode == 'VP':
            policiesUrl = 'https://' + self.access_hostname + '/cloudlets/api/v2/policies?gid=' + str(groupId) + '&includeDeleted=false&cloudletId=' + str(1)
            policiesResponse = session.get(policiesUrl)
        return policiesResponse

    def getCloudletPolicy(self,session,policyId):
        """
        Function to fetch a cloudelt policy detail

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        cloudletPolicyResponse : cloudletPolicyResponse
            Json object details of specific cloudlet policy
        """
        cloudletPolicyUrl = 'https://' + self.access_hostname + '/cloudlets/api/v2/policies/'+ str(policyId)
        cloudletPolicyResponse = session.get(cloudletPolicyUrl)
        return cloudletPolicyResponse
