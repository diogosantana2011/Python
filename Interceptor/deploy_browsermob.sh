### FOR DOWNLOADER.SH

# Special handling for browsermob-core distribution zip
# if [[ "$URL" == *"browsermob-core"* ]]; then
#     ARTIFACT="browsermob-core"
#     VERSION=$(echo "$URL" | sed "s/\// /g" | awk '{print $9}')
#     DOMAIN_1="net"
#     DOMAIN_2="lightbody.bmp"
#     ZIP_URI="$NEXUS?r=$REPO&g=$DOMAIN_1.$DOMAIN_2&a=$ARTIFACT&v=$VERSION&p=zip"
#     echo "Downloading BrowserMob Proxy $VERSION ZIP from $ZIP_URI"
#     wget -nv --content-disposition "$ZIP_URI" -qO /tmp/browsermob.zip
#     # Extract to /srv/browsermob
#     mkdir -p /srv/browsermob
#     unzip -q /tmp/browsermob.zip -d /srv/browsermob
# fi

#!/bin/bash

#
# Deploy BrowserMob Proxy
#

SOURCE=/tmp/browsermob.zip
DEST_PATH=/srv/browsermob
SERVICE=browsermob
ENV_FILE=/etc/profile.d/browsermob.sh

scriptPath="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
basePath=${scriptPath%/*/*}
servicePath=$basePath/services/3et

###########################
# Check artifact present
if [ ! -f $SOURCE ]; then
  echo
  echo "    File $SOURCE not found! - Deploy failed"
  echo
  exit 1
fi

echo
echo "    File $SOURCE found - Deploy started"
echo

###########################
# Create service path
mkdir -p $DEST_PATH
rm -rf $DEST_PATH/*

echo "Extracting BrowserMob Proxy jar..."
cp -f $SOURCE $DEST_PATH/browsermob-proxy.jar

# Find the bin/browsermob-proxy script
BMPP_BIN=$(find $DEST_PATH -type f -path "*/bin/browsermob-proxy" | head -n 1)
if [ -z "$BMPP_BIN" ]; then
    echo "Error: browsermob-proxy script not found after extraction!"
    exit 1
fi

##########################
# Create/update env var for Python and system
echo "Configuring BROWSERMOB_PROXY_PATH..."
echo "export BROWSERMOB_PROXY_PATH=$BMPP_BIN" > $ENV_FILE
chmod +x $ENV_FILE

# Also export it in this shell for immediate use
export BROWSERMOB_PROXY_PATH=$BMPP_BIN

##########################
# Create systemd service
SYSTEMD_FILE=$servicePath/$SERVICE/$SERVICE.service
if [ ! -f $SYSTEMD_FILE ]; then
  echo "Systemd service file not found: $SYSTEMD_FILE"
  exit 1
fi

sed "s|{{BROWSERMOB_PROXY_PATH}}|$BROWSERMOB_PROXY_PATH|g" $SYSTEMD_FILE > /etc/systemd/system/$SERVICE.service
systemctl daemon-reload

#######################
# Start $SERVICE
systemctl restart $SERVICE
systemctl status $SERVICE --no-pager

rm -rf $SOURCE

RESULT=$(systemctl is-active $SERVICE)
if [ "$RESULT" != "active" ]; then
  echo "Error deploying $SERVICE"
  exit 1
fi

echo
echo " ** BrowserMob Proxy Deploy finished **"
echo "    BROWSERMOB_PROXY_PATH set to: $BROWSERMOB_PROXY_PATH"
echo
