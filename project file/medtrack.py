from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Temporary in-memory user store
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return "User already exists!"

        users[username] = {'password': password, 'role': role}
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(f"/{user['role']}")

        return "Invalid credentials!"

    return render_template('login.html')

@app.route('/doctor')
def doctor_dashboard():
    if 'role' in session and session['role'] == 'doctor':
        return render_template('doctor.html', username=session['username'])
    return redirect('/login')

@app.route('/patient')
def patient_dashboard():
    if 'role' in session and session['role'] == 'patient':
        return render_template('patient.html', username=session['username'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
