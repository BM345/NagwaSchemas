import requests 
import logging 
import http.client 
from headers import headers

http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger("requests.packages.urllib3")
logger.setLevel(logging.DEBUG)
logger.propagate = True 

url = "https://cds.nagwa.com/super.admin/single/437130710653/view/437130710653.question.xml/9/"

session = requests.Session()

for _ in range(10):

    r = session.get(url, headers = headers)
    r.raw.chunked = True 
    r.encoding = "utf-8"

    print(r.text)