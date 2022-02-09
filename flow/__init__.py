import os
import flickrapi
import webbrowser

from flask import Flask

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
    f = flickrapi.FlickrAPI(app.config['FLICKR_API_KEY'], app.config['FLICKR_API_SECRET'], store_token=False)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        # if not authenticated, go through the OAuth flow
        # else
        AUTH=True
        if not AUTH:
            f.authenticate_via_browser(perms='read')
            pass 
        else:
            return 'Hello, authenticated user!'

        # out-of-band flow
        #if not f.token_valid(perms='read'):
        #    # Get a request token
        #    f.get_request_token(oauth_callback='oob')

        #    # Open a browser at the authentication URL. Do this however
        #    # you want, as long as the user visits that URL.
        #    authorize_url = f.auth_url(perms='read')
        #    webbrowser.open_new_tab(authorize_url)

        #    # Get the verifier code from the user. Do this however you
        #    # want, as long as the user gives the application the code.
        #    verifier = str(input('Verifier code: '))

        #    # Trade the request token for an access token
        #    f.get_access_token(verifier)
        #else:
        #    return 'Hello, authenticated user!'

    @app.route('/callback')
    def callback():

        # https://localhost:16502/?oauth_token=72157720832530627-1d1c235a02d71a5f&oauth_verifier=c157aa47a3d7b349
        print(request)

    return app
