import os, pandas as pd, numpy as np, joblib, xgboost as xgb, pika, logging, json, time, base64
from datetime import timedelta
import httpx
from io import StringIO

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

connection_params = pika.ConnectionParameters(host='rabbitmq',
                                              port=5672,
                                              virtual_host='/',
                                              credentials=pika.PlainCredentials(
                                                  username='rbbmq',
                                                  password='rbbmqpwd'
                                              ),
                                              heartbeat=30,
                                              blocked_connection_timeout=2)

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

queue_name = 'ml_task_queue'
channel.queue_declare(queue=queue_name)

def callback(ch, method, properties, body, *args, **kwargs):
    payload = json.loads(body)
    #file_name = payload['image']
    #image = base64.b64decode(payload['bytes'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue_name, 
                     on_message_callback=callback,
                     auto_ack=False)


logger.info('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()