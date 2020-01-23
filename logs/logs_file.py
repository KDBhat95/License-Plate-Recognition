import pika
import json
import base64
import redis
import datetime

#Write log to file
def callback(ch, method, properties, body):
    data = json.loads(body)
    message_string = data['message_string']
    with open("log_file.log", "a+") as f:
        f.write(str(datetime.datetime.now())+" "+method.routing_key+": "+ message_string+"\n")

#Connect to rabbit
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='log_exchange', exchange_type='topic')

#First queue for info messages
result = channel.queue_declare(queue='Info_log_queue')
queue_name1 = result.method.queue
channel.queue_bind(exchange='log_exchange', queue=queue_name1, routing_key='*.info')

#Second queue for debug messages
result = channel.queue_declare(queue='Debug_log_queue')
queue_name2 = result.method.queue
channel.queue_bind(exchange='log_exchange', queue=queue_name2, routing_key='*.debug')

#Consume Info logs
channel.basic_consume(on_message_callback=callback, queue=queue_name1, auto_ack=True)
#Consume Debug logs
channel.basic_consume(on_message_callback=callback, queue=queue_name2, auto_ack=True)

channel.start_consuming()