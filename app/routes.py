from app import app, db
from flask import session, render_template, flash, redirect, url_for, request, send_from_directory
#from app.RFIs import RFI -----Removed this as it was replaced by the database model Rfi
from app.forms import RFIForm, LoginForm, RegistrationForm, ResponseForm, TeamForm, ProjectForm
from app.models import User,Rfi,Team,Project
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import os
from functools import wraps
from app.pdf_create import RFI_PDF
from app.permissions import team_only, design_team_only, construction_team_only, construction_manager_only

@app.route('/')
@app.route('/index')
@login_required
def index():
	projects = Project.query.order_by(Project.unit_name.asc(), Project.proj_title.asc())
	return render_template('index.html', title='Home', projects=projects)


@app.route('/add_rfi/<id>', methods=['GET', 'POST'])
@login_required
@construction_team_only
def add_rfi(id):
	project = Project.query.filter_by(id=id).first_or_404()
	form = RFIForm()
	if form.validate_on_submit():
		filename ='RFI' + form.rfi_number.data +' - '+ form.title.data +'.pdf'
		filepath = os.path.join(app.config['UPLOAD_FOLDER'],project.proj_title)
		fullpath =os.path.join(filepath,filename)
		if not os.path.exists(filepath):
			os.mkdir(filepath)
		form.UploadFile.data.save(fullpath)
		
		rfi=Rfi(
			rfi_number=form.rfi_number.data, 
			title=form.title.data,
			date_received=form.date_received.data,
    		dwg_refer=form.dwg_refer.data,
			spec_refer=form.spec_refer.data,
			assigned_to=form.assigned_to.data,
			cost_change=form.cost_change.data,
			time_change=form.time_change.data,
			filename=filename,
			project = project
			)

		db.session.add(rfi)
		db.session.commit()
		flash('RFI {} - {} Submitted'.format(form.rfi_number.data, form.title.data))
		return redirect(url_for('rfilog', id=project.id))
	return render_template('add_rfi.html', title='Add RFI', form=form, project=project)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
        
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')

		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html',  title='Sign In', form=form)    

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/rfilog/<id>')
@login_required
@team_only
def rfilog(id):	
	rfis=Rfi.query.filter_by(project_id=int(id)).order_by(Rfi.rfi_number.asc()).all()
	project = Project.query.filter_by(id=id).first_or_404()
	return render_template('RFI_Log.html', title='RFI Log', rfis=rfis, project=project)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/RFI_Resp/<id>/<rfi_number>',methods=['GET', 'POST'])
@login_required
@design_team_only
def RFI_Resp(id,rfi_number):
	form = ResponseForm()
	rfi = Rfi.query.filter_by(project_id=int(id), rfi_number=rfi_number).first_or_404()
	project = Project.query.filter_by(id=id).first_or_404()
	if form.validate_on_submit():
		rfi.date_response = form.date_response.data
		rfi.response = form.response.data
		rfi.reviewer = form.reviewer.data
		fname='State Response RFI ' + str(rfi.rfi_number) + ' - ' + rfi.title +'.pdf'
		rfi.response_fname = fname
		db.session.commit()
		
		create_pdf(rfi,project)
		
		return redirect(url_for('rfilog', id=project.id))
	elif request.method == 'GET':
		form.date_response.data = rfi.date_response
		form.response.data = rfi.response
		form.reviewer.data = rfi.reviewer
	return render_template('RFI_Resp.html', rfi=rfi, form=form, project=project)    

@app.route('/uploads/<id>/<path:filename>', methods=['GET', 'POST'])
def showfile(id, filename):
	project = Project.query.filter_by(id=id).first_or_404()
	uploads = os.path.join(app.config['UPLOAD_FOLDER'],project.proj_title)
	return send_from_directory(directory=uploads, filename=filename)

@app.route('/manageteam/<id>', methods=['GET', 'POST'])
@login_required
@construction_manager_only
def manageteam(id):
	project = Project.query.filter_by(id=id).first_or_404()
	form = TeamForm()
	team=Team.query.filter_by(project_id=int(id)).order_by(Team.role.asc()).all()
	if form.validate_on_submit():
		member=Team(
			role = form.role.data,
			firstname = form.fName.data,
			lastname = form.lName.data,
			email = form.email.data,
			project_id= project.id
			)
		exists = Team.query.filter_by(project_id=int(id),role=form.role.data).first()
		if not exists:
			db.session.add(member)
			db.session.commit()
			flash('Team Member {} {} added'.format(form.fName.data, form.lName.data))
		else:
			db.session.commit()
			flash('Team Member {} {} updated'.format(form.fName.data, form.lName.data))
		return redirect(url_for('manageteam', id=project.id))
	return render_template('manageteam.html',title='Manage Team Members', team=team, form=form, project=project)

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
	form = ProjectForm()
	if form.validate_on_submit():
		project=Project(
			unit_name = form.unit_name.data,
			proj_title = form.proj_title.data,
			)
		db.session.add(project)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('create_project.html',title='Create a new project', form=form)

@app.route('/responses/<id>/<path:filename>', methods=['GET', 'POST'])
def showresp(id, filename):
	project = Project.query.filter_by(id=id).first_or_404()
	uploads = os.path.join(app.config['RESPONSES_FOLDER'], project.proj_title)
	return send_from_directory(directory=uploads, filename=filename)

@app.route('/proj/<id>')
@login_required
@team_only
def proj(id):
	form = ResponseForm()
	project = Project.query.filter_by(id=id).first_or_404()
	return render_template('proj.html', project=project)  

def create_pdf(rfi,project):
	pdf = RFI_PDF(orientation='P', format='Letter')
	pdf.alias_nb_pages()
	pdf.add_page()
	pdf.borders()
	pdf.headers(rfi.rfi_number, rfi.title, rfi.date_received, rfi.date_response, rfi.dwg_refer,rfi.spec_refer,rfi.response,rfi.reviewer, project.unit_name, project.proj_title)

	fname='State Response RFI ' + str(rfi.rfi_number) + ' - ' + rfi.title +'.pdf'
	fpath=os.path.join(app.config['RESPONSES_FOLDER'], project.proj_title)
	if not os.path.exists(fpath):
		os.mkdir(fpath)
	pdf.output(os.path.join(fpath,fname), 'F')	
	

