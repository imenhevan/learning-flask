from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgres://wkznuojfpkvlab:21e65ad54aba15bc8a076c6fae50f975190a7ae403b4f8483a2c8d6a8d1be77e@ec2-54-235-193-0.compute-1.amazonaws.com:5432/dfh5f1pks6jd4v'
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:DBadmin@localhost/learningflask'
db.init_app(app)

app.secret_key="development-key"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
	if 'email' in session:
		return redirect(url_for('home'))

	form = SignupForm()
	if request.method=='POST':

		if form.validate()==False:
			print form.dob
			return render_template('signup.html',form=form)
		else:
			dob= datetime.strptime(form.dob.data, '%m/%d/%Y').date()
			newuser=User(form.first_name.data, form.last_name.data, form.email.data, form.password.data, dob)

			db.session.add(newuser)
			db.session.commit()

			session['email']=newuser.email
			return redirect(url_for('home'))

	elif request.method=='GET':
		return render_template('signup.html', form=form)

@app.route("/login", methods=["GET","POST"])
def login():
	if 'email' in session:
		return redirect(url_for('home'))

	form=LoginForm()
	if request.method == "POST":
		if form.validate()==False:
			return render_template("login.html",form=form)
		else:	
			email=form.email.data
			password=form.password.data

			user=User.query.filter_by(email=email).first()
			
			if user is None:
				session['loginerror']='Could not find user'
				return redirect(url_for('login'))

			if user.check_password(password):
				session['email']=form.email.data
				session['loginerror']=''
				return redirect(url_for('home'))
			else:
				session['loginerror']='Wrong password!'
				return redirect(url_for('login'))
	elif request.method=="GET":
		return render_template('login.html', form=form)

@app.route("/home", methods=["GET", "POST"])
def home():
	if 'email' not in session:
		return redirect(url_for('login'))
	
	form = AddressForm()

	places=[]
	my_coordinates=(37.4221, -122.0844)


	if request.method == 'POST':
		if form.validate == False:
			return render_template('home.html', form=form)
		else:
			# get the address
			address=form.address.data
			# query for places around it
			p=Place()
			my_coordinates=p.address_to_latlng(address)
			places=p.query(address)

			# return those results
			return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

	elif request.method == 'GET':
		return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)


@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))

if __name__ =="__main__":
	app.run(debug=True)