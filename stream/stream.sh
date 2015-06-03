#!/bin/bash

# sintaksa za zagon:
# ~$ ./stream.sh server_ip [preset_location]
# 
# privzet preset location je ./custom_ultrafast.ffpreset
# za "debug" namene je server ip lahko lunavm (stream na virtualko)

# nastavi ip streama
STREAM_IP=""
if [ ! $1 ]
then
	echo "Cannot stream, no server IP set!"
	exit 1
else
	STREAM_IP=$1
fi

STREAM_IP=$STREAM_IP":10000"

echo "Streaming to "$STREAM_IP
echo ""

# definiraj lokacijo preseta
PRESET_LOCATION="custom_ultrafast.ffpreset"
if [ $2 ]
then
	PRESET_LOCATION=$2
fi

# ugotovi kateri preset bomo uporabili
USE_PRESET="-fpre "$PRESET_LOCATION
if [ ! -e ${PRESET_LOCATION} ]
then
	echo "Custom preset file not found ("$PRESET_LOCATION"), using default ultrafast"
	USE_PRESET="-preset ultrafast"
fi

# start stream
ffmpeg -an -f video4linux2 -s 640x480 -i /dev/video0 -c:v h264 -an -pix_fmt yuv420p -r 20 $USE_PRESET -tune zerolatency -f mpegts "udp://"$STREAM_IP"?pkt_size=1316"
