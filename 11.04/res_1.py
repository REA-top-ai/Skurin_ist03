import requests
from requests.auth import HTTPBasicAuth
basic = HTTPBasicAuth('user', 'pass')
a = requests.get('https://httpbin.org/basic-auth/user/pass', auth=basic)
print(a.json())

import requests

bearer_token = "sdfjahiHKJSDBfheJBDF3u283HGAF"

headers = {"Authorization": f"Bearer {bearer_token}"}

response = requests.get("https://httpbin.org/headers", headers=headers)

print(response.json())



from requests.auth import HTTPDigestAuth
url = 'https://httpbin.org/digest-auth/auth/user/pass'
a = requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
print(a.json())
