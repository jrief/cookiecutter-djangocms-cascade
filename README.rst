Cookiecutter for django-CMS with Cascade
========================================

Powered by Cookiecutter_, **cookiecutter-djangocms-cascade** is a set of templates for jumpstarting a
django-CMS project quickly.

Use this Cookiecutter to run a simple django-CMS. It adds a simple navigation bar, a footer
and a placeholder to add components out of the Cascade plugin system.


Quick How-To
------------

Install cookiecutter_, pipenv_ and npm_ onto your operating system, for instance

on Ubuntu

.. code-block:: bash

	sudo apt-get install python-cookiecutter pipenv nodejs npm

on MacOS

.. code-block:: bash

	sudo brew install cookiecutter pipenv node

.. note:: If ``pipenv`` is not available through your package manager, try with ``pip install pipenv``.

then change into your projects directory and invoke

.. code-block:: bash

	cookiecutter --no-input https://github.com/jrief/cookiecutter-djangocms-cascade

This creates a directory named ``my-cms``. Using this directory, either run the django-CMS demo locally, or
deploy it onto a Docker Machine.


Run django-CMS demo locally
---------------------------

Running the django-CMS demo locally is probably the best choice, when you want to experiment.

.. code-block:: bash

	cd my-cms
	pipenv install --sequential
	npm install
	export DJANGO_DEBUG=1
	pipenv run ./manage.py migrate
	pipenv run ./manage.py createsuperuser
	./manage.py runserver

Point a browser onto http://localhost:8000/?edit and log in with your credentials.

This demo uses SQLite as its database. It does neither support caching, nor full text searches.


Run django-CMS in Docker as Standalone Application
--------------------------------------------------

Running the django-CMS demo inside a Docker container, allows you to test all features such as full
text search, proper caching, running asynchronous tasks and uses a Postgres database. Check that
your Docker machine is running, if unsure invoke ``docker-machine ip``.

On answering the Cookiecutter questions, say ``use_docker=Yes`` and ``use_uwsgi_protocol=NO``.

.. code-block:: bash

	cd my-cms
	docker-compose up --build -d
	docker-compose exec wsgiapp /web/manage.py createsuperuser

Point a browser onto http://<docker-machine-ip>:9009/ and start surfing. Determine the IP address using
``docker-machine ip``. You will be redirected onto the login screen for Django. Use the credentials as
provided in the previous statement.


Run django-CMS in Docker behind NGiNX
-------------------------------------

In the previous configuration, uWSGI is configured to listen on port 9009 for HTTP requests. There
we can connect the browser directly onto the Docker machine's IP address. In a productive
environment, we might want to use NGiNX as a proxy in front of our Django application server. This
allows us to proxy services for multiple domains and to use https.

First we must create two separate Docker containers. This has to be done only once per host. Using
this setup, we can connect as many containers as our machine can handle. In a separte folder,
create a file named ``docker-compose.yml`` and add this content:

.. code-block:: yaml

	version: '2.0'

	services:
	  nginx-proxy:
	    restart: always
	    image: jwilder/nginx-proxy:latest
	    ports:
	      - '80:80'
	      - '443:443'
	    volumes:
	      - nginxcerts:/etc/nginx/certs:ro
	      - nginxvhostd:/etc/nginx/vhost.d
	      - /usr/share/nginx/html
	      - /var/run/docker.sock:/tmp/docker.sock:ro
	    networks:
	      - nginx-proxy

	  letsencrypt-nginx-proxy-companion:
	    restart: always
	    image: jrcs/letsencrypt-nginx-proxy-companion
	    # environment:  # remove this fake certificate in production
	    # - ACME_CA_URI=https://acme-staging.api.letsencrypt.org/directory
	    volumes:
	      - nginxcerts:/etc/nginx/certs:rw
	      - /var/run/docker.sock:/var/run/docker.sock:ro
	    volumes_from:
	      - nginx-proxy

	networks:
	  nginx-proxy:
	    external: true

	volumes:
	  nginxcerts:
	  nginxvhostd:

Now start the proxy together with its companion:

.. code-block:: bash

	docker-compose up -d

If they are running, switch back to your working directory and recreate the project answering the
Cookiecutter questions with ``use_docker=Yes`` and ``use_uwsgi_protocol=YES``.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _npm: https://www.npmjs.com/get-npm
.. _pipenv: https://pipenv.readthedocs.io/
