from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    username = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50))

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('sign-in.html')

@app.route('/sign-in', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return redirect(url_for('profile', username=username))
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender'].lower()
        username = request.form['username']
        user_id = request.form['user_id']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        if gender == 'male':
            return 'Sign up failed. Gender must be "Female" or "Trans".'
        new_user = User(name=name, age=age, gender=gender, username=username, user_id=user_id, password=password, phone=phone, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('profile', username=username))  # Redirect to profile page after signup
    return render_template('signup.html')

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('profile.html', user=user)
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)