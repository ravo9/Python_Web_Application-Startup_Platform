import json, os
import sqlite3
from flask import Flask, g, session, url_for, redirect

app = Flask(__name__)


def init_db():
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  with app.open_resource('data_schema.sql', mode='r') as f:
    c.executescript(f.read())
  conn.commit()
  conn.close()


# A function returning a total number of current circles.
def get_number():
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  acc = 0
  sql = "SELECT * FROM circles"
  for row in c.execute(sql):
    acc += 1
  conn.close()
  return acc


def get_new_id():
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  sql = "SELECT id FROM circles ORDER BY id DESC LIMIT 1"
  c.execute(sql)
  temp = c.fetchone()
  if (temp is None):
    return 0
  else:
    new_id = temp[0]
    return int(new_id) + 1


# A function that returns a circle of a given ID.
def read_circle( id ):
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  circle = []
  c.execute('select * from circles where id =?', (id,))
  circle = c.fetchone()
  conn.close()
  if circle == None:
    circle = []
  return circle

# A function that returns all circles.
def read_all_circles():
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  circles = []
  c.execute('select * from circles')
  for row in c:
    circles.append(row)
  conn.close()
  if circles == None:
    circles = []
  return circles


def add_circle ( circle ):
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  c.execute('insert into circles values (?,?,?,?,?,?,?,?,?,?)', (circle[0], circle[1], circle[2], circle[3], circle[4], circle[5], circle[6], circle[7],circle[8], circle[9],))
  conn.commit()
  conn.close()


def delete_circle ( id ):
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  c.execute('delete from circles where id =?', (id,))
  conn.commit()
  conn.close()
  return 

 

