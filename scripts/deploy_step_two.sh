#! /bin/bash

### SERVER DEPLOY AUTOMATION PART 2 ###

# STEP 1: set up python environment for Django app (should be in virtualenv)
pip install -r ../requirements.txt

# STEP 2: download uwsgi and nginx
sudo apt-get install build-essential nginx
sudo -H pip3 install uwsgi

# STEP 3: copy and paste configuration files for uwsgi and nginx
sudo mkdir -p /etc/uwsgi/sites
sudo cp /home/woobak_template/config/uwsgi/woobak.ini /etc/uwsgi/sites/woobak.ini
sudo cp /home/woobak_template/config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service

sudo cp /home/woobak_template/config/nginx/woobak.conf /etc/nginx/sites-available/woobak.conf
sudo ln -s /etc/nginx/sites-available/woobak.conf /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start uwsgi

# STEP 4: changing firewall options
sudo ufw allow 'Nginx Full'

# STEP 5: last step configuring uwsgi and nginx
sudo systemctl enable nginx
sudo systemctl enable uwsgi

# STEP 4: configuring supervisor and firing up celery/celerybeat workers
sudo apt-get install supervisor
sudo service supervisor start
systemctl status supervisor
sudo supervisorctl status

cd /etc/supervisor/confd

touch celerybeat.conf
touch celery.conf

sudo apt-get install rabbitmq-server
systemctl status rabbitmq-server
