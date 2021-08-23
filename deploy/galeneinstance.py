from pulumi.resource import ComponentResource, ResourceOptions
from pulumi_gcp import *


class ServerArgs():
    """
    ServerArgs holds the configuration values for a Galéne instance
    """

    def __init__(
            self,
            admin_password: str,
            max_user: int,
            ip_query_url: str,
            ssl_cert: str,
            ssl_key: str):
        """
        :param admin_password: password of the admin user of the meeting
        :param max_user: maximum number of participants for a meeting
        :param ip_query_url: url by which the external ip of the instance can be requested
        :param ssl_cert: SSL certificate used by the meeting. If left empty, a certificate will be generated.
        :param ssl_key: the SSL key that belongs to the given certificate (only needs to be set when a certificate is explicitly set as well)
        """
        self.admin_password = admin_password
        self.max_user = max_user
        self.ip_query_url = ip_query_url
        self.ssl_cert = ssl_cert
        self.ssl_key = ssl_key


class GaleneInstance(ComponentResource):
    """
    GaleneInstance represents a single Galéne instance along with all required resources, including network, firewall, etc...
    """

    def __init__(
            self,
            name: str,
            args: ServerArgs):
        """
        :param name: hostname of the instance
        :param args: arguments needed to instantiate the server (VM)
        """
        super().__init__("custom:app:GaleneServer", name, {})

        default_net = compute.get_network("default")
        firewall = self.create_firewall(default_net)
        script = f"""#!/bin/bash
        docker run -d --restart always -p 443:8443 -p 1194:1194 -p 1194:1194/udp -e EXTERNAL_IP_QUERY_URL={args.ip_query_url} -e ADMIN_PASSWORD={args.admin_password} -e SSL_CERTIFICATE=\'{args.ssl_cert}\' -e SSL_PRIVATE_KEY=\'{args.ssl_key}\' -p 32000-32079:32000-32079/udp bendahl/galene:master
        """

        container_instance_addr = compute.address.Address(name)
        instance_type = self.map_instance_type(args.max_user)
        container_instance = self.create_instance(container_instance_addr, default_net, firewall, name, script,
                                                  instance_type)
        self.name = container_instance.name
        self.external_ip = container_instance_addr.address
        self.meeting_url = container_instance_addr.address.apply(lambda ip: f"https://{ip}/group/meeting")
        self.register_outputs({})

    @staticmethod
    def create_instance(container_instance_addr, default_net, firewall, name, script, instance_type):
        """
        This method will create the actual VM instance and ensure that the given network and firewall settings are
        applied correctly. The script will be executed once and serves to initialize the actual container.

        :param container_instance_addr: external IPv4 address of the machine
        :param default_net: network to be used by this instance
        :param firewall: preconfigured firewall settings to be applied
        :param name: hostname of the instance
        :param script: start script that runs upon boot
        :param instance_type: instance sizing (e.g. 'n2-highcpu-2')
        :return:
        """
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
        """
        Creates a firewall specification for the Galéne instance. Besides SSH and HTTP/HTTPS, there are various ports
        that are required in order to serve media streams, etc.. All this is taken care of by this configuration.

        :param network: compute network to apply these rules to
        :return:
        """
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
                    ports=["1194", "32000-32079"]
                ),
            ]
        )

    @staticmethod
    def map_instance_type(max_user: int) -> str:
        """ This method provides a rough sizing estimate based on the information given at galene.org. The values
        for instance sizes required for meetings > 40 users are extrapolated, but have not been verified by load
        testing. Therefore, the upper bound is chosen a bit more conservatively, probably not fully using all available
        CPU resources.

        :param max_user: maximum number of users (values have to be in the closed interval [2, 100])
        :return: instance type name"""
        if 1 < max_user <= 20:
            return "n2-highcpu-2"
        if 20 < max_user <= 40:
            return "n2-highcpu-4"
        if 40 < max_user <= 80:
            return "n2-highcpu-16"

        raise InvalidInstanceSizeException(f"{max_user} is out of range. Valid group sizes are between 2 and 100 "
                                           f"users.")


class InvalidInstanceSizeException(Exception):
    """
    InvalidInstanceSizeException will be thrown when there is no valid instance mapping for the given number of users
    """
    pass
