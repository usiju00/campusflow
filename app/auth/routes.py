from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.models import Student, Wallet
from app import db
import bcrypt

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        matric_number = request.form['matric_number']
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']
        level = request.form['level']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        student = Student(
            full_name=full_name,
            matric_number=matric_number,
            email=email,
            password_hash=hashed.decode('utf-8'),
            department=department,
            level=level
        )
        db.session.add(student)
        db.session.flush()
        wallet = Wallet(student_id=student.id)
        db.session.add(wallet)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matric_number = request.form['matric_number']
        password = request.form['password']
        student = Student.query.filter_by(matric_number=matric_number).first()
        if student and bcrypt.checkpw(password.encode('utf-8'), student.password_hash.encode('utf-8')):
            login_user(student)
            return redirect(url_for('auth.dashboard'))
        flash('Invalid credentials')
    return render_template('auth/login.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html', student=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
