# import the Flask constructor
from flask import Flask
# import various Flask modules that we will be using
from flask import render_template, redirect, url_for, session, request
# call the constructor on our current context
app = Flask(__name__)
# initialize the session module (used for cookies) with a cryptographically
# secure secret key, in order to prevent clients from forging cookies
# (The session module handles everything for us, we just need to provide this)
app.secret_key = 'some secret'

# a list to keep track of all the users who log in
users = []

# handle the login logic for some user, assuming password was good
def login(username):
  # set the "logged_in" cookie to True
  # we could also set session['username'], but we don't in order to showcase
  # dynamic urls in show_users
  session['logged_in'] = True
  # add this user to the users list
  users.append(username)

# This is an annotation that tells Flask to connect the following function with 
# the url '/'. When clients request '/', we run this function and send back to the 
# client the return value 
@app.route('/')
def main_page():
  # render_template uses Jinja2, Flask's built-in templating system with our 
  # homepage, located in the templates directory
  # We could also use a different templating engine if we wanted to
  return render_template('home.html')

# This is the login page. We want to allow clients to submit GET or POST requests
@app.route('/login', methods=['GET', 'POST'])
def handle_login():
  # If they are GETting this page, we just send back the login page
  # (just navigating to /login in their browser)
  if request.method == 'GET':
    return render_template('login.html')
  # If they POSTed to this page (ie a form submission), start trying to validate
  else:
    # request.form is the place where we can find the data from the POST request
    password = request.form['password']
    user = request.form['user']
    if password == "secret":
      # validation successful - login the user
      login(user)
      # url_for gives us the url of the show_users method, in this case when called
      # with this particular user. 
      # This is convenient because we can easily change the location of /users to 
      # /ids without having to update this redirection logic
      return redirect(url_for('show_users', name=user))
    else:
      # We pass an error value into render_template. Jinja2, the template rendering
      # engine, will run through the logic specified in login.html with this variable
      return render_template('login.html', error="Invalid credentials")

# <name> is a dynamic part of this url. This means that /users/sudarshan and
# /users/joe are both valid urls, and the <name> part will get passed into the 
# following function
@app.route('/users/<name>')
def show_users(name):
  # if not logged in, we redirect to home
  if not session.get('logged_in'):
    return redirect(url_for('main_page'))
  # We pass in both the username and the list of users into render_template.
  # Jinja2 will run through the logic in users.html using these values
  return render_template('users.html', name=name, users=users)

# If we are running this app from the command line. The standard way to prevent
# our Flask site from starting if we import this as a module for something else
if __name__ == '__main__':
  # Running with debug=True does 2 things:
  # 1 - restarts the server anytime we make a change to this (or any) file
  # 2 - provides a nice debugging interface with stack traces and correctly-scoped
  # consoles if we get a runtime error
  # Note that this allows people who view your site to run arbitrary code on your 
  # computer, so you don't want debug=True to be set when you publish your site
  app.run(debug = True)