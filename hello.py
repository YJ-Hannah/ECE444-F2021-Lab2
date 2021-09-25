from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	email = StringField('What is your UofT Email address?', validators=[Required(), Email()])
	submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	isEmail = None
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		if 'utoronto' not in form.email.data:
			isEmail = False
		else :
			isEmail = True
		session['name'] = form.name.data
		session['email'] = form.email.data
		session['isEmail'] = isEmail
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), isEmail=session.get('isEmail'))

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
	app.run(debug=True)

