#! /bin/bash

function checkProcess() {
  _count=$(ps -ef | grep python3 | grep corona_server.py | wc -l)
}

checkProcess

if [ $_count = 0 ]; then
  python3 corona_server.py &
  sleep 3
else
  echo "サーバ起動中です。"
fi
