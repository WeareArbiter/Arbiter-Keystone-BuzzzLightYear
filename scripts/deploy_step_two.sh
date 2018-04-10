#! /bin/bash

# when file doesn't work: sed -i 's/\r$//' [filename]

### SERVER DEPLOY AUTOMATION PART 2 ###

# STEP 1: download uwsgi and nginx and rabbitmq-server
sudo apt-get install build-essential nginx
sudo -H pip3 install uwsgi

# STEP 2: set up python environment for Django app (should be in virtualenv)
pip install -r /home/arbiter/buzzz.co.kr/requirements.txt

# STEP 3: copy and paste configuration files for uwsgi and nginx
sudo mkdir -p /etc/uwsgi/sites
sudo cp /home/arbiter/buzzz.co.kr/config/uwsgi/buzzz.ini /etc/uwsgi/sites/buzzz.ini
sudo cp /home/arbiter/buzzz.co.kr/config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service

sudo cp /home/arbiter/buzzz.co.kr/config/nginx/buzzz.conf /etc/nginx/sites-available/buzzz.conf
sudo ln -s /etc/nginx/sites-available/buzzz.conf /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start uwsgi

# STEP 4: changing firewall options
sudo ufw allow 'Nginx Full'

# STEP 5: last step configuring uwsgi and nginx
sudo systemctl enable nginx
sudo systemctl enable uwsgi

# STEP 4: configuring supervisor and firing up celery/celerybeat workers
sudo apt-get install supervisor rabbitmq-server
sudo service supervisor start

sudo cp /home/arbiter/buzzz.co.kr/config/supervisor/celery.conf /etc/supervisor/conf.d/celery.conf
sudo cp /home/arbiter/buzzz.co.kr/config/supervisor/celerybeat.conf /etc/supervisor/conf.d/celerybeat.conf

sudo mkdir -p /var/log/celery
sudo touch /var/log/celery/arbiter_worker.log
sudo touch /var/log/celery/arbiter_beat.log

sudo supervisorctl reread
sudo supervisorctl update
