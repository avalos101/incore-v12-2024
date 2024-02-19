apt-get install nginx software-properties-common -y
add-apt-repository ppa:certbot/certbot
apt-get update && apt-get install certbot -y
mkdir /etc/nginx/ssl && openssl dhparam -out /etc/nginx/ssl/dhp-2048.pem 2048
pip3 install --upgrade pip &&  pip3 install setuptools_rust && pip3 install --upgrade certbot


certbot certonly --rsa-key-size 4096 --manual --agree-tos --manual-public-ip-logging-ok --email="diego.avalos@incore.club" --server=https://acme-v02.api.letsencrypt.org/directory --preferred-challenges=dns --domain="*.integrapp.cloud"

nano /etc/nginx/sites-available/integrapp.cloud


# contenido del archivo

upstream integrapp.cloud {
    server 127.0.0.1:8080;
}

server {
    listen      443;
    server_name integrapp.cloud *.integrapp.cloud;

    access_log  /var/log/nginx/integrapp.cloud.access.log;
    error_log   /var/log/nginx/integrapp.cloud.error.log;

    ssl on;
    ssl_certificate     /etc/letsencrypt/live/integrapp.cloud/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/integrapp.cloud/privkey.pem;
    keepalive_timeout   60;

    ssl_ciphers "ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS:!AES256";
    ssl_protocols           TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_dhparam /etc/nginx/ssl/dhp-2048.pem;

    proxy_buffers 16 64k;
    proxy_buffer_size 128k;

    location / {
        proxy_pass  http://integrapp.cloud;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_redirect off;

        proxy_set_header    Host            $host;
        proxy_set_header    X-Real-IP       $remote_addr;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Forwarded-Proto https;
    }

    location ~* /web/static/ {
        proxy_cache_valid 200 60m;
        proxy_buffering on;
        expires 864000;
        proxy_pass http://integrapp.cloud;
    }
}

server {
    listen      80;
    server_name integrapp.cloud *.integrapp.cloud;

    add_header Strict-Transport-Security max-age=2592000;
    rewrite ^/.*$ https://$host$request_uri? permanent;
}
 # fin del contenido del archivo

ln -s /etc/nginx/sites-available/integrapp.cloud /etc/nginx/sites-enabled/integrapp.cloud && /etc/init.d/nginx restart
