from flask import Flask, render_template, request, redirect, url_for, session, flash

from models import db, Users


app = Flask(__name__)
app.secret_key = '12345'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = Users.query.filter_by(username=username).first()

        if user:
            # Verify the password
            if user.password == password:
                # Store the user's id in the session
                session['user_id'] = user.id
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password. Please try again.', 'error')
        else:
            flash('User does not exist. Please sign up.', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))

        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

