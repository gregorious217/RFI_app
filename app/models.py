from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean)


	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash,password)


class Rfi(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rfi_number = db.Column(db.String(4), index=True)
	title = db.Column(db.String(120), index=True)
	date_received = db.Column(db.String(40), index=True)
	date_response = db.Column(db.String(40), index=True)
	dwg_refer = db.Column(db.String(60), index=True)
	spec_refer = db.Column(db.String(120), index=True)
	assigned_to = db.Column(db.String(60), index=True)
	cost_change = db.Column(db.Boolean)
	time_change = db.Column(db.Boolean)
	response = db.Column(db.Text(400))
	reviewer = db.Column(db.String(60))
	filename = db.Column(db.String(100))
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	response_fname = db.Column(db.String(100))

	def __repr__(self):
		return '<RFI {} - {}>'.format(self.rfi_number,self.title)

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String(60))
	firstname = db.Column(db.String(30), index=True)
	lastname = db.Column(db.String(30), index=True)
	email = db.Column(db.String(60), index=True, unique=True)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	
	def __repr__(self):
		return '<{} - {}  {} , {}>'.format(self.role,self.firstname,self.lastname, self.email)

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	unit_name = db.Column(db.String(120), index=True)
	proj_title = db.Column(db.String(120), index=True, unique=True)
	rfis = db.relationship("Rfi", backref="project", lazy="dynamic")
	team = db.relationship('Team', backref="team", lazy="dynamic")

@login.user_loader
def load_user(id):
	return User.query.get(int(id))