import secrets
import pulumi
from galeneinstance import GaleneInstance, ServerArgs

cfg = pulumi.Config()
ip_query_url = cfg.get("ip_query_url") or "ipinfo.io/ip"
admin_password = cfg.require_secret("admin_password")

instance = GaleneInstance("galene-server",
                          ServerArgs(
                              ip_query_url,
                              admin_password
                          ))

pulumi.export("container_instance_name", instance.name)
pulumi.export("container_instance_external_ip", instance.external_ip)
