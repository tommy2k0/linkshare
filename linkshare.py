from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from passwordhelper import PasswordHelper
from forms import RegistrationForm
from forms import LoginForm
from forms import AddLinkForm

import config

if config.test:
	from mockdbhelper import  MockDBHelper as DBHelper
else:
	from dbhelper import DBHelper

from user import User

app = Flask(__name__)
app.secret_key = 'tPXJY3Z37Qybz4QyhV+hOyUxVQeEXf1Ao2C8upz+fGQXKsM' 
login_manager = LoginManager(app)
DB = DBHelper()
PH = PasswordHelper()

@app.route('/')
def home():
	return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm(), addlinkform=AddLinkForm())

@app.route('/account')
@login_required
def account():
	links = DB.get_links(current_user.get_id())
	return render_template("account.html", links=links, addlinkform=AddLinkForm())

@app.route('/login', methods=["POST"])
def login():
	form = LoginForm(request.form)
	if form.validate():
		stored_user = DB.get_user(form.loginemail.data)
		if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
			user = User(form.loginemail.data)
			login_user(user, remember=True)
			return redirect(url_for('account'))
		form.loginemail.errors.append("Email or password invalid")
	return render_template("home.html", loginform=form, registrationform=RegistrationForm(), addlinkform=AddLinkForm())

@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route('/register', methods=["POST"])
def register():
	form = RegistrationForm(request.form)
	if form.validate():
		if DB.get_user(form.email.data):
			form.email.errors.append("Email address already registered")
			return render_template("home.html", loginform=LoginForm(), registrationform=form)
		salt = PH.get_salt()
		hashed = PH.get_hash(form.password2.data + salt)
		DB.add_user(form.email.data, salt, hashed)
		return render_template("account.html", addlinkform=AddLinkForm(), onloadmessage="Registration successful.")
	return render_template("home.html", loginform=LoginForm(), registrationform=form)

@app.route('/account/addlink', methods=["POST"])
@login_required
def add_link():
	form = AddLinkForm(request.form)
	if form.validate():
		DB.add_link(form.link.data, current_user.get_id())
		return redirect(url_for("account"))
	return render_template("account.html", addlinkform=form, links=DB.get_links(current_user.get_id()))

@app.route('/account/deletelink')
def delete_link():
	linkid = request.args.get("linkid")
	DB.delete_link(linkid)
	return redirect(url_for('account'))


if __name__ == '__main__':
	app.run(port=5000, debug=True)
