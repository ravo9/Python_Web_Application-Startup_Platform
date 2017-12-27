import json
import sqlite3
import bcrypt
from flask import Flask, g, session, url_for, redirect

app = Flask(__name__)


def init_db():
  conn = sqlite3.connect('data/users.db')
  c = conn.cursor()
  with app.open_resource('users_schema.sql', mode='r') as f:
    c.executescript(f.read())
  conn.commit()
  conn.close()


# A function returning a total number of users.
def get_number():
  conn = sqlite3.connect('data/users.db')
  c = conn.cursor()
  acc = 0
  sql = "SELECT * FROM users"
  for row in c.execute(sql):
    acc += 1
  conn.close()
  return acc


# A function that returns a user of a given mail.
def read_user( mail ):
  conn = sqlite3.connect('data/users.db')
  c = conn.cursor()
  user = []
  c.execute('select * from users where mail =?', (mail,))
  user = c.fetchone()
  conn.close()
  if user == None:
    user = []
  return user


def add_user ( user ):
  conn = sqlite3.connect('data/users.db')
  c = conn.cursor()
  # Password encrypting.
  user[1] = bcrypt.hashpw(user[1], bcrypt.gensalt())
  c.execute('insert into users values (?,?,?,?,?,?,?,?,?,?,?)', (user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10],))
  conn.commit() 
  conn.close()


# A function checking login credentials.
def check_credentials ( mail, password ):
  conn = sqlite3.connect('data/users.db')
  c = conn.cursor()
  c.execute('SELECT password FROM users WHERE mail =?', (mail,))
  db_password = c.fetchone()
  conn.close()
  if db_password == bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()):
    print db_password
    print "HERE"
    return 'true'
  else:
    return 'false'
