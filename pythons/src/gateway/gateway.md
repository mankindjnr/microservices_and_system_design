# API GATEWAY

## Dependancies

- gridfs - this is going to allow us to store large files in mongodb
- pika - this is going to allow us to communicate with rabbitmq

```python
server = Flask(__name__)
server.config['MONGO_URI'] = "mongodb://host.minikube.internal:27017/videos"
```

- `mongodb://host.minikube.internal:27017/videos` - this is the mongodb uri that we are going to use to connect to the mongodb database. `host.minikube.internal` gives us access to our localhost from inside the cluster.

- `videos` - this is the name of the database that we are going to use.
- `27017` - this is the port that mongodb is running on.

```python
fs = gridfs.GridFS(mongo.db)
```

- `fs` - this is the gridfs object that we are going to use to store and retrieve files from mongodb.

We are going to use mongodb to store our videos and mo3 files. Gridfs is a way to store large files in mongodb. 
Mongodb has a limit of 16mb per document. Gridfs allows us to store files larger than 16mb by splitting them into chunks and storing them in a separate collection. 

mongodb sets this limits since it may cause degredation in performance.

`collections == tables`

Since Gridfs splits the file into chunks we will use this collections to interact with it:

- `fs.files` - this is the collection that stores the metadata of the file.
- `fs.chunks` - this is the collection that stores the chunks of the file.


### RabbitMQ

```python
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
```

The `rabbitmq` string references our rabbitmq host.
The `BlockingConnection` allows for asynchronous communication with rabbitmq.

