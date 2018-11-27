#!/usr/bin/env python
'''
Demo: Read the IP address and credentials, and configures syslog using Restconf
'''

import csv
import requests
import xmltodict, json

filnavn = input("Device fil navn (*.csv): " )
syslog_addresse = input ("Hvad er addresse på din ny syslog server? ")
svar = input ("Skal jeg slette dine gamle syslog? (Y/N) ")

with open(filnavn) as fh:
    Inventory_list = []
    csv_reader = csv.DictReader(fh, delimiter=',')
    for row in csv_reader:
        Inventory_list.append(row)

    if svar == "Y":
        index= 0
        while (index < len(Inventory_list)):
            url = "https://" + Inventory_list[index]["IP address"] + ":443/restconf/data/Cisco-IOS-XE-native:native/logging/host/"
            payload = '{"host": {"ipv4-host-list": [{"ipv4-host": "' + syslog_addresse + '"}]}}'
            headers = {'Content-Type': "application/yang-data+json"}
            r = requests.put(url,auth=(Inventory_list[index]["Username"], Inventory_list[index]["Password"]), headers=headers, data=payload, verify=False)
            if "204" in str(r):
                print ("Configuration succesful")
            else:
                print ("Something went wrong with the configuration: " + r.text + str(r))

            index+=1
    elif svar == "N":
        index= 0
        while (index < len(Inventory_list)):
            url = "https://" + Inventory_list[index]["IP address"] + ":443/restconf/data/Cisco-IOS-XE-native:native/logging/host"
            payload = {"host": {"ipv4-host-list": []}}
            headers = {'Content-Type': "application/yang-data+json"}
            r = requests.get(url, auth=(Inventory_list[index]["Username"], Inventory_list[index]["Password"]),headers=headers, verify=False)
            data = r.text
            syslog_list = xmltodict.parse(data)
            #print("TYPE: " + str(type(syslog_list["host"]["ipv4-host-list"])))
            #print ("SYSLOG_LIST: " + str(syslog_list))
            #print ("O: " + str(syslog_list["host"]["ipv4-host-list"]))
            #print ("Length: " + str(len(syslog_list["host"]["ipv4-host-list"])))
            if len(syslog_list["host"]["ipv4-host-list"]) == 1:
                payload["host"]["ipv4-host-list"].append({"ipv4-host": syslog_list["host"]["ipv4-host-list"]["ipv4-host"]})
                print ("INSIDE IF LEN == 1")
            elif len(syslog_list["host"]["ipv4-host-list"]) > 1:
                for syslog in syslog_list["host"]["ipv4-host-list"]:
                    #syslog = syslog_list["host"]["ipv4-host-list"]
                    print ("Loop_1: " + str(syslog_list["host"]["ipv4-host-list"]))
                    print ("In loop: " + str(syslog) + ", TYPE: " + str(type(syslog)))
                    payload["host"]["ipv4-host-list"].append({"ipv4-host": syslog["ipv4-host"]})
            payload["host"]["ipv4-host-list"].append({"ipv4-host": syslog_addresse})

            print ("PAYLOAD: " + str (payload))
            payload = json.dumps(payload)
            print ("PAYLOAD AS STRING: " + payload)
            r = requests.put(url,auth=('cisco', 'cisco123'), headers=headers, data=payload, verify=False)
            if "204" in str(r):
                print ("Configuration succesful")
            else:
                print ("Something went wrong with the configuration: " + r.text)
            print ("INDEX: " + str(index))
            index+=1

    else:
        print("Forkert svar")
