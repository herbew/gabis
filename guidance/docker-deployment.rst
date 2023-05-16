#|==============================================================================
#|          D E P L O Y M E N T   G U I D A N C E with Docker
#|==============================================================================

# 1. DOCKER INSTALLATION
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

	sudo apt-get update
	sudo apt install apt-transport-https ca-certificates curl software-properties-common
	
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
	
	apt-cache policy docker-ce
	Installed: (none)
	  Candidate: 5:19.03.9~3-0~ubuntu-focal
	  Version table:
	     5:19.03.9~3-0~ubuntu-focal 500
	        500 https://download.docker.com/linux/ubuntu focal/stable amd64 Packages
	        
	        
	sudo apt install docker-ce
	sudo systemctl status docker
	
	sudo usermod -aG docker $USER
	
	# IF Permission Denied
	sudo chmod 666 /var/run/docker.sock
	
	# Base https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
	
	sudo apt  install docker-compose


# 2. DONWNLOAD REPOSITORY
	git clone https://github.com/herbew/gabis.git
	git clone https://herbew@bitbucket.org/8campus/static33.git static
	  
	cp -Rf static gabis/gabis
	
	cd gabis/

# 3 CREATE a ENV file
	..<your directory>/gabis
	vi .env
	-------------------------------------------------------------------------------
	DATABASE_URL=postgres://ugabis:PwDgabisSatu1Dua3@container_postgres/db_gabis
	
	DJANGO_ADMIN_URL=admin/
	DJANGO_SETTINGS_MODULE=config.settings.production
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
	            
	REDIS_URL=redis://container_redis:6379
	REDISTOGO_URL=redis://container_redis:6379
	IP_MONGODB=container_mongo
	IP_REDIS=container_redis
	DJANGO_ALLOWED_HOSTS=192.168.0.161 
	-------------------------------------------------------------------------------
	
	DJANGO_ALLOWED_HOSTS set as localhost or IP of cloud/VM
	
	# Trace Deployment
	docker-compose up
	docker-compose build
	
	# Deployment
	docker-compose up -d
	docker-compose up -d --build
	
	
	# ssh
	docker exec -it <ID Container> /bin/bash
	
	
	https://docs.docker.com/engine/reference/commandline
	
	docker image ls
	docker image rm -f <ID>
	
	
	docker rm $(docker ps -a -f status=exited -q)
	docker rmi $(docker images -a)
	
	docker container ls
	docker kill $(docker ps -q)
	

# 4 RUN TEST 
	python3 -m pytest
	
	or
	
	python3 ./manage.py test gabis.apps.masters.tests.parsers.nextbase.test_csv_documents
	
	
	
	docker exec -it container_ID_or_name /bin/bash
	
	docker stop c8b57c4bf7e3
	docker rmi -f c8b57c4bf7e3
	
	
	