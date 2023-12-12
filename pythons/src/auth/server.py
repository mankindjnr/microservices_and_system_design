import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# configuration for our server
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization # get the authorization header (username, password)
    if not auth:
        return "Missing credentials", 401

    # check database for username and password
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE email = %s", (auth.username))

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            # create a jwt token
            return createJWT(auth.username, os.environ.get("JWT_SECRET"))

    else:
        return "Invalid credentials", 401

# check if the jwt token is valid - the api gateway will call this to ensure  the user is authenticated
# and authorized to access the resource and also the token is not expired or tampered with
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "Missing Credentials", 401

    # decode the jwt token "Bearer <token>"
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded_jwt = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except:
        return "not authorized", 403

    return decoded_jwt, 200

# create a jwt token
def createJWT(username, secret, authz):
    return jwt.encode({
        "username": username,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "admin": authz,
    },
    secret,
    algorithm="HS256",
    )

if __name__ == "__main__":
    print("Starting server...")
    server.run(debug=True, host="0.0.0.0", port=5000)