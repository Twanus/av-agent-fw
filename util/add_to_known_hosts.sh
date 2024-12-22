#!/bin/bash

# Usage: ./add_to_known_hosts.sh <hostname>
HOSTNAME=$1

if [ -z "$HOSTNAME" ]; then
  echo "Usage: $0 <hostname>"
  exit 1
fi

# Fetch the host key and append it to the known_hosts file
ssh-keyscan -H $HOSTNAME >> ~/.ssh/known_hosts

echo "Host key for $HOSTNAME added to known_hosts."
