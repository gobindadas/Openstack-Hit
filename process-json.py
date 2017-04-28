#Author: Gobinda Das
#This class will read existing json and pick openstack related fields and create object.
#Create YAML object from new object and pass to orchestation module.

import json
import yaml
import orchestration

class ProcessJson:
    def process(self,jsonFile):
        jObj = {};
        with open(jsonFile,'r') as jsonData:
            data = json.load(jsonData)["vmDetails"];

            jObj["heat_template_version"] = "2015-04-30";
            jObj["description"] = "Create new network and add 2 subnet to the network,2 security groups,2 vms in each subnet with floatingIP,attach volume to wach vm";

            # Create key
            jObj["resources"] = {};
            jObj["resources"]["demo_key"] = {};
            jObj["resources"]["demo_key"]["type"] = "OS::Nova::KeyPair";
            jObj["resources"]["demo_key"]["properties"] = {};
            jObj["resources"]["demo_key"]["properties"]["name"] = data["demo_key"]["name"];

            # Create network
            jObj["resources"]["demo_net"] = {};
            jObj["resources"]["demo_net"]["type"] = "OS::Neutron::Net";
            jObj["resources"]["demo_net"]["properties"] = {};
            jObj["resources"]["demo_net"]["properties"]["name"] = data["demo_net"]["name"];
            jObj["resources"]["demo_net"]["properties"]["tenant_id"] = data["demo_net"]["tenant_id"];

            #Create router
            jObj["resources"]["demo_router"] = {};
            jObj["resources"]["demo_router"]["type"] = "OS::Neutron::Router";
            jObj["resources"]["demo_router"]["properties"] = {};
            jObj["resources"]["demo_router"]["properties"]["external_gateway_info"] = {};
            jObj["resources"]["demo_router"]["properties"]["external_gateway_info"]["network"] = data["demo_router"]["network"];

            # Create Subnet
            jObj["resources"]["demo_subnet"] = {};
            jObj["resources"]["demo_subnet"]["type"] = "OS::Neutron::Subnet";
            jObj["resources"]["demo_subnet"]["properties"] = {};
            jObj["resources"]["demo_subnet"]["properties"]["allocation_pools"] = [{}];
            jObj["resources"]["demo_subnet"]["properties"]["allocation_pools"][0]["end"] = data["demo_subnet"]["allocation_pools"][0]["end"];
            jObj["resources"]["demo_subnet"]["properties"]["allocation_pools"][0]["start"] = data["demo_subnet"]["allocation_pools"][0]["start"];
            jObj["resources"]["demo_subnet"]["properties"]["cidr"] = data["demo_subnet"]["cidr"];
            jObj["resources"]["demo_subnet"]["properties"]["gateway_ip"] = data["demo_subnet"]["gateway_ip"];
            jObj["resources"]["demo_subnet"]["properties"]["network_id"] = {};
            jObj["resources"]["demo_subnet"]["properties"]["network_id"]["get_resource"] = "demo_net";
            jObj["resources"]["demo_subnet"]["properties"]["tenant_id"] = data["demo_subnet"]["tenant_id"];

            # Create router interface
            jObj["resources"]["router_interface"] = {};
            jObj["resources"]["router_interface"]["type"] = "OS::Neutron::RouterInterface";
            jObj["resources"]["router_interface"]["properties"] = {};
            jObj["resources"]["router_interface"]["properties"]["router_id"] = {};
            jObj["resources"]["router_interface"]["properties"]["router_id"]["get_resource"] = "demo_router";
            jObj["resources"]["router_interface"]["properties"]["subnet_id"] = {};
            jObj["resources"]["router_interface"]["properties"]["subnet_id"]["get_resource"] = "demo_subnet";

            #Server1
            jObj["resources"]["server1"] = {};
            jObj["resources"]["server1"]["type"] = "OS::Nova::Server";
            jObj["resources"]["server1"]["properties"] = {};
            jObj["resources"]["server1"]["properties"]["availability_zone"] = data["server1"]["availability_zone"];
            jObj["resources"]["server1"]["properties"]["flavor"] = data["server1"]["flavor"];
            jObj["resources"]["server1"]["properties"]["image"] = data["server1"]["image"];
            jObj["resources"]["server1"]["properties"]["name"] = data["server1"]["name"];
            jObj["resources"]["server1"]["properties"]["key_name"] = {};
            jObj["resources"]["server1"]["properties"]["key_name"]["get_resource"] = "demo_key";
            jObj["resources"]["server1"]["properties"]["networks"] = [{}];
            jObj["resources"]["server1"]["properties"]["networks"][0]["network"] = {};
            jObj["resources"]["server1"]["properties"]["networks"][0]["network"]["get_resource"] = "demo_net";
            jObj["resources"]["server1"]["properties"]["networks"][0]["port"] = {};
            jObj["resources"]["server1"]["properties"]["networks"][0]["port"]["get_resource"] = "server1_port";

            # Create Server1 Floating IP
            jObj["resources"]["server1_floating_ip"] = {};
            jObj["resources"]["server1_floating_ip"]["type"] = "OS::Neutron::FloatingIP";
            jObj["resources"]["server1_floating_ip"]["properties"] = {};
            jObj["resources"]["server1_floating_ip"]["properties"]["floating_network"] = data["server1_floating_ip"]["floating_network"];
            jObj["resources"]["server1_floating_ip"]["properties"]["port_id"] = {};
            jObj["resources"]["server1_floating_ip"]["properties"]["port_id"]["get_resource"] = "server1_port";

            # Create Server1 Port
            jObj["resources"]["server1_port"] = {};
            jObj["resources"]["server1_port"]["type"] = "OS::Neutron::Port";
            jObj["resources"]["server1_port"]["properties"] = {};
            jObj["resources"]["server1_port"]["properties"]["fixed_ips"] = [{}];
            jObj["resources"]["server1_port"]["properties"]["fixed_ips"][0]["subnet_id"] = {};
            jObj["resources"]["server1_port"]["properties"]["fixed_ips"][0]["subnet_id"]["get_resource"] = "demo_subnet";
            jObj["resources"]["server1_port"]["properties"]["network_id"] = {};
            jObj["resources"]["server1_port"]["properties"]["network_id"]["get_resource"] = "demo_net";

            # Server2
            jObj["resources"]["server2"] = {};
            jObj["resources"]["server2"]["type"] = "OS::Nova::Server";
            jObj["resources"]["server2"]["properties"] = {};
            jObj["resources"]["server2"]["properties"]["availability_zone"] = data["server2"]["availability_zone"];
            jObj["resources"]["server2"]["properties"]["flavor"] = data["server2"]["flavor"];
            jObj["resources"]["server2"]["properties"]["image"] = data["server2"]["image"];
            jObj["resources"]["server2"]["properties"]["name"] = data["server2"]["name"];
            jObj["resources"]["server2"]["properties"]["key_name"] = {};
            jObj["resources"]["server2"]["properties"]["key_name"]["get_resource"] = "demo_key";
            jObj["resources"]["server2"]["properties"]["networks"] = [{}];
            jObj["resources"]["server2"]["properties"]["networks"][0]["network"] = {};
            jObj["resources"]["server2"]["properties"]["networks"][0]["network"]["get_resource"] = "demo_net";
            jObj["resources"]["server2"]["properties"]["networks"][0]["port"] = {};
            jObj["resources"]["server2"]["properties"]["networks"][0]["port"]["get_resource"] = "server2_port";

            # Create Server2 floating IP
            jObj["resources"]["server2_floating_ip"] = {};
            jObj["resources"]["server2_floating_ip"]["type"] = "OS::Neutron::FloatingIP";
            jObj["resources"]["server2_floating_ip"]["properties"] = {};
            jObj["resources"]["server2_floating_ip"]["properties"]["floating_network"] = data["server2_floating_ip"]["floating_network"];
            jObj["resources"]["server2_floating_ip"]["properties"]["port_id"] = {};
            jObj["resources"]["server2_floating_ip"]["properties"]["port_id"]["get_resource"] = "server2_port";

            # Create Server2 Port
            jObj["resources"]["server2_port"] = {};
            jObj["resources"]["server2_port"]["type"] = "OS::Neutron::Port";
            jObj["resources"]["server2_port"]["properties"] = {};
            jObj["resources"]["server2_port"]["properties"]["fixed_ips"] = [{}];
            jObj["resources"]["server2_port"]["properties"]["fixed_ips"][0]["subnet_id"] = {};
            jObj["resources"]["server2_port"]["properties"]["fixed_ips"][0]["subnet_id"]["get_resource"] = "demo_subnet";
            jObj["resources"]["server2_port"]["properties"]["network_id"] = {};
            jObj["resources"]["server2_port"]["properties"]["network_id"]["get_resource"] = "demo_net";

            # Create Volume
            jObj["resources"]["cinder_volume"] = {};
            jObj["resources"]["cinder_volume"]["type"] = "OS::Cinder::Volume";
            jObj["resources"]["cinder_volume"]["properties"] = {};
            jObj["resources"]["cinder_volume"]["properties"]["size"] = 1;
            jObj["resources"]["cinder_volume"]["properties"]["availability_zone"] = "nova";

            # Attach Volume to server2
            jObj["resources"]["volume_attachment"] = {};
            jObj["resources"]["volume_attachment"]["type"] = "OS::Cinder::VolumeAttachment";
            jObj["resources"]["volume_attachment"]["properties"] = {};
            jObj["resources"]["volume_attachment"]["properties"]["volume_id"] = {};
            jObj["resources"]["volume_attachment"]["properties"]["volume_id"]["get_resource"] = "cinder_volume";
            jObj["resources"]["volume_attachment"]["properties"]["instance_uuid"] = {};
            jObj["resources"]["volume_attachment"]["properties"]["instance_uuid"]["get_resource"] = "server2";
            jObj["resources"]["volume_attachment"]["properties"]["mountpoint"] = "/dev/sdb";

        with open("sample-revised.json", "w") as writeJson:
            json.dump(jObj, writeJson)
        self.convertJson2Yaml("sample-revised.json");

    # Convert json to yaml
    def convertJson2Yaml(self, file):
        with open(file) as jData:
            fileContent = yaml.safe_dump(json.load(jData), default_flow_style=False)
            with open("sample-revised.yaml", "w") as writeData:
                writeData.write(str(fileContent))
        orchObj = orchestration.Ochestration();
        #Call orchestration modue to orchestrate openstack resources
        orchObj.orchestrateResource("eric-dev-new.yaml");


obj = ProcessJson();
obj.process("sample.json");


