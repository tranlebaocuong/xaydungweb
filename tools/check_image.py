import sys
from urllib import request, parse

if len(sys.argv) < 2:
    print('Usage: check_image.py <path_relative_to_root>')
    sys.exit(2)

path = sys.argv[1]
url = 'http://localhost:8000/' + parse.quote(path, safe='/:')
print('Checking', url)
try:
    resp = request.urlopen(url)
    print('HTTP', resp.getcode())
    print('Content-Length:', resp.getheader('Content-Length'))
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
