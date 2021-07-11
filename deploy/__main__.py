import asyncio
import pulumi
from pulumi.resource import ResourceOptions
from pulumi_gcp import compute

cfg = pulumi.Config()
ip_query_url = cfg.get("ip_query_url") or "ipinfo.io/ip"

def get_admin_password(pw: str):
    global admin_password 
    admin_password = pw
cfg.require_secret("admin_password").apply(get_admin_password)


default_net = compute.get_network("default")
firewall = compute.Firewall(
    "galene-ingress",
    network=default_net.id,
    priority=80,
    target_tags=["galene"],
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

script = f"""#!/bin/bash
docker run -d --restart always -p 443:8443 -p 1194:1194 -p 1194:1194/udp -e EXTERNAL_IP_QUERY_URL={ip_query_url} -e ADMIN_PASSWORD={admin_password} -p 32000-32100:32000-32100/udp bendahl/galene:master
"""

container_instance_addr = compute.address.Address(
    "galene-container-instance")

container_instance = compute.Instance(
    "galene-container-instance",
    machine_type="n1-standard-1",
    boot_disk=compute.InstanceBootDiskArgs(
        initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
            image="cos-cloud/cos-stable-89-16108-470-1",
        )
    ),
    metadata_startup_script=script,
    tags=["galene"],
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
pulumi.export("container_instance_name", container_instance.name)
pulumi.export("container_instance_external_ip",
            container_instance_addr.address)


    