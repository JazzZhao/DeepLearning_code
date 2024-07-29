## NL2SQL代码
### 项目示例结构

* app_nl2sql_server
* ​	---logs    # 日志文件存放目录
* ​	---utils     # 各种工具函数
* ​		---gen_query.py  # 请求大模型接口
* ​		---NW_ChatBot.py   # 初始化类
* ​		---prompts.py   # prompts编写
* ​		---get_logger.py   # 处理日志的文件
*      ---write_query.py   # 拼接请求大模型参数
* ​	---views   # 视图函数目录
* ​		---nl2sql.py   # 视图文件
* ​	---config.json    # 配置文件
* ​ ---app_core.py    # flask初始化文件
* ​ ---app_server.py   # 服务启动文件
* ​ ---gunicorn.py   # gunicorn配置文件(多线程部署)
* ​ ---manage_server.sh   # 以sh命令启动脚本
* ​	---requirements.txt   # 服务所依赖的环境文件
* ​	---start.sh   # docker启动sh脚本
* test   # 服务测试脚本目录

### 启动方式

* 1. 以py文件启动
*    python app_server.py   
*    说明: 在app_server.py 下面修改对应的端口, 只适合本地调试,线上不要这样操作
* 
* 2. 以gunicorn方式启动
*    gunicorn -c gunicorn.py app_server:app
*    说明: 1. 根据自身的配置修改gunciorn中的workers参数设置并发
*    	   2. 启动容器的时候-p port1:port2  port2端口要和bing参数中:后面的端口保持一致
*    	   3. 如果知道自己一个并发占用多少显存, 可以打开注释2-16行, 只需要指定显卡, 服务会自动计算当前给的显卡能启动多少并发
* 
* 3. nginx 部署
* 
*    ......
* 


### 启动镜像

docker run -p 8082:8082 --name nl2sql --restart=always -v /ai_home/zhongjiayi/gpu_server/nl2sql:/home/nl2sql -itd common_base_env:20240427 /bin/bash /home/nl2sql/start.sh



说明: -p 指定端口, 前面的8082只要宿主机支持该端口就行,可以随便设置, 后面的一个8082一定要和容器中代码保持一致, 如果是python启动那就和app_server.py中设置的端口保持一致, 如果是gunicorn那就和gunicorn中bind中的端口保持一致, 如果是nginx启动则和nginx中监听的端口保持一致
* ​     --name 给容器起一个别名
*    	--restart=always 保证容器如果在服务器重启或者容器被杀也能自己再次启动
* ​     -v 前面的路径是代码路径, 后面的路径是挂载到容器中的路径, 也可以挂载多个-v
* ​     -itd 以守护进程的方式后台运行
* ​     /bin/bash 后面的是服务启动的脚本路径


注: 如果是以dockerfile构建的镜像就可以不要/bin/bash + 后面的启动脚本, 直接把启动命令写到dockerfile中去
       