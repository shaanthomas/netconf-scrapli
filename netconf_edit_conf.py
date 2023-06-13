from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file



PATH = os.path.abspath('')
TEMPLATES = os.path.join(PATH, 'Templates')
DATA = os.path.join(PATH, 'DATA')
CFG = os.path.join(PATH, 'CFG')
csr = os.path.join(TEMPLATES, 'csr.j2')


nr = InitNornir(config_file="config.yaml")
#Create a function to make a template and send it to device
def config_device(task):
    #EIRGP Template task is to build template file, name=explanator
    #Template is eigrp_payload
    #Path is this directory
    eigrp_template = task.run(
        task=template_file,
        name='Building EIGRP CONFIG',
        template='eigrp.j2',
        path='./',
    )
    #Variable to create the template
    routing_output = eigrp_template.result
    #Task to send the config to the running config
    task.run(task=netconf_edit_config, target='running', config=routing_output)
result = nr.run(task=config_device)
print_result(result)
