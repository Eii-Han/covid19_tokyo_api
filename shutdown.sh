#! /bin/bash

function getProcessCount(){
  _count=$(pgrep -fc "corona_server.py")
}

function getPid(){
  _pid=$(pgrep -f "corona_server.py" | head -1)
}

getProcessCount
if [ "$_count" -gt 0 ]; then
  getPid
  kill "$_pid"
  sleep 3
  getProcessCount
  if [ "$_count" = 0 ]; then
    echo 'サーバ終了しました。'
  else
    echo 'サーバ終了処理が失敗しました。'
  fi
else
  echo 'サーバ起動していません。'
fi

