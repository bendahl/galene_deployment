import os
import pulumi

from galeneinstance import GaleneInstance, ServerArgs

cfg = pulumi.Config()
ip_query_url = cfg.get("ip_query_url") or "ipinfo.io/ip"
admin_password = os.getenv("ADMIN_PASSWORD")
max_user = int(os.getenv("MAX_USER")) or 0
ssl_certificate = os.getenv("SSL_CERTIFICATE")
ssl_private_key = os.getenv("SSL_PRIVATE_KEY")

instance = GaleneInstance("galene-server",
                          ServerArgs(
                              admin_password,
                              max_user,
                              ip_query_url,
                              ssl_certificate,
                              ssl_private_key,
                          ))

pulumi.export("Container Instance Name", instance.name)
pulumi.export("External IP", instance.external_ip)
pulumi.export("Meeting URL", f'https://{instance.external_ip}/group/meeting')
