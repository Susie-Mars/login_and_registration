from flask import Flask
DATABASE = "users_schema"
app= Flask(__name__)
app.secret_key = "Our secret!"

