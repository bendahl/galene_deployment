#!/bin/sh

echo "$(date): starting $(cat /opt/galene/version)"

# Decode string if it is base64 encoded
decode() {
  echo $1 | base64 -d - 1>/dev/null 2>&1
  if [ ! $? -eq 0 ]
  then
    echo $1
  else
    echo $1 | base64 -d -
  fi
}

if [ -z "$ADMIN_USERNAME" ]
then
  ADMIN_USERNAME="admin"
fi

if [ -z "$ADMIN_PASSWORD" ]
then
  echo "Empty admin password not allowed. Aborting."
  exit 1
fi

GALENE_ENV=""

if [ -n "$SSL_CERTIFICATE" ]
then
  decode "$SSL_CERTIFICATE"  > /opt/galene/data/cert.pem
fi

if [ -n "$SSL_PRIVATE_KEY" ]
then
  decode "$SSL_PRIVATE_KEY" > /opt/galene/data/key.pem
fi

chown galene:galene /opt/galene/data/*

cp /opt/galene/templates/groups/meeting.json /opt/galene/groups/meeting.json
sed -i s/__op_username__/"${ADMIN_USERNAME}"/g /opt/galene/groups/meeting.json
sed -i s/__op_password__/"${ADMIN_PASSWORD}"/g /opt/galene/groups/meeting.json
sed -i s/__user_password__/"${USER_PASSWORD}"/g /opt/galene/groups/meeting.json

## start service
cd /opt/galene || exit 1
chown galene:galene recordings

if [ -z "$EXTERNAL_IP_QUERY_URL" ]
then
  echo "Starting galene with default turn settings (0.0.0.0:1194). Note that your video stream may not work without properly setting the external IP address."
  exec su galene -c "ulimit -n 65536 && ./galene -http :8443 -udp-range 32000-32079"
else
  EXTERNAL_IP=$(wget -q -O - $EXTERNAL_IP_QUERY_URL)
  echo "Starting galene with turn set to $EXTERNAL_IP:1194"
  exec su galene -c "ulimit -n 65536 && ./galene -http :8443 -udp-range 32000-32079 -turn $EXTERNAL_IP:1194"
fi
