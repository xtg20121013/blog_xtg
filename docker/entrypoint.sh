set -e

if [ "$1" == "upgradedb" ]
then
    exec python main.py upgradedb
else
    exec supervisord -n
fi