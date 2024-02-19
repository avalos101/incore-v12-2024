================
 External tests
================

Install Dependencies
====================

If you don't use dockers:

* Install phantomjs `2.0.0+ <https://github.com/ariya/phantomjs/commit/244cf251cd767db3ca72d1f2ba9432bda0b0ba7d>`__ ::

    wget https://gist.github.com/julionc/7476620/raw/e8f36f2a2d616720983e8556b49ec21780c96f0c/install_phantomjs.sh
    sed -i 's/phantomjs-1.9.8/phantomjs-2.1.1/' install_phantomjs.sh
    # check script before running.
    less install_phantomjs.sh
    bash install_phantomjs.sh

* Update python library::

    pip3 install -U requests
    pip3 install 'requests[security]'

* For python 3 and higher versions::

    pip3 install unittest2

If **"No module named unittest2" Error** is given even if unittest2 is already installed, inside the incore docker open python in terminal and execute next::

    import sys
    sys.path.append('/usr/local/lib/python3.5/dist-packages')

or append the path where unittest2 was installed.

Docker
======

* use *-dev* images of `install-incore <https://github.com/it-projects-llc/install-incore>`__, e.g. ``itprojectsllc/install-incore:10.0-dev``

::

    docker network create multi_session_test_network

    docker run --network=multi_session_test_network -d -e POSTGRES_USER=incore -e POSTGRES_PASSWORD=incore --name db_ms_test postgres:9.5


    docker run \
    -e DB_PORT_5432_TCP_ADDR=db_ms_test \
    --network=multi_session_test_network \
    -e INCORE_MASTER_PASS=admin \
    -e DATABASE=test_database \
    -e INCORE_DOMAIN=incore-nginx \
    -v /PATH/TO/pos-addons/:/mnt/addons/it-projects-llc/pos-addons/ \
    -v /PATH/TO/incore/:/mnt/incore-source/ \
    --name incore \
    -t itprojectsllc/install-incore:$INCORE_BRANCH-dev -- --workers=1 -d test_database --db-filter test_database


    docker run \
    -p 8080:80 \
    --name incore-nginx \
    --network=multi_session_test_network \
    -t itprojectsllc/docker-incore-nginx

* Note. Name ``incore`` for docker container is mandatory for nginx container and cannot be changed

Prepare inCore
============

* in file ``addons/point_of_sale/static/src/js/gui.js`` comment out following line ::

    self.close_other_tabs();

* in file ``addons/bus/static/src/js/bus.js`` replace ::

      if(typeof Storage !== "undefined"){
          bus.bus = new CrossTabBus();
      } else {
          bus.bus = new bus.Bus();
      }

  with the following code: ::

      bus.bus = new bus.Bus();

* use database with demo data
* configure nginx to handle ``/longpolling/poll`` requests (no needed if you use docker instruction above)
* Add following System Parameter:

  * Key: ``pos_multi_session.allow_external_tests``
  * Value: ``1``

Run inCore
========
if you don't use docker instruction above:

* set ``-d`` (``--database``) parameter
* use default port
* set ``--db-filter``  equal to database name
* set ``--workers=1``

Run tests
=========

To run tests, you need to run incore server and then execute::

    cd pos_multi_session
    DATABASE=test_database python -m unittest discover -t . -s external_tests

To run only one file::

    DATABASE=test_database python -m unittest discover -t . -s external_tests -p test_sync.py

Run tests in Docker
-------------------
::

    docker exec -u incore -i -t incore /bin/bash -c "\
    cd /mnt/addons/it-projects-llc/pos-addons/pos_multi_session; \
    python -m unittest discover -t . -s external_tests"

Run tests in browser
====================

You can try repeat test in real browser, though it's not very convenient

* open incore with localhost:8080
* open POS interface
* copy-paste code from ``pos_multi_session/external_tests/tests/inject.js``
* line-by-line copy-paste test js code from ``pos_multi_session/external_tests/tests/test_sync.py``, e.g.

  * in admin window::

        console.log('test_10_new_order');
        mstest.remove_all_orders();

  * in demo window::

        mstest.remove_all_orders();

  * in admin window::

        mstest.fill_order();

  * etc.

