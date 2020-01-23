from __future__ import print_function
import requests
import json
import sys
import base64

host_ip = sys.argv[1]
method = sys.argv[2]
filename = sys.argv[3]

try:
    addr = 'http://'+host_ip+':5000'
    headers = {'content-type': 'application/json'}
    print(addr)
    print(filename)
    img = open(filename, 'rb').read()
    # send http request with image and receive response
    image_url = addr + '/image'

    image_val = base64.encodebytes(img)
    image_val = image_val.decode('ascii')

    requestBody = {'image': image_val, 'filename': filename}
    response = requests.put(image_url, data=json.dumps(requestBody), headers=headers)
    print("Response is:", response)
    print(json.loads(response.text))
except Exception as e:
    print(e)
