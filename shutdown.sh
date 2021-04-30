#! /bin/bash

function getProcessCount(){
  _count=$(ps -ef | grep corona_server.py | grep -v grep | wc -l)
}

function getPid(){
  _pid=$(ps -ef | grep corona_server.py | grep -v grep | head -1 | awk '{print $2}')
}

getProcessCount
if [ $_count -gt 0 ]; then
  getPid
  kill $_pid
  sleep 3
  getProcessCount
  if [ $_count = 0 ]; then
    echo 'サーバ終了しました。'
  else
    echo 'サーバ終了処理が失敗しました。'
  fi
else
  echo 'サーバ起動していません。'
fi

