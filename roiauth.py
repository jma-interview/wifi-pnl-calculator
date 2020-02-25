
import json
import base64
import requests
import urllib
from jose import jwt

try:
    from constant import cognito_domain, cognito_client_id, cognito_client_secret, local_host, dev_url, prod_url
    from exception import AuthException
except:
    from .constant import cognito_domain, cognito_client_id, cognito_client_secret, local_host, dev_url, prod_url
    from .exception import AuthException

class Cognito(object):
    Domain = cognito_domain
    Client_ID = cognito_client_id
    Client_Secret = cognito_client_secret
    Redirect_URL = local_host
    response_type = 'code'
    login = 'login'
    logout = 'logout'
    token = 'oauth2/token'

    @classmethod
    def oauth2_login(cls):
        return f'{cls.Domain}/{cls.login}?response_type={cls.response_type}&client_id={cls.Client_ID}&redirect_uri={cls.Redirect_URL}'

    @classmethod
    def oauth2_logout(cls):
        return f'{cls.Domain}/{cls.logout}?client_id={cls.Client_ID}&logout_uri={cls.Redirect_URL}{cls.logout}'

    @classmethod
    def oauth2_token_check(cls):
        return f'{cls.Domain}/{cls.login}?response_type=token&client_id={cls.Client_ID}&redirect_uri={cls.Redirect_URL}'

    @classmethod
    def oauth2_token(cls):
        return f'{cls.Domain}/{cls.token}'

    @classmethod
    def aws_authentication(cls):
        s = f'{cls.Client_ID}:{cls.Client_Secret}'
        encoded = base64.b64encode(s.encode('ascii')).decode("utf-8")
        return f'Basic {encoded}'

class DevCognito(Cognito):
    pass

class TestCognito(Cognito):
    Redirect_URL = dev_url
    pass

class ProdCognito(Cognito):
    Redirect_URL = prod_url
    pass

cognito = {
    'dev': DevCognito,
    'test': TestCognito,
    'prod': ProdCognito,

    'default': DevCognito
}

def get_token(code, conn=DevCognito):
    token_url = conn.oauth2_token()

    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : conn.aws_authentication()
    }
    params = {
        "grant_type" : "authorization_code",
        "redirect_uri": conn.Redirect_URL,
        "client_id": conn.Client_ID,
        "code":code
    }
    payload = urllib.parse.urlencode(params)

    r = requests.request("POST", token_url, data=payload, headers=headers)

    if r.status_code > 299:
        e_msg = 'Error in response of AWS Cognito Auth. Detail will be listed below: \n' \
                f'Status Code: {r.status_code }\nContent: {r.text}\n'
        raise AuthException(e_msg)

    token = json.loads(r.text).get("id_token")

    payload = jwt.get_unverified_claims(token)

    res = dict()
    res["given_name"] = payload.get('given_name')
    res["family_name"] = payload.get('family_name')
    res["user"] = payload.get('name')
    res["email"] = payload.get('email')
    return res


