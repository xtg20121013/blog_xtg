#!/bin/sh
set -e

if [ "$1" == "upgradedb" ]
then
    python main.py upgradedb
fi
exec supervisord -n
