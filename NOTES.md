# Getting permission in an interactive Python session
```
>>> f.token_valid(perms='read')
False
>>> f.get_request_token(oauth_callback='oob')
>>> authorize_url = f.auth_url(perms='read')
>>> import webbrowser
>>> webbrowser.open_new_tab(authorize_url)
True
>>> f.get_access_token('594-342-293')
>>> f.token_valid(perms='read')
```
