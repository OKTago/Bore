from local_settings import APP_ID, APP_SECRET, APP_FACE_URL, SCOPES
import urllib
import cgi

def get_cookie_name():
    return "fbs_" + APP_ID

def redirect_to_auth():
    scopes = ",".join(SCOPES)
    return "<script>top.location.href=\"https://graph.facebook.com/oauth/authorize?client_id="+APP_ID+"&redirect_uri="+APP_FACE_URL+"&scope="+scopes+"\";</script>"

def get_token(code):
    args = dict(client_id=APP_ID, redirect_uri=APP_FACE_URL)
    args["client_secret"] = APP_SECRET
    args["code"] = code
    response = cgi.parse_qs(urllib.urlopen(
        "https://graph.facebook.com/oauth/access_token?" +
        urllib.urlencode(args)).read())
    access_token = response["access_token"][-1]
    return access_token
