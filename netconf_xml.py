#! usr/bin/python3

from nornir_scrapli.tasks import netconf_get_config, netconf_get
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
import xmltodict
from pprint import pprint







nr = InitNornir(config_file="config.yaml")
#This will provide the equivalent of a show run. The result will be in a yang xml format
#Task.run lets you run a task within a task
#Using the xpath filter type and the '/native' filter will pull the whole show run file from the device in yang xml
#https://www.w3schools.com/xml/xpath_syntax.asp

#This method uses the get_config method. Ca
def get_config(task):
  #Filter data
    filter = task.run(task=netconf_get, filter_= '/native/interface//Loopback[name=33]', filter_type='xpath')
    #Save results in a variable
    output = filter.result
    #Change data to ordered dictionary
    dict_result = xmltodict.parse(output)
    #Create a nornir variable called facts for every host
    task.host['facts'] = dict_result
    loopback33 = task.host["facts"]["rpc-reply"]["data"]["native"]["interface"]["Loopback"]['name']
    l33_address = task.host['facts']['rpc-reply']['data']['native']['interface']['Loopback']['ip']['address']['primary']['address']
    mask = task.host['facts']['rpc-reply']['data']['native']['interface']['Loopback']['ip']['address']['primary']['mask']
    print(loopback33)
    print(f'Loopback{loopback33} has an address of {l33_address} and a mask of ')

def get_info(task):
  result = task.run(task=netconf_get, filter_= '/native/interface', filter_type='xpath')

target = nr.filter(alias='csr1')
results = target.run(task=get_config)
# print_result(results)

# result = target.run(task=get_info)
# print_result(result)

#IPDB lets us access the python debugger
# import ipdb
# ipdb.set_trace()
