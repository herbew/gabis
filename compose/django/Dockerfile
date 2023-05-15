FROM python:3.8

	ENV PYTHONUNBUFFERED 1
    
	RUN mkdir -p /opt/gabis
	COPY . ./opt/gabis
	
	WORKDIR /opt/gabis
	RUN chmod +x compose/django/docker-entrypoint.sh
	RUN pip3 install -r requirements/production.txt





