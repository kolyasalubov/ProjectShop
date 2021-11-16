#!/bin/sh


echo "Starting bot..."

while true
do
  python main.py &
  process=$!
  sleep 5
  inotifywait -qr "." -e modify --exclude "__"
  kill $process
  echo "Changes detected, restarting..."
done
