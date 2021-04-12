# monitor-tel部署

## 修改系统配置
echo "net.core.somaxconn = 4096" >> /etc/sysctl.conf   
sysctl -p  


## 配置python基础环境
yum install gcc gcc-c++ libtool make libffi-devel openssl-devel sqlite-devel mysql-devel git -y  

./configure --prefix=/usr/local/python3.6.4  
make  
make install  



## 部署项目  
    pip3 install virtualenv  
    # 配置阿里云python源并安装依赖包  
    cd /usr/local/webserver/monitor-tel/mysite/monitoring
    pip3 install -r requirements.txt  
    # 配置项目环境  
    cd /usr/local/webserver/
    virtualenv monitor-tel
    source /usr/local/webserver/monitor-tel/bin/activate

    
    # 部署项目  
    git clone git@172.16.17.29:ops/project/monitor-tel.git



    # 初始化数据库  
	django-admin startproject mysite
	python3 manage.py startapp monitoring
    mkdir -p /usr/local/webserver/monitor-tel/logs
    mkdir -p /usr/local/webserver/monitor-tel/mysite/logs  
	cp -r /usr/local/webserver/monitor-tel/monitor-tel/* /usr/local/webserver/monitor-tel/mysite/
	修改/usr/local/webserver/monitor-tel/mysite/mysite/settings.py数据库连接 
    修改/usr/local/webserver/monitor-tel/mysite/mysite/celery.py 消息中间件连接（app，  BROKER_URL，CELERY_RESULT_BACKEND）
    python3 manage.py makemigrations  
    python3 manage.py migrate  

## 配置进程管理工具
pip3 install supervisor==4.2.1
sudo mkdir -p /etc/supervisor  
sudo scp -r /usr/local/webserver/monitor-tel/mysite/monitoring/supervisord/* /etc/supervisor/   
sudo chown tq.tq -R /etc/supervisor   


启动 supervisord 
查看 supervisorctl status


## 配置nginx转发(例)  
    server  {
        listen 80 ;
        server_name monitor-tel.test.in.chinawyny.com;
        location / {
            uwsgi_pass  monitor-tel;
            include     /usr/local/nginx/uwsgi_params; # the uwsgi_params file you installed
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            #proxy_set_header X-Forwarded-Port $server_port;
            proxy_set_header HOST $host:$server_port;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_next_upstream http_500 http_502 http_503 error timeout invalid_header;
            }
        #location /static {
        #    alias /usr/local/webserver/django/mysite/static; # your Django project's static files - amend as required
        #    }
    }
    
    upstream monitor-tel {
        #server unix:///usr/local/webserver/django/mysite/mysite.sock; # for a file socket
        server 172.16.17.77:8001; # for a web port socket (we'll use this first)
    }
    
    
    server  {
        listen 8000;
        server_name monitor-tel.test.in.chinawyny.com;
    
    location / {
        root /usr/local/www/tq/dist;
        index index.html;
        try_files $uri /index.html;
     }
    location /api {
        proxy_pass http://monitor-tel.test.in.chinawyny.com;
     }
    }