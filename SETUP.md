# Install dependencies

`apt install uwsgi uwsgi-plugin-python3`

# Setup nginx
```
location = /flickr-oauth { rewrite ^ /flickr-oauth/; }
location /flickr-oauth { try_files $uri @flickr-oauth; }
location @flickr-oauth {
  include uwsgi_params;
  uwsgi_pass unix:/tmp/flickr-oauth.sock;
}
```

# Set up uwsgi.ini:
```
[uwsgi]
socket = /tmp/flickr-oauth.sock
#chdir = /var/www
venv = /home/ciaron/ciaron.net/flickr-oauth/venv
#processes = 4
#threads = 2
plugins = python3
wsgi-file = /home/ciaron/ciaron.net/flickr-oauth/wsgi.py
# application is called "app" in wsgi.py:
module = wsgi:app
mount = /flickr-oauth=wsgi:app
chmod-socket = 666

```

# Set up flickr-oauth.py (the wsgi file):

```
from flow import create_app

app = create_app()

if __name__ == "__main__":
    app=create_app()
    app.run(debug=True)
```

# Run uwsgi as nginx user (www-data, see `id www-data`)
`uwsgi -s /tmp/flickr-oauth.sock --manage-script-name --uid=33 --gid=33 uwsgi.ini`

# TODO
run as system service or under supervisord, e.g.
https://www.devdungeon.com/content/run-python-wsgi-web-app-waitress
