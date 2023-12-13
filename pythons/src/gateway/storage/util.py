import pika, json

def upload(f, fs, channel, access):
    # upload he file to mongodb using gridfs
    # upon successful upload send a message to the queue/rabbitmq
    try:
        fid = fs.put(f) # upon succeess, file id
    except Exception as err:
        return "internal server error", 500

    message = {
        "video_fid": str(fid),
        "mp3_fild": None,
        "username": access["username"],
    }

    # send message to rabbitmq
    try:
        channel.basic_publish(
            exchange='',
            routing_key='video',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # message are availabke after a restart or crash
            ),
        )
    except Exception as err:
        fs.delete(fid) #if the message is noot put in the queuem delete frommongo db since it will never be processed.
                    # the downstream services only process messages from the queue
        return "internal server error", 500
