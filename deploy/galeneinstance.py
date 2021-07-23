from pulumi.resource import ComponentResource, ResourceOptions
from pulumi_gcp import *


class ServerArgs():
    def __init__(
            self,
            admin_password: str,
            max_user: int,
            ip_query_url: str,
            ssl_cert: str,
            ssl_key: str):
        self.admin_password = admin_password
        self.max_user = max_user
        self.ip_query_url = ip_query_url
        self.ssl_cert = ssl_cert
        self.ssl_key = ssl_key


class GaleneInstance(ComponentResource):
    def __init__(
            self,
            name: str,
            args: ServerArgs,
            opts: ResourceOptions = None):
        super().__init__("custom:app:GaleneServer", name, {}, opts)

        default_net = compute.get_network("default")
        firewall = self.create_firewall(default_net)
        script = f"""#!/bin/bash
        docker run -d --restart always -p 443:8443 -p 1194:1194 -p 1194:1194/udp -e EXTERNAL_IP_QUERY_URL={args.ip_query_url} -e ADMIN_PASSWORD={args.admin_password} -e SSL_CERTIFICATE=\'{args.ssl_cert}\' -e SSL_PRIVATE_KEY=\'{args.ssl_key}\' -p 32000-32099:32000-32099/udp bendahl/galene:master
        """

        container_instance_addr = compute.address.Address(name)
        instance_type = self.map_instance_type(args.max_user)
        container_instance = self.create_instance(container_instance_addr, default_net, firewall, name, script,
                                                  instance_type)

        self.name = container_instance.name
        self.external_ip = container_instance_addr.address
        self.register_outputs({})

    @staticmethod
    def create_instance(container_instance_addr, default_net, firewall, name, script, instance_type):
        return compute.Instance(
            name,
            machine_type=instance_type,
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

    @staticmethod
    def create_firewall(network):
        return compute.Firewall(
            "galene-ingress",
            network=network.id,
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

    @staticmethod
    def map_instance_type(max_user: int):
        """ This method provides a rough sizing estimate based on the information given at galene.org. The values
        for instance sizes required for meetings > 40 users are extrapolated, but have not been verified by load
        testing. Therefore, the upper bound is chosen a bit more conservatively, probably not fully using all available
        CPU resources."""
        if 1 < max_user < 30:
            return "n2-highcpu-2"
        if 30 <= max_user <= 40:
            return "n2-highcpu-4"
        if 40 < max_user <= 80:
            return "n2-highcpu-16"
        if 80 < max_user <= 100:
            return "n2-highcpu-32"

        raise InvalidInstanceSizeException(f"{max_user} is out of range. Typical group sizes are between 20 and 100 "
                                           f"users.")


class InvalidInstanceSizeException(Exception):
    pass
