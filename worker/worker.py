import pika
import json
import base64
import redis
import getALPR
import getGeoTag
import socket

table1 = redis.StrictRedis(host="redis", db=1)
table2 = redis.ConnectionPool(host="redis", db=2)
cache2 = redis.Redis(connection_pool=table2)
table3 = redis.StrictRedis(host="redis", db=3)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')
result = channel.queue_declare(queue='toWorker')
queue_name = result.method.queue
channel.queue_bind(exchange='direct_exchange', queue=queue_name, routing_key='image')

#to send to rabbit
channel.exchange_declare(exchange='log_exchange', exchange_type='topic')
print("Waiting to receive messages...",flush=True)

#send output
def send_info_message(message_string):
    message = {'message_string' : message_string}
    routing_key = socket.gethostname()+".info"
    channel.basic_publish(exchange="log_exchange", routing_key=routing_key, body=json.dumps(message))

#send debug logs
def send_debug_message(message_string):
    message = {'message_string' : message_string}
    routing_key = socket.gethostname()+".debug"
    channel.basic_publish(exchange="log_exchange", routing_key=routing_key, body=json.dumps(message))

#md5, license:confidence:lat:long
def insert_table1(temp, latitude, longitude, md5):
    send_debug_message("Inserting into table 1")      
    for i in range(len(temp)):
        license_num = temp[i][0]
        confidence = temp[i][1]
        str1 = license_num+":"+str(confidence)+":"+str(latitude)+":"+str(longitude) 
        table1.sadd(md5, str1)
        send_info_message("Item being pushed: "+str1)
    send_debug_message("All push events successful")

#file_name, md5
def insert_table2(file_name, md5):
    send_info_message("Inserting into table 2: file_name: "+file_name+"md5: "+md5) 
    cache2.set(file_name, md5)
    send_debug_message("Push Successful")

#license_num, md5
def insert_table3(temp, md5):
    send_debug_message("Inserting into table 3:")
    for i in range(len(temp)):
        license_num = temp[i][0]
        #print(type(license_num), type(md5))
        table3.sadd(license_num, md5)
        send_info_message("Item being pushed: "+license_num+","+md5)
    send_debug_message("All push events successfull");
    
def write_image_to_file(datastore):
    f = open(datastore['filename'], 'wb')
    f.write(base64.b64decode(datastore['image']))
    f.close()       

def callback(ch, method, properties, body):
    send_debug_message("Recevied toWorker Message..")
    datastore = json.loads(body)

    send_debug_message("Received put_image request: ")
    file_name = datastore['filename']
    md5_val = datastore['md5']

    write_image_to_file(datastore)

    temp = getALPR.get_license(file_name)
    if len(temp) == 0:
        send_debug_message("Can't find plate for image: "+file_name)
        send_debug_message("Not inserting file "+file_name+ " into redis database")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    latitude, longitude = getGeoTag.main_func(file_name)
    if latitude is None or longitude is None:
        send_debug_message("No Latitude and Longitude for image: "+file_name)
        send_debug_message("Not inserting file "+file_name+ " into redis database")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
        
    #(md5, license:confidence:lat:long)
    insert_table1(temp, latitude, longitude, md5_val)
    #(file_name, md5)
    insert_table2(file_name, md5_val)  
    #(license_num, md5)
    insert_table3(temp, md5_val)

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name)
channel.start_consuming()