# Install dependencies

`apt install uwsgi uwsgi-plugin-python3`

# Setup nginx
```
location = /flickr-oauth { rewrite ^ /flickr-oauth/; }
location /flickr-oauth { try_files $uri @flickr-oauth; }
location @flickr-oauth {
  include uwsgi_params;
  uwsgi_pass unix:/tmp/yourapplication.sock;
}
```

# Set up uwsgi.ini:
```
[uwsgi]
socket = /tmp/yourapplication.sock
#chdir = /var/www
venv = /home/ciaron/ciaron.net/flickr-oauth/venv
processes = 4
threads = 2
plugins = python3
wsgi-file = /home/ciaron/ciaron.net/flickr-oauth/wsgi.py
```

# Set up wsgi.py:

```
from flow import create_app

if __name__ == "__main__":
    app=create_app()
    app.run(debug=True)
```

# Run uwsgi as user www-data (the nginx runner)
`uwsgi -s /tmp/yourapplication.sock --manage-script-name --mount /flickr-oauth=flickr-oauth:app --uid=33 --gid=33 uwsgi.ini`
 (or wsgi:app, feel free to fix this!)

# TODO
run as system service or under supervisord, e.g.
https://www.devdungeon.com/content/run-python-wsgi-web-app-waitress
