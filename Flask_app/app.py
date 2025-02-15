from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Credential.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, try again."
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        new_user = User(name=name, age=age, gender=gender)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/update_credentials', methods=['GET', 'POST'])
def update_credentials():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = Credential.query.filter_by(username=session['user']).first()
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        db.session.commit()
        session['user'] = user.username  # Update session
        return redirect(url_for('index'))
    return render_template('update_credentials.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Insert admin and sandhiya credentials if they don't exist
        default_users = [
            {'username': 'admin', 'password': 'admin123'},
            {'username': 'sandhiya', 'password': 'sandhiya123'}
        ]
        
        for user in default_users:
            if not Credential.query.filter_by(username=user['username']).first():
                new_user = Credential(username=user['username'], password=user['password'])
                db.session.add(new_user)
        db.session.commit()

    app.run(host='0.0.0.0', port=5000, debug=True)
