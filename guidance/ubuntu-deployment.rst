#|==============================================================================
#|          D E P L O Y M E N T   G U I D A N C E with Ubuntu 20.04
#|==============================================================================

sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libpq-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

INSTALL DATABASE
--------------------
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'

sudo apt update
sudo apt-get install postgresql-10

sudo -u postgres psql -c "CREATE USER ugabis WITH ENCRYPTED PASSWORD 'PwDgabisSatu1Dua3';"
sudo -u postgres psql -c "CREATE DATABASE db_gabis;"

sudo -u postgres psql db_gabis -c "GRANT ALL ON ALL TABLES IN SCHEMA public to ugabis;"
sudo -u postgres psql db_gabis -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to ugabis;"
sudo -u postgres psql db_gabis -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to ugabis;"

INSTALL MONGODB
--------------------
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

sudo wget --quiet -O - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
sudo apt-get install gnupg
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo apt-get install mongodb-org=4.4.4 mongodb-org-server=4.4.4 mongodb-org-shell=4.4.4 mongodb-org-mongos=4.4.4 mongodb-org-tools=4.4.4
ps --no-headers -o comm 1
sudo systemctl start mongod.service
sudo systemctl daemon-reload

sudo systemctl status mongod
sudo systemctl enable mongod
sudo systemctl stop mongod
sudo systemctl restart mongod


IF ANY ERROR ONLY
-------------------
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock
sudo systemctl restart mongod


mongo <<EOF
use db_gabis_trails;
db.createUser(
  {
    user: "trail_gabis",
    pwd: "PwDgabisSatu1Dua3",
    roles: [{ role: "readWrite", db: "db_gabis_trails" },]
  },
);
use db_gabis_django_message;
db.createUser(
  {
    user: "django_messages_gabis",
    pwd: "PwDgabisSatu1Dua3",
    roles: [{ role: "readWrite", db: "db_gabis_django_messages" },]
  },
);
use db_gabis_bookings
db.createUser(
  {
    user: "booking_gabis",
    pwd: "PwDgabisSatu1Dua3",
    roles: [{ role: "readWrite", db: "db_gabis_bookings" },]
  }
);
EOF


use db_gabis_trails
db.dropDatabase();

use db_gabis_django_message
db.dropDatabase();

use db_gabis_bookings
db.dropDatabase();

db.dropUser("trail_gabis");
db.dropUser("django_messages_gabis");
db.dropUser("booking_gabis");

true
show users;


sudo apt-get install language-pack-id
sudo dpkg-reconfigure locales

sudo apt-get install -y python3 python3-pip 
sudo apt-get install -y python3-venv

python3 -m pip install --user pipenv

git clone https://github.com/herbew/gabis.git
git clone https://herbew@bitbucket.org/8campus/static33.git static
  
cp -Rf static gabis/gabis

#sudo ln -s /home/herbew/gabis /opt/gabis
python3 -m venv envgabis
  
source envgabis/bin/activate


sudo apt-get install dos2unix -y 
cd gabis

dos2unix utility/install_os_dependencies.sh
dos2unix utility/install_python_dependencies.sh
sudo ./utility/install_os_dependencies.sh install

source envgabis/bin/activate
cd gabis

sudo -H pip3 install virtualenv
./utility/install_python_dependencies.sh
pip install -r requirements/production.txt
_________________________________________
DATABASE_URL=postgres://ugabis:PwDgabisSatu1Dua3@127.0.0.1/db_gabis

DJANGO_ADMIN_URL=admin/
DJANGO_SETTINGS_MODULE=config.settings.local
DJANGO_SECRET_KEY=#6kuxzt=%fb(+npb18f%l$b$t2+nkh*t48*2$l&r4-h-zyprn6

DJANGO_EMAIL_BACKEND=anymail.backends.mailjet.EmailBackend
DJANGO_SERVER_EMAIL=
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_DEBUG=True

DJANGO_MAILGUN_API_KEY=
DJANGO_MAILGUN_SERVER_NAME=

DJANGO_EMAIL_HOST=
DJANGO_EMAIL_PORT=
DJANGO_EMAIL_USER=
DJANGO_EMAIL_PASSWORD=

MAILJET_API_KEY=
MAILJET_SECRET_KEY=

REDIS_URL=redis://localhost:6379
REDISTOGO_URL=redis://localhost:6379
IP_MONGODB=localhost
IP_REDIS=localhost
	
____________________________________________________________________________


 python3 ./manage.py migrate sites
 python3 ./manage.py makemigrations localized
 python3 ./manage.py makemigrations users
 python3 ./manage.py makemigrations masters
 python3 ./manage.py makemigrations schedules

 python3 ./manage.py migrate
 
 python3 ./manage.py update_translation_fields users
 python3 ./manage.py update_translation_fields masters
 python3 ./manage.py update_translation_fields localized
 python3 ./manage.py update_translation_fields schedules
 
 python3 ./manage.py collectstatic --noinput
 python3 ./manage.py shell -c "from gabis.apps.users.models import User; User.objects.create_superuser('herbew', 'herbew@gmail.com', 'password')"
 python3 ./manage.py shell -c "from gabis.apps.users.models import User; user = User.objects.get(username='herbew'); user.types='001'; user.save()"
 
#Redis
 sudo apt install redis-server redis
 
 
sudo systemctl enable redis
sudo systemctl start redis
sudo systemctl restart redis
sudo systemctl daemon-reload
sudo systemctl status redis

#Gunicorn

assume absolute path of the source /home/herbew/filecontroller/
vi /home/herbew/filecontroller/config/systemd/gunicorn/gunicorn.service
user as herbew
____________:

User=herbew
WorkingDirectory=/home/herbew/gabis
ExecStart=/home/herbew/envgabis/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/herbew/herbew.sock config.wsgi:application

____________


sudo cp -f config/systemd/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service

sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl status gunicorn

#RQWorker
assume absolute path of the source /home/herbew/filecontroller/
user as herbew
____________:

User=herbew
WorkingDirectory=/home/herbew/gabis
ExecStart=/home/herbew/envgabis/bin/python3 /home/herbew/gabis/manage.py rqworker high default low

____________

sudo cp -f config/systemd/rqworker/rqworker.service /etc/systemd/system/rqworker.service
sudo systemctl enable rqworker
sudo systemctl start rqworker
sudo systemctl restart rqworker
sudo systemctl daemon-reload
sudo systemctl status rqworker

#HTTPS--Cerbot
sudo apt install certbot python3-certbot-nginx

IF ANY ERROR
------------
sudo apt install snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot

sudo ln -s /snap/bin/certbot /usr/bin/certbot


#NGINX
assume absolute path of the source /home/herbew/filecontroller/
user as herbew
vi /home/herbew/filecontroller/config/nginx/local-nginx.conf

sudo apt install nginx

sudo cp -f config/nginx/local-nginx.conf /etc/nginx/sites-available/gabis
sudo ln -s /etc/nginx/sites-available/gabis /etc/nginx/sites-enabled/

sudo chown -R www-data:www-data /var/log/nginx;
sudo chmod -R 755 /var/log/nginx;

#Test--
sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful


sudo service nginx configtest

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx
sudo systemctl daemon-reload
sudo systemctl status nginx


sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart rqworker

http://192.168.0.121:8080/en-us/master/document/list/

#ONLY change 
sudo vi /etc/nginx/sites-available/gabis
server {

          access_log /var/log/nginx/access.log combined;
      add_header Cache-Control no-cache;

          listen 80;
          server_name  192.168.0.121;

       ...

sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart rqworker


sudo apt install redis-server