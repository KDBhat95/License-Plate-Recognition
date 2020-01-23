# Sample Flask REST server implementing two methods
##
# Endpoint /api/image is a POST method taking a body containing an image
# It returns a JSON document providing the 'width' and 'height' of the
# image that was provided. The Python Image Library (pillow) is used to
# proce#ss the image
##
# Endpoint /api/add/X/Y is a post or get method returns a JSON body
# containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response
import jsonpickle
import numpy as np
from PIL import Image
import io
import hashlib
import pika
import json
import base64
import redis
import socket

app = Flask(__name__)

# def send_info_message(channel, message_string):
#     message = {'message_string' : message_string}
#     routing_key = socket.gethostname()+".info"
#     channel.basic_publish(exchange="log_exchange", routing_key=routing_key, body=json.dumps(message))

# #send debug logs
# def send_debug_message(channel, message_string):
#     message = {'message_string' : message_string}
#     routing_key = socket.gethostname()+".debug"
#     channel.basic_publish(exchange="log_exchange", routing_key=routing_key, body=json.dumps(message))

# route http posts to this method
@app.route('/image', methods=['PUT'])
def put_image():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        print("Received PUT_IMAGE request...")
        img_data = json.loads(r.data)
        de = base64.b64decode(img_data['image'])

        m = hashlib.md5(de)
        md_val = m.hexdigest()
        response = {
            'md5': md_val,
            }
        print("Returning Hash value: "+md_val)
        image_val = base64.encodebytes(de)
        image_val = image_val.decode('ascii')
        message = {'image': image_val, 'md5': md_val, 'filename': img_data['filename']}
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        print("Connection to RabbitMQ server: "+str(channel))

        channel.exchange_declare(exchange='log_exchange', exchange_type='topic')
        channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')
        channel.queue_declare(queue="toWorker")
        channel.basic_publish(exchange="direct_exchange", routing_key="image", body=json.dumps(message))
        connection.close()

    except Exception as e:
        print(str(e))
        response = {'md5': 0}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
@app.route('/hash/<string:checksum>', methods=['GET'])
def get_metadata(checksum):
    print("Received get request for checksum")
    try:
        table1 = redis.StrictRedis(host="redis", port=6379, db=1)
        list_value = table1.smembers(checksum)
        list_value = [x.decode('utf-8') for x in list_value]
        if len(list_value) != 0:
            response = {
                'metadata': list_value,
            }
            for i in list_value:
                print("Item retrieved from database: "+str(i))
            print("GET request for checksum successful")
        else:
            print("Could not find values for "+checksum)
            response = {
                'metadata': "No metadata",
            }

    except Exception as e:
        print(str(e))
        response = {'metadata': 'Error'}

    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/license/<string:license_number>', methods=['GET'])
def get_license(license_number):
    #r = request
    #data = json.loads(r.data)
    print("Received request for get license")
    try:
        table3 = redis.StrictRedis(host="redis", port=6379, db=3)
        list_value = table3.smembers(license_number)
        list_value = [x.decode('utf-8') for x in list_value]
        if len(list_value) != 0:
            response = {
                'license': list_value,
            }
            for i in list_value:
                print("Item retrieved from database: "+str(i))
            print("GET request for license successful")
        else:
            print("Could not find value(s) for "+license_number)
            response = {
                'license': "No license plates",
            }

    except Exception as e:
        print(str(e))
        response = {'license': "Error"}

    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


try:
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    # channel = connection.channel()
    # send_debug_message("Connection to RabbitMQ server: "+str(channel))
    # channel.exchange_declare(exchange='log_exchange', exchange_type='topic')
    app.run(host="0.0.0.0", port=5000)
except Exception as e:
    print(str(e))
