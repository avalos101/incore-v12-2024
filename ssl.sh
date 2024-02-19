apt-get install nginx software-properties-common -y && add-apt-repository ppa:certbot/certbot && apt-get update && apt-get install certbot -y && mkdir /etc/nginx/ssl && openssl dhparam -out /etc/nginx/ssl/dhp-2048.pem 2048

# para subdominios
service nginx stop && certbot certonly --standalone -d luisfe.s2.incore.appm && service nginx start

# Dominios
service nginx stop && certbot certonly --standalone -d luisfe.s2.incore.appm -d www.luisfe.s2.incore.appm && service nginx start

#crear zona
nano /etc/nginx/sites-available/luisfe.s2.incore.appm

# contenido del archivo
upstream luisfe.s2.incore.appm {
    server 127.0.0.1:8080;
}

server {
    listen      443;
    server_name luisfe.s2.incore.appm www.luisfe.s2.incore.appm;

    access_log  /var/log/nginx/luisfe.s2.incore.appm.access.log;
    error_log   /var/log/nginx/luisfe.s2.incore.appm.error.log;

    ssl on;
    ssl_certificate     /etc/letsencrypt/live/luisfe.s2.incore.appm/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/luisfe.s2.incore.appm/privkey.pem;
    keepalive_timeout   60;

    ssl_ciphers "ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS:!AES256";
    ssl_protocols           TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_dhparam /etc/nginx/ssl/dhp-2048.pem;

    proxy_buffers 16 64k;
    proxy_buffer_size 128k;

    location / {
        proxy_pass  http://luisfe.s2.incore.appm;
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
        proxy_pass http://luisfe.s2.incore.appm;
    }
}

server {
    listen      80;
    server_name luisfe.s2.incore.appm www.luisfe.s2.incore.appm;

    add_header Strict-Transport-Security max-age=2592000;
    rewrite ^/.*$ https://$host$request_uri? permanent;
}
 # fin del contenido del archivo



#habilitar zona
ln -s /etc/nginx/sites-available/luisfe.s2.incore.appm /etc/nginx/sites-enabled/luisfe.s2.incore.appm && /etc/init.d/nginx restart
