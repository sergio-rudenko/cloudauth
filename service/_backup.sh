#!/bin/bash

# include credentials
. ../.env

DUMP_FILENAME=$1
[[ -z $DUMP_FILENAME ]] && DUMP_FILENAME='../data/backup/dump.sql'

CMD='docker exec -it '$POSTGRES_HOST' pg_dump -U'$POSTGRES_USER' -Cc --if-exists '$POSTGRES_BASE

# Dumpabase
$CMD > $DUMP_FILENAME
