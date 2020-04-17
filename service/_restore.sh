#!/bin/bash

# include credentials
. ../.env

DUMP_FILENAME=$1
[[ -z $DUMP_FILENAME ]] && DUMP_FILENAME='../data/backup/dump.sql'

# Restore
cat $DUMP_FILENAME | docker exec -i $POSTGRES_HOST psql -U$POSTGRES_USER $POSTGRES_BASE
