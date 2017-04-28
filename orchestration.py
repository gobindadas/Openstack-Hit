#Author: Gobinda Das
#This class will accept yaml object and call heat api to orchestrate openstack resources.

from keystoneauth1 import loading
from keystoneauth1 import session
from heatclient import client
import os
import base64

class Ochestration:
    # Call heat api to create stack using heat template
    def orchestrateResource(self, yamlFile):
        loader = loading.get_plugin_loader('password');

        # Read crudentials from environment variable.
        auth_url = os.environ.get("authentication_url");
        username = os.environ.get("userName");
        password = base64.b64decode(os.environ.get("password"));
        project_id = os.environ.get("project_id");
        user_domain_name = os.environ.get("user_domain_name");

        auth = loader.load_from_options(auth_url=auth_url, username=username, password=password,
                                        project_id=project_id, user_domain_name=user_domain_name);
        sess = session.Session(auth=auth);
        heat = client.Client('1', session=sess);
        with open(yamlFile, 'r') as loadedFile:
            data = loadedFile.read();
        heat.stacks.create(stack_name='ericsson_demo', template=data);
        print("Heat api called to create resources,Please check dashboard.");