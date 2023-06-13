#! usr/bin/python3

from nornir_scrapli.tasks import netconf_get_config, netconf_get
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
from xml.dom import minidom


#This tutorial is designed to remind me how to use yang models
#Step 1. Configure the device for whatever you are trying to use the yang model to program
#   ex. Configure the router for eigrp
#Step 2. Use nornir/scapli to perform a netconf_get using an xpath filter on /native element
#   Cisco stores all of its config in one roote element called /native
#Step 3. Look for your changes in the yang/XML result
#   In this example we would find the <router-eigrp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp"> portion of the xml
#Step 4. Modify filter in script to isolate the eigrp section
#   In this example we would use 

# <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
#   <data>
#     <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
#       <router>
#         <router-eigrp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp">
#           <eigrp>
#             <classic-mode>
#               <autonomous-system>100</autonomous-system>
#               <eigrp>
#                 <router-id>1.1.1.1</router-id>
#               </eigrp>
#               <network>
#                 <address-wildcard>
#                   <ipv4-address>10.1.1.1</ipv4-address>
#                   <wildcard>0.0.0.0</wildcard>
#                 </address-wildcard>
#               </network>
#             </classic-mode>
#           </eigrp>
#         </router-eigrp>
#       </router>
#     </native>
#   </data>


#Step 5 Take everything in the data section 
#   Amend the xml document so that you can use it as a payload
#   Change data to config 
#   Add the key words  operation - replace to the router section 
#   <config >
#     <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
#       <router operation = "replace">
#         <router-eigrp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp">
#           <eigrp>
#             <classic-mode>
#               <autonomous-system>100</autonomous-system>
#               <eigrp>
#                 <router-id>1.1.1.1</router-id>
#               </eigrp>
#               <network>
#                 <address-wildcard>
#                   <ipv4-address>12.1.1.1</ipv4-address>
#                   <wildcard>0.0.0.255</wildcard>
#                 </address-wildcard>
#               </network>
#             </classic-mode>
#           </eigrp>
#         </router-eigrp>
#       </router>
#     </native>
#   </config>

#Step 6. Use the config-tester to deploy config
filter1 = '''
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
</interfaces>
'''
filter2 =  '''
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
      </name>
      <type/>
      <link-up-down-trap-enable/>
    </interface>
</interfaces>
'''

filter3 = """
 <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
      <description/>
      <type/>
      <link-up-down-trap-enable/>
    </interface>
  </interfaces>
"""
filter4 = """
  <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
  </interfaces>
  """
filter5= """
  <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
    <interface>
      <name/>GigabitEthernet1</name>
    <interface/>
  </interfaces>
  """


nr = InitNornir(config_file="config.yaml")
#This will provide the equivalent of a show run. The result will be in a yang xml format
#Task.run lets you run a task within a task
#Using the xpath filter type and the '/native' filter will pull the whole show run file from the device in yang xml
#https://www.w3schools.com/xml/xpath_syntax.asp

#This method uses the get_config method. Ca
def get_config(task):
    #The task below uses a sub tree filter
    # result = task.run(task=netconf_get_config, source='running', filter_type='subtree', filter_=filter5)
    result = task.run(task=netconf_get, filter_= '/native/router', filter_type='xpath')
    #You can skip all the bull by just typing in filter and // to ge to tag that you want..its like a wildcard
    #result = task.run(task=netconf_get, filter_= '//router-ospf', filter_type='xpath')
#This method uses the net_conf get
#Notice that the filters are different
def get_info(task):
     #The task below uses a sub tree filter
    result = task.run(task=netconf_get, filter_type='subtree', filter_=filter4)
    #result = task.run(task=netconf_get, filter_= '/native/router', filter_type='xpath')

target = nr.filter(alias='csr1')
result = target.run(task=get_config)
# result = target.run(task=get_info)
print_result(result)

