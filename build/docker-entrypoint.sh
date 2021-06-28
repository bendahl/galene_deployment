#!/bin/sh

echo "$(date): starting $(cat /opt/galene/version)"

if [ -z "$ADMIN_USERNAME" ]
then
  ADMIN_USERNAME="admin"
fi

if [ -z "$ADMIN_PASSWORD" ]
then
  echo "Empty admin password not allowed. Aborting."
  exit 1
fi

cp /opt/galene/templates/groups/meeting.json /opt/galene/groups/meeting.json
sed -i s/__op_username__/${ADMIN_USERNAME}/g /opt/galene/groups/meeting.json
sed -i s/__op_password__/${ADMIN_PASSWORD}/g /opt/galene/groups/meeting.json
sed -i s/__user_password__/${USER_PASSWORD}/g /opt/galene/groups/meeting.json

## start service
cd /opt/galene || exit 1
chown galene:galene recordings
exec su galene -c "ulimit -n 65536 && ./galene -http :8443 -udp-range 32000-32099 $*"
