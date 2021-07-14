from pulumi.resource import ComponentResource, ResourceOptions
from pulumi import Output
from pulumi_gcp import *


class ServerArgs():
    def __init__(
            self,
            ip_query_url: str,
            admin_password: Output[str]):
        self.ip_query_url = ip_query_url
        self.admin_password = admin_password


class GaleneInstance(ComponentResource):
    def __init__(
            self,
            name: str,
            args: ServerArgs,
            opts: ResourceOptions = None):
        super().__init__("custom:app:GaleneServer", name, {}, opts)

        default_net = compute.get_network("default")

        firewall = compute.Firewall(
            "galene-ingress",
            network=default_net.id,
            priority=80,
            allows=[
                compute.FirewallAllowArgs(
                    protocol="tcp",
                    ports=["22", "80", "443", "1194"]
                ),
                compute.FirewallAllowArgs(
                    protocol="udp",
                    ports=["1194", "32000-32099"]
                ),
            ]
        )

        # Todo: Certs
        #script = Output.all(args.admin_password).apply(lambda args: f"""#!/bin/bash
        script = args.admin_password.apply(lambda pw: f"""#!/bin/bash
        docker run -d --restart always -p 443:8443 -p 1194:1194 -p 1194:1194/udp -e EXTERNAL_IP_QUERY_URL={args.ip_query_url} -e ADMIN_PASSWORD={pw} -p 32000-32099:32000-32099/udp bendahl/galene:master
        """)

        container_instance_addr = compute.address.Address(name)

        container_instance = compute.Instance(
            name,
            machine_type="n1-standard-1",
            boot_disk=compute.InstanceBootDiskArgs(
                initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
                    image="cos-cloud/cos-stable-89-16108-470-1",
                )
            ),
            metadata_startup_script=script,
            network_interfaces=[
                compute.InstanceNetworkInterfaceArgs(
                    network=default_net.id,
                    access_configs=[compute.InstanceNetworkInterfaceAccessConfigArgs(
                        nat_ip=container_instance_addr.address
                    )]
                )
            ],
            service_account=compute.InstanceServiceAccountArgs(
                email="default",
                scopes=[
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring.write",
                    "https://www.googleapis.com/auth/pubsub",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/trace.append",
                ],
            ),
            opts=ResourceOptions(depends_on=[firewall]),
        )
        self.name = container_instance.name
        self.external_ip = container_instance_addr.address
        self.register_outputs({})
