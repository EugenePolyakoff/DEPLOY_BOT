#!/bin/bash

HOST="10.3.131.14"
PORT="22"
USERNAME="root"
PRIVATE_KEY="/Users/e.polyakov/.ssh2/id_rsa_new"

REMOTE_COMMAND="/opt/qradar/upgrade/util/setup/upgrades/do_deploy.pl"

ssh -o StrictHostKeyChecking=no -i "$PRIVATE_KEY" -p "$PORT" "$USERNAME"@"$HOST" "$REMOTE_COMMAND"