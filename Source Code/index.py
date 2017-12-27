from flask import Flask, render_template, url_for, request, redirect, session
from functools import wraps
from datetime import datetime
import ConfigParser
import data
import find
import users
import bcrypt

app = Flask(__name__)
app.secret_key = '3123929813983dshaudhs'

def init(app):
  config = ConfigParser.ConfigParser()
  try:
    config.read("etc/defaults.cfg")
    app.config['ip_address'] = config.get("config", "ip_address")
    app.config['port'] = config.get("config", "port")
  except:
    print "The config file couldn't be read."


@app.route("/")
@app.route("/page/<page_number>")
def index(page_number=1):

  last_index = data.get_number() - 1

  newest_circles = []

  page_number = int(page_number)
    
  # Looking for (and uploading) the 15 newest circles.
  all_circles = data.read_all_circles() 

  first_index = 9 * page_number - 9;
  last_index = first_index + 8;

  for x in range(first_index, last_index):
    try:
      newest_circles.append(all_circles[x]) 
    except:
      pass

  # A flag indicating that there are no more elements and there's no need to
  # implement "next page" button anymore.
  last_page_flag = 0
   
  # A variable telling the html file if the user is logged in or not (needed
  # to display a correct version of the nav toolbar).
  status = session.get('logged_in', False)
  username = session.get('user', "Anonymous user")
  if (username == ''):
    username = "Anonymous user"
  user = users.read_user(username) 

  return render_template('index.html', newest_circles = newest_circles, page_number = page_number,
      last_page_flag = last_page_flag, status = status, username=username,
      user=user)


# A function checking if the user is logged in or not to provide a proper
# access level.
def check_if_logged(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    status = session.get('logged_in', False)
    if status == True:
      return f(*args, **kwargs)
    else:
      return redirect('/users/login')
  return decorated


@app.route("/circles/add_circle", methods=['POST', 'GET'])
@check_if_logged
def add_circle():
  if request.method == 'POST':
    id = data.get_new_id()
    leader_mail = session['user']
    status = 'current'
    title = request.form['title']
    desc = request.form['desc']
    public_date = datetime.now().strftime("%Y-%m-%d")
    expiry_date = request.form['expiry_date']
    investment_value = request.form['investment_value']
    photo = request.files['photo']
    photo.save('static/uploads/circle'+str(id)+'.png')  
    circle = [id, leader_mail, status, title, desc, public_date, expiry_date, investment_value, "", ""]
    data.add_circle( circle )

    #return redirect('/circles/add_circle/published')
    return redirect('/')

  else:
    # A variable telling the html file if the user is logged in or not (needed
    # to display a correct version of the nav toolbar.
    status = session.get('logged_in', False)
    username = session.get('user', "Anonymous user")
    if (username == ''):
      username = "Anonymous user"
    user = users.read_user(username) 
    return render_template('add_circle.html', status=status, user=user,
    username=username)


@app.route("/users/login", methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    login = request.form['login']
    password = request.form['password']
    result = users.check_credentials( login, password )
    if result == 'true':
      session['logged_in'] = True
      session['user'] = login
      return redirect('/')
    else:
      return render_template('login.html', user=user, status=status)
  else:
    return render_template('login.html')


@app.route("/users/logout")
def log_out():
  session['logged_in'] = False
  session['user'] = ""
  return render_template('logout.html')


@app.route("/users/register", methods=['POST', 'GET'])
def register():
  if request.method == 'POST':
    mail = request.form['mail']
    password = request.form['password']
    first_name = request.form['first_name']
    surname = request.form['surname']
    address = request.form['address']
    town = request.form['town']
    post_code = request.form['post_code']
    country = request.form['country']
    phone = request.form['phone']
    desc = request.form['desc']
    photo = request.files['photo_user']
    photo.save('static/uploads/user'+str(mail)+'.png')  
    user = [mail, password, first_name, surname, "01-01-1999", address, town, post_code, country, phone, desc]
    users.add_user( user )
    session['logged_in'] = True
    session['user'] = mail
    return redirect('/')
  else:
    return render_template('register.html')


@app.route("/users/account", methods=['POST', 'GET'])
@check_if_logged
def account():
  if request.method == 'POST':
    return redirect('/')
  else:
    # User has to be read here to supply proper user data to be displayed.
    user = users.read_user( session['user'] )
   
    status = session.get('logged_in', False)
    username = session.get('user', "Anonymous user")
    user_mail = session.get('user', 'None')
    user = users.read_user(user_mail)  

    return render_template('account.html', user=user, status=status, username=username)


@app.route("/circles/<id>", methods=['POST', 'GET'])
@check_if_logged
def circle(id=-1):
  if request.method == 'POST':
    return redirect('/')
  else:
    id = int(id)
    status = session.get('logged_in', False)
    username = session.get('username', "Anonymous user")
    user_mail = session.get('user', 'None')
    user = users.read_user(user_mail)  
    circle = data.read_circle(id)

    status = session.get('logged_in', False)
    username = session.get('user', "Anonymous user")
    user_mail = session.get('user', 'None')
    user = users.read_user(user_mail)  

    return render_template('circle.html', user=user,
    circle=circle, username=username, status=status)


@app.route("/users/<mail>", methods=['POST', 'GET'])
@check_if_logged
def user(mail='null'):
  if request.method == 'POST':
    return redirect('/')
  else:
    mail = str(mail)
    status = session.get('logged_in', False)
    username = session.get('user', "Anonymous user")
    user_mail = session.get('user', 'None')
    user = users.read_user(mail)  
    return render_template('user.html', user=user)


# An internal search engine.
@app.route("/circles/find_circle", methods=['POST', 'GET'])
def find_circle():
  if request.method == 'POST':
    phrase = request.form['phrase']
    min_investment = request.form['min_investment']
    max_investment = request.form['max_investment'] 
    results = find.find_all_matching(phrase, min_investment, max_investment)

    # A variable telling the html file if the user is logged in or not (needed
    # to display a correct version of the nav toolbar.
    status = session.get('logged_in', False)
    username = session.get('user', "Anonymous user")
    user_mail = session.get('user', 'None')
    user = users.read_user(user_mail)  
    return render_template('results.html', results = results, status=status,
    user=user, username=username)

  else:

    # A variable telling the html file if the user is logged in or not (needed
    # to display a correct version of the nav toolbar.
    status = session.get('logged_in', False)
    username = session.get('user', "Anonymous user")
    user_mail = session.get('user', 'None')
    user = users.read_user(user_mail)  
    return render_template('find_circle.html', status=status, user=user,
    username=username)


@app.route("/circles/remove/<id>")
@check_if_logged
def remove(id=None):
  data.delete_circle(id)
  try:
    os.remove('static/uploads/circle'+str(id)+'.png')
  except:
    print "File doesn't exist."
  return redirect("/")


if __name__ == "__main__":
  init(app)
  #data.init_db()
  #users.init_db()
  app.run(host=app.config['ip_address'], port=app.config['port'])

