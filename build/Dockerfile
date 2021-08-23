## Git tag to be used. This controls which galene version will actually be built. Default: master
ARG ARG_VERSION=master

## Build Container
FROM golang:1-alpine as builder
ARG ARG_NAME
ARG ARG_VERSION
ENV NAME="Galene Video Conferencing Server"
ENV VERSION=${ARG_VERSION}
LABEL maintainer="Benjamin Dahlmanns"

RUN set -ex \
  && echo "Building ${NAME}. Version: ${VERSION}" \
  && apk update \
  && apk upgrade \
  && apk add \
    git \
  && rm -rf /var/cache/apk/* \
  && cd /opt \
  && git clone --depth=1 --branch ${VERSION} https://github.com/jech/galene \
  && cd galene \
  && CGO_ENABLED=0 go build -ldflags='-s -w' \
  && cd galene-password-generator \
  && CGO_ENABLED=0 go build -ldflags='-s -w' -o galene-password-generator \
  && cd .. \
  && echo "${NAME} version: ${VERSION}" > version \
  && echo "Done building ${NAME} ${VERSION}"


## Runtime Container
FROM alpine:3.13
LABEL maintainer="Benjamin Dahlmanns"

ENV ADMIN_USERNAME="admin"
ENV ADMIN_PASSWORD=""
ENV USER_PASSWORD=""

# This variable should point to a URL that will return the external IP of the host machine. This can either be an external
# service, like ipinfo.io or some internal meta data URL offered by your cloud provider.
# If this variable is left blank, the turn server will be startet with default settings. Otherwise, the external ip will be
# used to create the socket.
ENV EXTERNAL_IP_QUERY_URL=""

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
VOLUME /opt/galene/data /opt/galene/groups /opt/galene/recordings

EXPOSE 8443
EXPOSE 1194
EXPOSE 1194/udp
# May not make sense, depending on how flexible the setup will be... (currently, max of 80 users)
EXPOSE 32000-32079/udp

WORKDIR /opt/galene
COPY --from=builder /opt/galene/galene .
COPY --from=builder /opt/galene/galene-password-generator/galene-password-generator .
COPY --from=builder /opt/galene/static static
COPY --from=builder /opt/galene/version .
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY groups/meeting.json /opt/galene/templates/groups/meeting.json

RUN set -ex \
  && apk update \
  && apk upgrade \
  && apk add \
    gettext \
    tzdata \
  && rm -rf /var/cache/apk/* \
  && chmod 755 /usr/local/bin/docker-entrypoint.sh \
  && addgroup galene -g 1000 \
  && adduser -u 1000 -G galene -D galene
