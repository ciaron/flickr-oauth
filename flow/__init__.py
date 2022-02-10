import os
import flickrapi
import webbrowser

from flask import Flask
from flask import url_for, redirect, request, session

#FLICKR_API_KEY=os.environ['API_KEY']
#FLICKR_API_SECRET=os.environ['API_SECRET']

def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    #f = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, store_token=False)
    #f = flickrapi.FlickrAPI(app.config['FLICKR_API_KEY'], app.config['FLICKR_API_SECRET'], store_token=False)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        # if not authenticated, go through the OAuth flow
        # else
        #AUTH=False
        #if not AUTH:
        #    #f.authenticate_via_browser(perms='read')
        #    f.get_request_token()
        #    url = f.auth_url(perms='read')
        #    return (url_for('index'))
        #else:
        #    return 'Hello!'
        return 'Hello!'

    @app.route('/login')
    def login():
        #f = flickrapi.FlickrAPI(app.config['FLICKR_API_KEY'], app.config['FLICKR_API_SECRET'], store_token=False, token_cache_location='/tmp/.flickr')
        f = flickrapi.FlickrAPI(app.config['FLICKR_API_KEY'], app.config['FLICKR_API_SECRET'], token_cache_location='/tmp/.flickr')
        if f.token_valid(perms='read'):
            # Already logged in
            print('Already logged in, redirecting to index.')
            return redirect(url_for('index'))

        # Get the request token
        callback = url_for('auth_ok', _external=True)
        print('Getting request token with callback URL %s' % callback)
        f.get_request_token(oauth_callback=callback)

        authorize_url = f.auth_url(perms='read')

        # Store it in the session, to use in auth_ok()
        session['request_token'] = f.flickr_oauth.resource_owner_key
        session['request_token_secret'] = f.flickr_oauth.resource_owner_secret
        session['requested_permissions'] = f.flickr_oauth.requested_permissions
        print(session)

        print('Redirecting to %s.' % authorize_url)
        return redirect(authorize_url)

    @app.route('/auth_ok')
    def auth_ok():
        #f = flickrapi.FlickrAPI(app.config['FLICKR_API_KEY'], app.config['FLICKR_API_SECRET'], store_token=False, token_cache_location='/tmp/.flickr')
        f = flickrapi.FlickrAPI(app.config['FLICKR_API_KEY'], app.config['FLICKR_API_SECRET'], token_cache_location='/tmp/.flickr')
        f.flickr_oauth.resource_owner_key = session['request_token']
        f.flickr_oauth.resource_owner_secret = session['request_token_secret']
        f.flickr_oauth.requested_permissions = session['requested_permissions']
        verifier = request.args['oauth_verifier']

        print('Getting resource key')
        f.get_access_token(verifier)
        return 'Verifier is %s' % verifier

    @app.route('/callback')
    def callback(request):

        # https://localhost:16502/?oauth_token=72157720832530627-1d1c235a02d71a5f&oauth_verifier=c157aa47a3d7b349
        print(request)

    return app
