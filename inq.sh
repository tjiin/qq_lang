#!/bin/bash

echo "INQ"
while [ "$REPLY" != "quit" ]; do
	read -r -p ">"
	# myVar=$(</dev/stdin)
	echo "#REPLY"
done
exit 1

