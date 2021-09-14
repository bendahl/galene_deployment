import os
import pulumi

from galeneinstance import GaleneInstance, ServerArgs

# environment setup
cfg = pulumi.Config()
ip_query_url = cfg.get("ip_query_url") or "ipinfo.io/ip"
admin_password = os.getenv("ADMIN_PASSWORD")
user_password = os.getenv("USER_PASSWORD", default="")
max_user = int(os.getenv("MAX_USER") or "0")
# note that the certificate information is optional and may be base64 encoded
ssl_certificate = os.getenv("SSL_CERTIFICATE", default="")
ssl_private_key = os.getenv("SSL_PRIVATE_KEY", default="")

# instantiation -> this is where the actual provisioning takes place
instance = GaleneInstance("galene-server",
                          ServerArgs(
                              admin_password,
                              user_password,
                              max_user,
                              ip_query_url,
                              ssl_certificate,
                              ssl_private_key,
                          ))

# variables that will be published, so they can be conveniently accessed/seen by the user
pulumi.export("Container Instance Name", instance.name)
pulumi.export("External IP", instance.external_ip)
pulumi.export("Meeting URL", instance.meeting_url)
