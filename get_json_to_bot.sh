#!/bin/bash

HOST="10.3.131.14"
PORT="22"
USERNAME="root"
PRIVATE_KEY="/Users/e.polyakov/.ssh2/id_rsa_new"

REMOTE_COMMAND="/home/deploy_bot/test.sh"

ssh -o StrictHostKeyChecking=no -i "$PRIVATE_KEY" -p "$PORT" "$USERNAME"@"$HOST" "$REMOTE_COMMAND"

scp -i "$PRIVATE_KEY" -P "$PORT" "$USERNAME"@"$HOST":/home/deploy_bot/stdout.json /Users/e.polyakov/Downloads/DEPLOY_BOT

REMOTE_COMMAND="> /home/deploy_bot/stdout.json"
ssh -o StrictHostKeyChecking=no -i "$PRIVATE_KEY" -p "$PORT" "$USERNAME"@"$HOST" "$REMOTE_COMMAND"
