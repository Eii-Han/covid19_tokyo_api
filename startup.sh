#! /bin/bash

function checkProcess() {
  _count=$(pgrep -fc "corona_server.py")
}

checkProcess
if [ "$_count" = 0 ]; then
  python3 corona_server.py &
  sleep 3
else
  echo "サーバ起動中です。"
fi
