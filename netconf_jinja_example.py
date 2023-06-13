from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config, send_configs
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
import os




PATH = os.path.abspath('')
TEMPLATES = os.path.join(PATH, 'Templates')
DATA = os.path.join(PATH, 'DATA')
CFG = os.path.join(PATH, 'CFG')
csr = os.path.join(TEMPLATES, 'payload.j2')


nr = InitNornir(config_file="config.yaml")
#Create a function to make a template and send it to device

def load_vars(task):
    data = task.run(task=load_yaml, file = f"./host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
    config_device(task)

def config_device(task):
    #Build Template 
    template = task.run(task=template_file, name='Building Config', template='payload.j2', path=TEMPLATES)
    #Variable to create the template
    rendered = template.result
    #Send the  generated config to the running config of the device
    task.run(task=netconf_edit_config, target='running', config=rendered)


cmds = ['interface g2', 'no shutdown']

# target=nr.filter(alias='csr1')
result = nr.run(task=load_vars)
print_result(result)

result = nr.run(task=send_configs, configs=cmds)
print_result(result)

# import ipdb
# ipdb.set_trace()
