# fastapi-websocket
fast api with using websocket simple example app

## Requirements
- Python 3.10
- FastAPI
- Uvicorn
- Websocket

## Installation
```bash
pip install -r requirements.txt
```

## How to run
```bash
uvicorn main:app --reload
```

## nginx
# create nginx file
```bash
sudo nano /etc/nginx/sites-available/chat.conf
```
# and add this file when edit something place
```
map $http_upgrade $connection_upgrade {
    default upgrade;
        '' close;
    }

  upstream websocket {
      server unix:/run/gunicorn.sock;
  }

  server {
      server_name your-domain.uz; // bu joyini o'zgartish kerak
      listen 80;
      location / {
          proxy_pass http://websocket;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection $connection_upgrade;
          proxy_set_header Host $host;
      }
      location /chat {
          proxy_pass http://websocket;
          include proxy_params;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
      }
  }
```
# nginx lan file
```bash
sudo ln /etc/nginx/sites-available/chat.conf /etc/nginx/sites-enabled/chat.conf

then

sudo nginx -t
sudo systemctl restart nginx
```

## gunicorn service
```
bash
sudo nano /etc/systemd/system/gunicorn.socket

then paste this code

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
## and then
```
bash
sudo nano /etc/systemd/system/gunicorn.service

then paste this code

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/something/fastapi-websocket // bu joydagi file pathni o'zgartirasiz
ExecStart=/home/something/fastapi-websocket/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 3 -b 0.0.0.0:8000 -t 360 --reload --access-logfile - main:app // bu joydagini ham o'zgartirasiz

[Install]
WantedBy=multi-user.target
```

# and then restart
```
bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```