if __name__ == '__main__':
    # code = 'b19dd9ca-97ca-4b72-a3b4-def74a82cd35'
    #
    # login = get_token(code)
    #
    # print(login)
    #
    # c = cognito['default']
    # print(c.oauth2_login())
    # print(c.oauth2_logout())

    # https://pac-idam-userpool-prd.auth.us-west-2.amazoncognito.com/login?response_type=code&client_id=4dbh4toj0gq3en2enh2vnl6md4&redirect_uri=https://127.0.0.1:5000/

    # https://pac-idam-userpool-prd.auth.us-west-2.amazoncognito.com/logout?client_id=4dbh4toj0gq3en2enh2vnl6md4&logout_uri=https://127.0.0.1:5000/logout

    id_token='eyJraWQiOiJKdjRQNkY0TDFGcHZ2NWlwWVJlYndPeFEyNzFFWG1XWFNTdlpDRW16SGxBPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiS2hvMHBFOVNoNTlSYnhoRHg4ODM4dyIsInN1YiI6IjA3MjNiODRlLTI5NDYtNGVjNC1iMzdmLTI0MWIzZGNkZDMxYiIsImNvZ25pdG86Z3JvdXBzIjpbInVzLXdlc3QtMl9OSjFkV0NKaVZfUGFuYXNvbmljLmFlcm8iXSwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9OSjFkV0NKaVYiLCJjb2duaXRvOnVzZXJuYW1lIjoiUGFuYXNvbmljLmFlcm9fSmltbXkuQ2hlbkBwYW5hc29uaWMuYWVybyIsImdpdmVuX25hbWUiOiJKaW1teSIsImF1ZCI6IjRkYmg0dG9qMGdxM2VuMmVuaDJ2bmw2bWQ0IiwiaWRlbnRpdGllcyI6W3sidXNlcklkIjoiSmltbXkuQ2hlbkBwYW5hc29uaWMuYWVybyIsInByb3ZpZGVyTmFtZSI6IlBhbmFzb25pYy5hZXJvIiwicHJvdmlkZXJUeXBlIjoiU0FNTCIsImlzc3VlciI6Imh0dHBzOlwvXC9zdHMud2luZG93cy5uZXRcLzEwYmJiMjQ3LTA4ZGYtNGFkMy1hNTVlLTQ3YmU3NjkzYjFkMVwvIiwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE1NDc1NzYxNDYzNjUifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTQ4MjgyNzQ3LCJuYW1lIjoiSmltbXkuQ2hlbkBwYW5hc29uaWMuYWVybyIsImV4cCI6MTU0ODI4NjM0NywiaWF0IjoxNTQ4MjgyNzQ3LCJmYW1pbHlfbmFtZSI6IkNoZW4iLCJlbWFpbCI6IkppbW15LkNoZW5AcGFuYXNvbmljLmFlcm8ifQ.I2ZoN389MzWSsgK_pGd8tAmH1QAbzIasEhLDjMBBUHtagPW71TF1mPqeNCwEIz47SDbOxGKwijYgjlsz4viExeWt1nXExOxlP4G9x8F33R_JcF_VLUyJwH1Qx-bGNwplYUsFLF0xFG3cJDIBnNvs_ErTV7dYm-MFqcuCGIZgv3iWL5U2sEA5OHA_3qcYkJxCEoBCoetEefVyHEE7D7i0tWZz29cbbcZxMRPlc1lz_G8lKqd-WN-li_HN701mocFdxaEwpIyLPloCREZ4sLqbvky4mhWSwm0ZzcPpLhMYEjeoZH4mI8Jb9iTZ9AATRMTPseUqfJYyDGj6rNnmlV6OPA&access_token=eyJraWQiOiJiZGZVc2VoR3pQeUMxMm56TzdJS1dYZnFnTVR4NEpmcWdPZXI1dkpxcUVFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwNzIzYjg0ZS0yOTQ2LTRlYzQtYjM3Zi0yNDFiM2RjZGQzMWIiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy13ZXN0LTJfTkoxZFdDSmlWX1BhbmFzb25pYy5hZXJvIl0sInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NDgyODI3NDcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX05KMWRXQ0ppViIsImV4cCI6MTU0ODI4NjM0NywiaWF0IjoxNTQ4MjgyNzQ3LCJ2ZXJzaW9uIjoyLCJqdGkiOiI1NTA3YjVkNS05YTk0LTQ0MDMtYTY0Zi1mMjk2Yjg1OGE5ODEiLCJjbGllbnRfaWQiOiI0ZGJoNHRvajBncTNlbjJlbmgydm5sNm1kNCIsInVzZXJuYW1lIjoiUGFuYXNvbmljLmFlcm9fSmltbXkuQ2hlbkBwYW5hc29uaWMuYWVybyJ9.IAfhNJmtoPzljFj01z4QyhUkCc8whQjJen-Ere61mlgL7CP2NrJTVh8uiDvJmjgummOnqf-oJ0Dne1u3r5-eQjapCYhCMz0x3XxNvLGJXLRaslasYlGGASv96mrb652o5KhN8Z4G11riVqbTvbNHPJRw66hudprvy_LhVJ5PUF3CmF_2ln_TOKC9nVxjeNz1GALyvtWhpLOCZKjeR1pJWibjrBBtuWjpYRKBM8hWOrNspRSduuXgMWab8mHjiyrX3o0gXF7iroDXMcdpi39DlrkObYnWV0LlicoueCqaDCz3fqP_ko2h1YVcrU7xzSihcg61waGW9bVaS-akhZ75PQ'


    print(TestCognito.Redirect_URL)
    print(TestCognito.oauth2_login())
    print(TestCognito.oauth2_logout())
    print(TestCognito.oauth2_logout())
