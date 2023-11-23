from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost:1337/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('University', backref='students')
    admission_year = db.Column(db.Integer, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль', validators=[DataRequired(), EqualTo('password')])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_hash == form.password.data:
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UniversityForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    short_name = StringField('Short Name', validators=[DataRequired()])
    creation_date = DateField('Creation Date', validators=[DataRequired()])


class StudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    university = SelectField('University', coerce=int, validators=[DataRequired()])
    admission_year = StringField('Admission Year', validators=[DataRequired()])


@app.route('/')
def index():
    universities = University.query.all()
    return render_template('index.html', universities=universities)


@app.route('/university/<int:university_id>')
def university_detail(university_id):
    university = University.query.get(university_id)
    students = Student.query.filter_by(university_id=university_id).all()
    return render_template('university_detail.html', university=university, students=students)


@app.route('/create_university', methods=['GET', 'POST'])
@login_required
def create_university():
    form = UniversityForm()
    if form.validate_on_submit():
        university = University(
            full_name=form.full_name.data,
            short_name=form.short_name.data,
            creation_date=form.creation_date.data
        )
        db.session.add(university)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_university.html', form=form)


@app.route('/edit_university/<int:university_id>', methods=['GET', 'POST'])
@login_required
def edit_university(university_id):
    university = University.query.get(university_id)
    form = UniversityForm(obj=university)
    if form.validate_on_submit():
        form.populate_obj(university)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_university.html', form=form, university=university)


@app.route('/delete_university/<int:university_id>')
@login_required
def delete_university(university_id):
    university = University.query.get(university_id)
    db.session.delete(university)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)


@app.route('/create_student', methods=['GET', 'POST'])
@login_required
def create_student():
    form = StudentForm()
    form.university.choices = [(u.id, u.short_name) for u in University.query.all()]
    if form.validate_on_submit():
        student = Student(
            full_name=form.full_name.data,
            birth_date=form.birth_date.data,
            university_id=form.university.data,
            admission_year=form.admission_year.data
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('create_student.html', form=form)


@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get(student_id)
    form = StudentForm(obj=student)
    form.university.choices = [(u.id, u.short_name) for u in University.query.all()]
    if form.validate_on_submit():
        db.session.delete(student)
        student = Student(
            full_name=form.full_name.data,
            birth_date=form.birth_date.data,
            university_id=form.university.data,
            admission_year=form.admission_year.data
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('edit_student.html', form=form, student=student)


@app.route('/delete_student/<int:student_id>')
@login_required
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
