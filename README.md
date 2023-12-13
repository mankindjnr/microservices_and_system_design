# microservices architecture and system design (python and kubernetes)

## KEY TERMS
***
### Synchronous interservice communication
- it means that the client will wait for the response from the server before it can continue with the next task.
    The client service cannot do anything when it is waiting for the response from the server. it is essentially blocked.

    __An example of this in our application will be the _api gateway_ and the _auth_ service, when the user is signing up or logging in so as to use our application, the api gateway will block itself as it awaits the _auth_ service to respond with the jwt token.__ 
    _This way, only authenticated users will be able to use our application._

### Asynchronous interservice communication
- it means that the client will not wait for the response from the server before it can continue with the next task.
    The client service can do other things when it is waiting for the response from the server. it is not blocked.
    We achieve this by using a message queue.

    Our gatewayy does not communicate directly with our converter service, instead, it puts a message in the queue, the converter service then consumes the message from the queue and then does its job. When the converter service is done, it puts a message in the queue, the notification service then consumes the message from the queue and then does its job.

    __An example of this in our application will be the _api gateway_ and the _video to mp3 converter_ service, when the user uploads a video, the api gateway will not block itself as it awaits the _video to mp3 converter_ service to respond with the converted mp3 file.__
    _This way, the user can upload multiple videos at the same time._

### Strong consistency
- it means that the data is always consistent across all services.
    This is achieved by using a database that supports strong consistency, such as mysql.

### Eventual consistency
- it means that the data is not always consistent across all services.
    This is achieved by using a database that supports eventual consistency, such as mongodb.
***
We will use the following tools to build this microservice:

1. python
2. mongoDB
3. Docker
4. Kubernetes /minikube
5. Mysql
6. RabbitMQ
7. k9s

The focus will not be in the microservices themselves, instead, the focus will fall on the connection of the services, the communication and relation to each other.

## The application top-down

The application is a video to mp3 converter.

Our application resides in kubernetes cluster, it is not accessible or available to the public, the only way to access it is through the api gateway. The api gateway is the only service that is exposed to the public, it is the only service that has a public ip address. The api gateway will be the one that receives requests from the client and then route the request to the appropriate service. The api gateway will also be the one that will send responses to the client.

__user uploads video -> hits the api gateway -> the gateway will then store the video in mongodb and then put a message to the queue(RabbitMQ) -this lets the downstream services know that there is a video to be processed in mongodb -> the video to mp3 converter consumes messages from RabbitMQ, it then gets the id of the video from the message, pull the video from mongodb, convert the video to mp3, store the mp3 in mongodb, -> then put a new message to the queue -> the notification service will then consume the message (the conversion job is done) -> when the notification service consumes the message in the queue it sends an email notifictio to the user that the conversion is done and ready for download. The user will then use the unique id from the notification and the jwt to send a request to the api gateway to download the mp3 -> the api gateway will then pull the mp3 from mongodb and serve to the client.__


Since we are going to be creating alot of services, we will have multiple folders in our repo, first

# PYTHON MICROSERVICES
This folder will have our python microservices, they are:

1. auth


### Auth
This service will handle the authentication of the user, it will be responsible for creating new users, logging in users and generating jwt tokens. We have imported datetme to help us set the expiry of the jwt token.

We are going to start with creating the server.

```python
import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)
```

### setting the environment variables

```python
server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
```
```bash
export MYSQL_HOST=127.0.0.1
```
```python
print(os.environ.get('MYSQL_HOST'))
print(server.config['MYSQL_HOST'])
```