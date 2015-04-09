#!/bin/bash

# sintaksa za zagon:
# ~$ ./pistream.sh server_ip [preset_location]
# 
# privzet preset location je ./custom_ultrafast.ffpreset
# za "debug" namene je server ip lahko lunavm (stream na virtualko)

# nastavi ip streama
STREAM_IP="212.235.189.232:10000"
if [ ! $1 ]
then
	echo "Cannot stream, no server IP set!"
	exit 1
elif [ ! $1 == "lunavm" ]
then
	STREAM_IP=$1
fi

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
raspivid -t 99999999 -n -w 320 -h 240 -o - | ffmpeg -an -i - -vcodec copy -an -pix_fmt yuv420p $USE_PRESET -tune zerolatency -f mpegts "udp://"$STREAM_IP"?pkt_size=1316"
