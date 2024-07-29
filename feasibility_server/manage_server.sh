#!/bin/bash

notes="
		"${server_name}"
		启动服务：bash manage_server.sh gunicorn-start
		启动服务：bash manage_server.sh gunicorn-stop
	"

action=$1
server_name='app_server'

function activate_workplace(){
	source /home/miniconda3/etc/profile.d/conda.sh
	conda activate base
}

function start_server() {
	
	activate_workplace
	echo "激活 环境"
	gunicorn -c gunicorn.py "${server_name}:app"
	echo "启动 flask服务"
}

function stop_server(){
	echo "杀死进程：" `cat "${server_name}".pid`
	kill -9 `cat "${server_name}".pid`
}

function restart_server(){
	activate_workplace
	stop_server
	sleep 2
	star_server
}

function tail_server(){
	tail -200f "${server_name}".log
}

if [ -z "$action" ];
then
    echo "${notes}"
    echo "Error: action param is not null"
    
elif [ $action = "-h"  ] || [ $action = "--help"  ] || [ $action = "h"  ]
then
	echo "${notes}"
	echo "确保启用了conda环境"

elif [ "$action" = "gunicorn-start"  ]
then
	start_server

elif [ "$action" = "gunicorn-stop" ]
then
	stop_server

elif [ "$action" = "gunicorn-restart" ]
then 
	restart_server

else
     echo "Error: param error"
fi