Run tests for separated servers
===============================

To run tests on separated servers do what is written in previous paragraphs and create two dockers more. First docker below will process functionality of main server while 'incore' container will provide synchronization. The second docker provides longpolling support for the first one.
::

    docker run \
    -e DB_PORT_5432_TCP_ADDR=db_ms_test \
    --network=multi_session_test_network \
    -p 8080:8080 \
    -p 8072:8072 \
    -e INCORE_MASTER_PASS=admin \
    -e DATABASE=db_incore_main \
    -e INCORE_DOMAIN=incore-main-nginx \
    -e INCORE_PORT=8069 \
    -v /PATH/TO/pos-addons/:/mnt/addons/it-projects-llc/pos-addons/ \
    -v /PATH/TO/incore/:/mnt/incore-source/ \
    --name incore-main \
    -t itprojectsllc/install-incore:10.0-dev -- --workers=1 -d db_incore_main --db-filter db_incore_main


    docker run \
    -p 8888:80 \
    --name incore-main-nginx \
    --network=multi_session_test_network \
    -t itprojectsllc/docker-incore-nginx

Main Server Configuration
-------------------------
* Open via localhost:8888
* Install necessary modules
* Configure main server according to instructions provided in module ``pos_multi_session_sync`` ``/doc/index.rst`` ``Configuration/Main Server``. Use ``incore-nginx`` like ``external server url``

Sync Server Configuration
-------------------------
* Run this session strictly in a different with the previous session browser to prevent data base addressation confusing
* Open via localhost:8080
* Configure sync server according to instructions provided in module ``pos_multi_session_sync`` ``/doc/index.rst`` ``Configuration/Separate Sync Server``
* Set parameter ``pos_multi_session.allow_external_tests`` with value '1' like it was for ``pos_longpolling.allow_public``.

incore-main-nginx Container Configuration
---------------------------------------
* Open ``incore-main-nginx`` container via::

    docker exec -i -u root -t incore-main-nginx /bin/bash

* Modify nginx configuration file ``etc/nginx/nginx.conf`` as represented below::

    user  nginx;

    worker_rlimit_nofile 1024;
    worker_processes 1;

    pid        /var/run/nginx.pid;
    error_log  /var/log/nginx/error.log;

    events {
      worker_connections 1024;
    }
    http {
      include /etc/nginx/mime.types;
      default_type  application/octet-stream;

      sendfile on;

      server_tokens on;

      types_hash_max_size 1024;
      types_hash_bucket_size 512;

      server_names_hash_bucket_size 64;
      server_names_hash_max_size 512;

      keepalive_timeout  65;
      tcp_nodelay        on;

      gzip              on;
      gzip_http_version 1.0;
      gzip_proxied      any;
      gzip_min_length   500;
      gzip_disable      "MSIE [1-6]\.";
      gzip_types        text/plain text/xml text/css
                        text/comma-separated-values
                        text/javascript
                        application/json
                        application/xml
                        application/x-javascript
                        application/javascript
                        application/atom+xml;

      proxy_redirect          off;

      proxy_connect_timeout   90;
      proxy_send_timeout      90;
      proxy_read_timeout      90;
      proxy_buffers           32 4k;
      proxy_buffer_size       8k;
      proxy_set_header         Host $http_host;
      proxy_set_header         X-Real-IP $remote_addr;
      proxy_set_header         X-Forward-For $proxy_add_x_forwarded_for;
      # when redirecting to https:
      # proxy_set_header         X-Forwarded-Proto https;
      proxy_set_header         X-Forwarded-Host $http_host;
      proxy_headers_hash_bucket_size 64;

      # List of application servers
      upstream app_servers {
        server incore-main:8080;
      }

      # Configuration for the server
      server {

        listen 80 default;

        client_max_body_size 1G;

        add_header              Strict-Transport-Security "max-age=31536000";
        add_header 'Access-Control-Allow-Origin' * always;

         location / {
            proxy_pass http://incore-main:8080;
            proxy_read_timeout    6h;
            proxy_connect_timeout 5s;
            proxy_redirect        off;
            #proxy_redirect        http://$host/ https://$host:$server_port/;
            add_header X-Static no;
            proxy_buffer_size 64k;
            proxy_buffering off;
            proxy_buffers 4 64k;
            proxy_busy_buffers_size 64k;
            proxy_intercept_errors on;

          }
          location /longpolling {
          proxy_pass http://incore-main:8072;
          }
      }
    }

