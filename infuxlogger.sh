#!/bin/bash

BUCKET="testing"
ORG="electronicayciencia@gmail.com"
URL="https://eu-central-1-1.aws.cloud2.influxdata.com"
TOKEN="l3-Ay...V7n44Gw=="

FILE="obras.log"


tail -f $FILE | while read time timestamp rms maxvalue
do
	lineformat="sndobras rms=$rms,maxvalue=$maxvalue ${timestamp}000000000"
	
	echo "$time => $lineformat"

    curl -sS "$URL/api/v2/write?bucket=$BUCKET&org=$ORG" \
        -H "Authorization: Token $TOKEN" \
        -H 'Content-Type: text/plain' \
        --data "$lineformat"
done
