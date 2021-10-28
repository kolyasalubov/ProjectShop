#!/bin/sh
restart_bot () {
  pkill -f main.py
  echo "Changes detected, restarting..."
  python main.py
}

echo "Starting bot..."
python main.py &
inotifywait -mr -e modify / |\
while read
do
  restart_bot
done