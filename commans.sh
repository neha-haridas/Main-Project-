[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/mypro/Main-Project-
ExecStart=/home/ubuntu/mypro/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          MycardProjectect.wsgi:application

[Install]
WantedBy=multi-user.target