* Do not forget to restart your 'incore-main-nginx' container after all steps::

    docker restart incore-main-nginx

incore-nginx Container Configuration
----------------------------------
* Open ``incore-nginx`` container via::

    docker exec -i -u root -t incore-nginx /bin/bash

* Modify nginx configuration file ``etc/nginx/nginx.conf`` as represented below::

    user  nginx;

    worker_rlimit_nofile 1024;
    worker_processes 1;

    pid        /var/run/nginx.pid;
    error_log  /var/log/nginx/error.log;

    events {
      worker_connections 1024;
    }
    http {
      include /etc/nginx/mime.types;
      default_type  application/octet-stream;

      sendfile on;

      server_tokens on;

      types_hash_max_size 1024;
      types_hash_bucket_size 512;

      server_names_hash_bucket_size 64;
      server_names_hash_max_size 512;

      keepalive_timeout  65;
      tcp_nodelay        on;

      gzip              on;
      gzip_http_version 1.0;
      gzip_proxied      any;
      gzip_min_length   500;
      gzip_disable      "MSIE [1-6]\.";
      gzip_types        text/plain text/xml text/css
                        text/comma-separated-values
                        text/javascript
                        application/json
                        application/xml
                        application/x-javascript
                        application/javascript
                        application/atom+xml;

      proxy_redirect          off;

      proxy_connect_timeout   90;
      proxy_send_timeout      90;
      proxy_read_timeout      90;
      proxy_buffers           32 4k;
      proxy_buffer_size       8k;
      proxy_set_header         Host $http_host;
      proxy_set_header         X-Real-IP $remote_addr;
      proxy_set_header         X-Forward-For $proxy_add_x_forwarded_for;
      # when redirecting to https:
      # proxy_set_header         X-Forwarded-Proto https;
      proxy_set_header         X-Forwarded-Host $http_host;
      proxy_headers_hash_bucket_size 64;

      # List of application servers
      upstream app_servers {
        server incore:8080;
      }

      # Configuration for the server
      server {

        listen 80 default;

        client_max_body_size 1G;

        add_header              Strict-Transport-Security "max-age=31536000";
        add_header 'Access-Control-Allow-Origin' * always;

       location / {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range,X-Debug-Mode';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
             }
          add_header 'Access-Control-Allow-Origin' * always;
          proxy_pass http://incore:8080;
          proxy_read_timeout    6h;
          proxy_connect_timeout 5s;
          proxy_redirect        off;
          #proxy_redirect        http://$host/ https://$host:$server_port/;
          add_header X-Static no;
          proxy_buffer_size 64k;
          proxy_buffering off;
          proxy_buffers 4 64k;
          proxy_busy_buffers_size 64k;
          proxy_intercept_errors on;

        }
        location /longpolling {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range,X-Debug-Mode';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
             }
        add_header 'Access-Control-Allow-Origin' * always;
        proxy_pass http://incore:8072;
        }
      }
    }

* Do not forget to restart your 'incore-main-nginx' container after all steps::

    docker restart incore-nginx

Run tests in Docker for separated servers
-----------------------------------------
::

    docker exec -u incore -i -t incore-main /bin/bash -c "\
    cd /mnt/addons/it-projects-llc/pos-addons/pos_multi_session; \
    INCORE_PORT=80 python -m unittest discover -t . -s external_tests"

